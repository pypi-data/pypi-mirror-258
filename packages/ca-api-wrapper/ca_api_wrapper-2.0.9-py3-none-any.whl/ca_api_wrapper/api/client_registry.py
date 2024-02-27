from .client import ChannelAdvisorClient
from .products import ProductClient
from .orders import OrderClient
from .exports import ProductExportClient

class ClientsFactory:
    def __init__(self, access_token: str, default_profile_id: str, secondary_profile_id: str = None, base_url: str = "https://api.channeladvisor.com") -> None:
        self.access_token = access_token
        self.default_profile_id = default_profile_id
        self.secondary_profile_id = secondary_profile_id
        self.base_url = base_url
        
        self._base_client = ChannelAdvisorClient(access_token, default_profile_id, secondary_profile_id, base_url)

    @property
    def product_client(self):
        """Returns an instance of ProductClient using the base client configuration."""
        return ProductClient(self._base_client)

    @property
    def order_client(self):
        """Returns an instance of OrderClient using the base client configuration."""
        return OrderClient(self._base_client)

    @property
    def export_client(self):
        """Returns an instance of ExportClient using the base client configuration."""
        return ProductExportClient(self._base_client)

