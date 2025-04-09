<body>
	<p align="center">
	    <a href="#"><img src="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/res/logo.png"/></a>
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/releases"><img src="https://img.shields.io/github/v/release/xXxCLOTIxXx/projectZ.py" alt="GitHub release" />
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
	    <a href="https://pypi.org/project/projectZ/"><img src="https://img.shields.io/pypi/v/projectZ" alt="pypi" /></a>
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md" alt="docs" /></a>
	<img src="https://img.shields.io/pypi/dm/projectz" />
	</p>
	<div align="center">
		<a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/sponsor.md">
			<img src="https://img.shields.io/badge/%D0%A1%D0%BF%D0%BE%D0%BD%D1%81%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D1%82%D1%8C-Donate-F79B1F?style=for-the-badge&logo=github&logoColor=FF69B4&color=FF69B4" alt="Sponsor project"/>
		</a>
		<h1>This social network has ceased to exist, lol.</h1>
		<hr>
		<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2000&pause=2000&color=F79B1F&random=false&width=200&repeat=false&lines=Installation" alt="Installation"/>
	<p>Git</p>
	
```bash
pip install git+https://github.com/xXxCLOTIxXx/projectZ.py.git
```
<p>pypi</p>

```bash
pip install projectZ
```
<hr><br>
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=28&duration=2000&pause=2000&color=F79B1F&repeat=false&random=false&width=90&lines=Using" alt="Using"/>
</div>
<h4 align="center">Login example</h4>

```python
import projectZ

client = projectZ.Client()
client.login(email='email', password='password')
```


```python
import projectZ

client = projectZ.Client()
client.login(email='email', password='password')


@client.event("on_text_message")
def message(data):
    print(data.json)
```

<br><br>
<h4 align="center">Async login example</h4>

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
<hr><br>
<div align="center">
<a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md">
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=14&duration=1&pause=31&color=3DACF7&random=false&width=195&lines=Read+the+documentation" alt="=Read the documentation"/>
</a>
</div>
</body>
