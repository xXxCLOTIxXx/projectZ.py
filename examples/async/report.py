import projectZ
import asyncio
from aiofiles import open as async_open

email =  'email@gmail.com' #account email
password = 'password' #password for account
userId = #int userId
message = "text" #message for report

async def main():
	client = projectZ.AsyncClient()
	media = await async_open('image.png', "rb") #image
	try:
		await client.login(email=email, password=password)
		await client.report(userId=userId, message=message, images=media)
	except Exception as error:
		print(f"An error has occurred:\n{error}")


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())