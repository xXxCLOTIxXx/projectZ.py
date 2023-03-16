import projectZ
import asyncio


client = projectZ.AsyncClient()

async def main():
	await client.login(email='email', password='password')

@client.event("on_text_message")
async def on_text_message(data):
	msg = data.content
	print(f'new message!\n{msg}\n')

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
	loop.run_forever()