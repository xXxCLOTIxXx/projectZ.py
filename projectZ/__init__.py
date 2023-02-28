"""
Author: Xsarz

Enjoy using!
"""

from .utils import exceptions, generator, headers, objects
from .client import Client
from .socket import Socket

from os import system as s
from colored import fore
from json import loads
from requests import get

__title__ = 'projectZ.py'
__author__ = 'Xsarz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Xsarz'
__version__ = '1.1.4.1.1'


__newest__ = loads(get("https://pypi.org/pypi/projectZ.py/json").text)["info"]["version"]
if __version__ != __newest__:
	s('cls || clear')
	print(fore.ORANGE_1, f'{__title__} made by {__author__}\nPlease update the library. Your version: {__version__}  A new version:{__newest__}', fore.WHITE)