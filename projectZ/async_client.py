from .utils import exceptions, objects
from .utils.generator import Generator
from .utils.headers import Headers
from .async_socket import AsyncSocket, AsyncCallBacks

from json import dumps, loads
from sys import maxsize
from random import randint
from aiohttp import ClientSession, MultipartWriter
from asyncio import get_event_loop, new_event_loop, create_task
from magic import from_buffer

from aiofiles.threadpool.binary import AsyncBufferedReader

gen = Generator()

class AsyncClient(AsyncSocket, AsyncCallBacks):
	def __init__(self, deviceId: str = None, socket_debug: bool = False, language: str = "en-US", country_code: str = "en", time_zone: int = 180):
		self.api = 'https://api.projz.com'
		self.deviceId = deviceId if deviceId else gen.deviceId()
		self.profile = objects.User()
		self.language = language
		self.country_code = country_code
		self.time_zone = time_zone

		self.session = ClientSession()

		AsyncSocket.__init__(self, headers=self.parse_headers, debug=socket_debug)
		AsyncCallBacks.__init__(self)


	def __del__(self):
		try:
			loop = get_event_loop()
			loop.run_until_complete(self.close_session())
		except RuntimeError:
			loop = new_event_loop()
			loop.run_until_complete(self.close_session())

	async def close_session(self):
		if not self.session.closed: await self.session.close()



	def parse_headers(self, endpoint: str, data = None, content_type: str = 'application/json') -> dict:
		h = Headers(deviceId=self.deviceId, sid=self.profile.sid, time_zone=self.time_zone, country_code=self.country_code, language=self.language)
		head = h.get_persistent_headers()
		head.update(h.Headers())
		head.update({"Content-Type": content_type} if content_type else {})
		head["HJTRFS"] = gen.signature(path=endpoint, headers=head, body=data or bytes())
		return head


	async def upload_media(self, file: AsyncBufferedReader, target: int = 1):
		#TODO 
		duration = 0
		content = await file.read()
		writer = MultipartWriter()
		part = writer.append(content, {"Content-Type": from_buffer(content, mime=True)})
		part.set_content_disposition("form-data", name="media", filename=file.name)

		endpoint = f"/v1/media/upload?target={target}&duration={duration}"

		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, content_type=f"multipart/form-data; boundary={writer.boundary}"), data=writer) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def login(self, email: str, password: str):

		data = dumps({
			"authType": 1,
			"email": email,
			"password": password
		})
		endpoint = '/v1/auth/login'

		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			if response.status != 200: return exceptions.CheckException(await response.text())
			else:
				self.profile = objects.User(loads(await response.text()))
				await self.connect()
				return self.profile


	async def logout(self):
		endpoint = '/v1/auth/logout'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			if response.status != 200: return exceptions.CheckException(await response.text())
			else:
				self.profile = objects.User()
				await self.disconnect()
				return response.status

	async def Online(self):
		#TODO 
		if self.online_loop_active: return
		self.online_loop_active = create_task(self.online_loop())
		return self.online_loop_active

	async def Offline(self):
		if self.online_loop_active:
			self.online_loop_active.cancel()
			self.online_loop_active = None
		return self.online_loop_active


	async def join_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status



	async def leave_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def get_from_link(self, link: str):

		data = dumps({"link": link})
		endpoint = f"/v1/links/path"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.FromLink(loads(await response.text()))


	async def get_link(self, userId: int):

		data = dumps({
			"objectId": 0,
			"objectType": 0,
			"parentId": 0,
			"path": f"user/{userId}",
			"circleIdForCircleAnnouncement": 0,
			"parentType": 0
		})

		endpoint = '/v1/links/share'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.FromLink(loads(await response.text()))

	async def get_my_chats(self, start: int = 0, size: int = 20, type: str = 'managed'):

		endpoint = f'/v1/chat/joined-threads?start={start}&size={size}&type={type}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else  objects.Thread(loads(await response.text()))


	async def send_message(self, chatId: int, message: str, message_type: int = 1, reply_to: int = None, poll_id: int = None, dice_id: int = None):
		#TODO 
		seqId = randint(0, maxsize)
		data = {
			"type": message_type,
			"threadId": chatId,
			"uid": self.profile.uid,
			"seqId": seqId,
			"extensions": {}
		}
		data["content"] = message
		if reply_to: data["extensions"]["replyMessage"] = reply_to
		if poll_id: data["extensions"]["pollId"] = poll_id
		if dice_id: data["extensions"]["diceId"] = dice_id

		resp = await self.send(t=1, data=data, threadId=chatId, seqId=seqId)
		return resp
