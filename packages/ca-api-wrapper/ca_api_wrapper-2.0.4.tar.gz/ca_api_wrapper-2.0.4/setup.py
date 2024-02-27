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
    'version': '2.0.4',
    'description': '',
    'long_description': None,
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
