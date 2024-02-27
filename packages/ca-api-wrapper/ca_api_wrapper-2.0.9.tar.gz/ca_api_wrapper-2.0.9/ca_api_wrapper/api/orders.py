from .client import ChannelAdvisorClient
from .filters import Filter
import json

from typing import List, Dict, Any

class OrderClient:
    def __init__(self, client: ChannelAdvisorClient):
        self.client = client

    def list(self, order_filter: Filter = None, paginate: bool = False, page_size: int = 250) -> List[Dict[str, Any]]:
        orders = []
        params = {"$top": page_size}

        if order_filter:
            assert isinstance(order_filter, Filter), "order_filter must be a Filter object"
            params["$filter"] = order_filter.get_filter()

        next_link = "v1/orders"
        
        while next_link:
            response = self.client.make_request(next_link, params=params)
            response_data = response.json()
            orders.extend(response_data.get('value', []))  # Assuming the list of orders is under 'value'
            
            # Check if there's a next link and if pagination is requested
            next_link = response_data.get('@odata.nextLink') if paginate else None
            if next_link:
                next_link = next_link.replace(self.client.base_url, "") 
                # Prepare for the next request
                params = {} 
                
        return orders

    def get_by_id(self, id):
        return self.client.make_request(f"v1/Orders({id})?$expand=Items")
    
    def create(self, order):
        return self.client.make_request("v1/orders/Create", method="POST", data=order)
    
    def create_private_note(self, id:int, note:str): 
        return self.client.make_request(f"v1/orders{id}", data=json.dumps({"PrivateNotes": {note}}))