# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shazamio_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'shazamio-core',
    'version': '1.0.6',
    'description': '',
    'long_description': '# shazamio-core',
    'author': 'dotX12',
    'author_email': 'dev@shitposting.team',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
