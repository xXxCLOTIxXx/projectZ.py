<body>
	<p align="center">
	    <a href="#"><img src="https://github.com/xXxCLOTIxXx/projectZ.py/blob/dev/docs/res/logo.png"/></a>
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/releases"><img src="https://img.shields.io/github/v/release/xXxCLOTIxXx/projectZ.py" alt="GitHub release" />
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
	    <a href="https://pypi.org/project/projectZ/"><img src="https://img.shields.io/pypi/v/projectZ" alt="pypi" /></a>
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md" alt="docs" /></a>
	</p>
	<div align="center">
		<a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/sponsor.md">
			<img src="https://img.shields.io/static/v1?style=for-the-badge&label=Sponsor project&message=%E2%9D%A4&color=ff69b4" alt="Sponsor project"/>
		</a>
		<hr>
		<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2000&pause=2000&color=F79B1F&random=false&width=200&lines=Installation"/>
	</div>
		    
```bash
pip install projectZ
```
<h4 align="center">or</h4>
		    
```bash
pip install git+https://github.com/xXxCLOTIxXx/projectZ.py.git
```
<p align="center">Library for working with projectZ servers, below you will see code examples</p>
<h1 align="center">Login example</h1>

```python
import projectZ

client = projectZ.Client()
client.login(email='email', password='password')
```

<h1 align="center">Async login example</h1>

```python
import projectZ
import asyncio


client = projectZ.AsyncClient()
async def main():
	await client.login(email='email', password='password')

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
```

</body>
