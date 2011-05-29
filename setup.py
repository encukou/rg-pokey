#! /usr/bin/env python
# Encoding: UTF-8

from setuptools import setup, find_packages

__copyright__ = "Copyright 2009-2011, Petr Viktorin"
__license__ = "MIT"
__version__ = '0.1'
__author__ = 'Petr "En-Cu-Kou" Viktorin'
__email__ = 'encukou@gmail.com'

setup(
    name='regeneration-pokey',
    version=__version__,
    description=u'Pokémon battle mechanics',
    author=__author__,
    author_email=__email__,
    install_requires=[
            "pyyaml>=3.0",
            "pokedex",
            "regeneration-battle",
        ],
    setup_requires=[
            'pytest>=2.0',
        ],
    packages=find_packages(),
    namespace_packages=['regeneration'],

    include_package_data=True,
    package_data={},
)
