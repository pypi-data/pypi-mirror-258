# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['etb_env']

package_data = \
{'': ['*']}

install_requires = \
['python-dotenv>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'etb-env',
    'version': '0.2.1',
    'description': 'A little class for getting env variables',
    'long_description': '',
    'author': 'Tate Button',
    'author_email': 'yg3bpwn0or679hau8fxi@duck.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
