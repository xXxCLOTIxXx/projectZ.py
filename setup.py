from setuptools import setup, find_packages
from platform import system

with open("README.md", "r") as file:
	long_description = file.read()

link = 'https://github.com/xXxCLOTIxXx/projectZ.py/archive/refs/heads/main.zip'
ver = '1.1.7.2'

setup(
	name = "projectZ.py",
	version = ver,
	url = "https://github.com/xXxCLOTIxXx/projectZ.py",
	download_url = link,
	license = "MIT",
	author = "Xsarz",
	author_email = "xsarzy@gmail.com",
	description = "Library for creating projectZ bots and scripts.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	keywords = [
		"projectZ.py",
		"projectZ",
		"projectZ-py",
		"projectZ-bot",
		"api",
		"python",
		"python3",
		"python3.x",
		"xsarz",
		"official",
		"async",
		"sync",
		"projz"
	],
	install_requires = [
		"websocket-client",
		"requests",
		"aiohttp",
		"aiofiles",
		"ujson",
		"python-magic-bin" if system().lower() == "windows" else "python-magic"
	],
	packages = find_packages()
)
