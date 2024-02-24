# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xaux']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'xaux',
    'version': '0.1.0',
    'description': 'Support tools for Xsuite packages',
    'long_description': '# Xaux\n\nSupport tools for Xsuite packages\n',
    'author': 'Frederik Van der Veken',
    'author_email': 'frederik@cern.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
