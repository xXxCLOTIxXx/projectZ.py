<body>
	<table align="center">
		<tr> <th colspan="3">Library Information</th> </tr>
		<tr>
			<td>
				<a href='https://pypi.org/project/projectZ/'><img src="https://raw.githubusercontent.com/github/explore/666de02829613e0244e9441b114edb85781e972c/topics/pip/pip.png" height="60px">
				 Library in pypi</a>
			</td>
	</table>
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
