<table align="center">
	<tr> <th colspan="3">Library Information</th> </tr>
	<tr>
		<td>
			<a href='https://projectzpy.readthedocs.io/en/latest/'><img src="https://pbs.twimg.com/profile_images/525686734760067072/OhsWgbsr_400x400.png" height="30px">
			 Library Documentation</a>
		</td>
		<td>
			<a href='https://github.com/xXxCLOTIxXx/projectZ.py'><img src="https://upload.wikimedia.org/wikipedia/commons/9/91/Octicons-mark-github.svg" height="30px">
			 GitHub</a>
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
<p align="center">Library for working with projectZ servers, below you will see code examples, for more examples see the documentation or the examples folder</p>
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