from .client import ChannelAdvisorClient

class OrderClient:
    def __init__(self, client: ChannelAdvisorClient):
        self.client = client

    def list(self):
        return self.client.make_request("v1/orders")

    def get_by_id(self, id):
        return self.client.make_request(f"v1/Orders({id})?$expand=Items")
    
    def create(self, order):
        return self.client.make_request("v1/orders/Create", method="POST", data=order)