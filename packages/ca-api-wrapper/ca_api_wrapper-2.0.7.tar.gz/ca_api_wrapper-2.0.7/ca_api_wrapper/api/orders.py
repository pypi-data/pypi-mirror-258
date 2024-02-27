from .client import ChannelAdvisorClient
from .filters import Filter
import json

class OrderClient:
    def __init__(self, client: ChannelAdvisorClient):
        self.client = client

    def list(self, order_filter: Filter=None):
        if order_filter: 
            assert isinstance(type(order_filter) == Filter)
        
        params = {
            "$filter": order_filter.get_filter()
        }
        return self.client.make_request("v1/orders", params=params)

    def get_by_id(self, id):
        return self.client.make_request(f"v1/Orders({id})?$expand=Items")
    
    def create(self, order):
        return self.client.make_request("v1/orders/Create", method="POST", data=order)
    
    def create_private_note(self, id:int, note:str): 
        return self.client.make_request(f"v1/orders{id}", data=json.dumps({"PrivateNotes": {note}}))