from .client import ChannelAdvisorClient
from .filters import ProductFilter
import logging
import json
from urllib.parse import quote

log = logging.getLogger(__name__)
class ProductClient:
    def __init__(self, client:ChannelAdvisorClient):
        assert type(client) == ChannelAdvisorClient, "client must be a ChannelAdvisorClient object"
        self.client = client
        self._endpoints = ChannelAdvisorEndpoints(self.client)

    @property
    def products(self): 
        return self._endpoints.products

    @property   
    def attributes(self): 
        return self._endpoints.attributes

class ChannelAdvisorEndpoints: 
    def __init__(self, client:ChannelAdvisorClient):
        self.client = client
        self.products = ChannelAdvisorProductsEndpoints(self.client)
        self.attributes = ChannelAdvisorAttributesEndpoints(self.client)
        
class ChannelAdvisorProductsEndpoints: 
    def __init__(self, client:ChannelAdvisorClient):        
        self.client = client

    def list(self):
        return self.client.make_request("v1/products")
    
    def get_by_sku(self, sku): 
        product_filter = ProductFilter()
        
        encoded_sku = quote(sku)
        product_filter.add_filter(attribute="Sku", operator="eq", value=encoded_sku)
        sku_filter = product_filter.get_filter()
        
        return self.client.make_request("v1/products", params=f"$filter={sku_filter}")    
    
    def report_generator_get_by_sku_expand_attributes(self, sku, access_token): 
        product_filter = ProductFilter()

        product_filter.add_filter(attribute="Sku", operator="eq", value=sku)
        sku_filter = product_filter.get_filter()

        # Adding $expand parameter for attributes
        params = {
            "$filter": sku_filter,
            "$expand": "Attributes"
        }
        return self.client.make_request("v1/products", params=params)

    def get_by_id(self, id): 

        return self.client.make_request(f"v1/Products({id})")
    
    def get_by_upc(self, upc): 
        filter = ProductFilter()
        filter.add_filter(attribute="Upc", operator="eq", value=upc)
        upc_filter = filter.get_filter() 
        return self.client.make_request("v1/products", params=f"$filter={upc_filter}")
        
class ChannelAdvisorAttributesEndpoints: 
    def __init__(self, client:ChannelAdvisorClient):
        self.client = client

    def get(self, product_id: int, attribute_name: str):    
        return self.client.make_request(f"v1/Products({product_id})/Attributes('{attribute_name}')")

    def update(self, product_id: int, attribute_name: str, new_value): 
        data = {
            "Value": {"Attributes": [{"Name": attribute_name, "Value": str(new_value)}]}
        }
        return self.client.make_request(endpoint=f"v1/Products({product_id})/UpdateAttributes", method="POST", data=json.dumps(data))