# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ca_api_wrapper',
 'ca_api_wrapper.api',
 'ca_api_wrapper.custom_models',
 'ca_api_wrapper.custom_models.orders']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=2.2.1,<3.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'ca-api-wrapper',
    'version': '2.0.6',
    'description': '',
    'long_description': '[![Documentation Status](https://readthedocs.org/projects/rithum-api-wrapper/badge/?version=latest)](https://rithum-api-wrapper.readthedocs.io/en/latest/?badge=latest)\n\n# CA API Wrapper\n\nThe `ca_api_wrapper` is a Python package that simplifies interacting with the ChannelAdvisor API. It provides a straightforward, object-oriented approach to accessing ChannelAdvisor\'s features, such as managing products, orders, and exports, making it easier for developers to integrate ChannelAdvisor services into their applications.\n\n## Features\n\n- **Easy Authentication**: Simplify the process of authenticating with the ChannelAdvisor API.\n- **Product Management**: Easily list, retrieve, and update product information.\n- **Order Processing**: Fetch and update orders with minimal hassle.\n- **Export Utilities**: Access export functionalities provided by ChannelAdvisor.\n- **Error Handling**: Robust error handling to gracefully manage API exceptions.\n\n## Installation\n\nInstall `ca_api_wrapper` using pip:\n\n```bash\npip install ca_api_wrapper\n```\n### Quick start\nHere\'s a quick example to get you started with the ca_api_wrapper:\n```py\n\nfrom ca_api_wrapper.api.client_registry import ClientsFactory\n\n# User provides their own credentials\naccess_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX-1234"\ndefault_profile_id = 12345678\nsecondary_profile_id = 12345679 \n\nfactory = ClientsFactory(access_token, default_profile_id, secondary_profile_id)\nproduct_client = factory.product_client\n\nresponse = product_client.products.get_by_id(11111111)\n```\n\n',
    'author': 'Vick Mu',
    'author_email': 'arbi3400@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
