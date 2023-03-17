import projectZ
import asyncio
from aiofiles import open as async_open

email = 'test@gmail.com' #account email
password = 't4tdej6!3r5E' #password for account
nick = 'projectZ_LIB' #nickname
icon = 'icon.png' #avatar image path

async def main():
	client = projectZ.AsyncClient()
	try:
		await client.send_verify_code(email=email)
		code = input(f'Confirmation code sent to the email "{email}"\nCode >> ')
		await client.register(email=email, password=password, code=code, icon=await async_open(icon, "rb"), nickname=nick)
		print(f"Account created!\nEmail: {email}\nPassword: {password}")
	except Exception as error:
		print(f"An error has occurred:\n{error}")


if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())