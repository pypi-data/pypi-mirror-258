from .client import ChannelAdvisorClient
from .products import ProductClient
from .orders import OrderClient
from .exports import ProductExportClient

from typing import Union


class ClientFactory:
    @staticmethod
    def create_clients(access_token, default_profile_id, secondary_profile_id=None, base_url="https://api.channeladvisor.com") -> Union[ChannelAdvisorClient, ProductClient, OrderClient, ProductExportClient]:
        base_client = ChannelAdvisorClient(
            access_token, default_profile_id, secondary_profile_id, base_url)
        return {
            '_base': base_client,
            'product': ProductClient(base_client),
            'order': OrderClient(base_client),
            'export': ProductExportClient(base_client)
        }
