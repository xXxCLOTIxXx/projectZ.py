<body>
	<p align="center">
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/releases"><img src="https://img.shields.io/github/v/release/xXxCLOTIxXx/projectZ.py" alt="GitHub release" />
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="licence" /></a>
	    <a href="https://pypi.org/project/projectZ/"><img src="https://img.shields.io/pypi/v/projectZ" alt="pypi" /></a>
	    <a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md"><img src="https://img.shields.io/website?down_message=failing&label=docs&up_color=green&up_message=passing&url=https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/docs/main.md" alt="docs" /></a>
	</p>
	<div align="center">
		<a href="https://github.com/xXxCLOTIxXx/xXxCLOTIxXx/blob/main/sponsor.md">
			<img src="https://img.shields.io/static/v1?style=for-the-badge&label=Sponsor project&message=%E2%9D%A4&color=ff69b4" alt="Sponsor project"/>
		</a>
	</div>
	<table align="center">
		</tr>
		<tr> <th colspan="3">More info</th> </tr>
		<tr>
			<td>
				<a href="https://t.me/DxsarzUnion"><img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" height="30px">
				 Telegram Channel</a>
			</td>
			<td>
				<a href="https://www.youtube.com/channel/UCNKEgQmAvt6dD7jeMLpte9Q"><img src="https://upload.wikimedia.org/wikipedia/commons/0/09/YouTube_full-color_icon_%282017%29.svg" height="30px">
				 YouTube channel</a>
			</td>
			<td>
				<a href="https://discord.gg/GtpUnsHHT4"><img src="https://www.svgrepo.com/show/353655/discord-icon.svg" height="30px">
				 Discord Server</a>
			</td>
		</tr>
	</table>
<h1 align="center">projectZ.py</h1>
		    
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
