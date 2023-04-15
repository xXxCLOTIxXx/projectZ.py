from .utils import exceptions, objects
from .utils.generator import Generator
from .utils.headers import Headers
from .async_socket import AsyncSocket, AsyncCallBacks

from json import dumps, loads
from sys import maxsize
from random import randint
from aiohttp import ClientSession, MultipartWriter
from asyncio import get_event_loop, new_event_loop, create_task
from io import BytesIO
from aiofiles.threadpool.binary import AsyncBufferedReader
from typing import Union, Optional

gen = Generator()

class AsyncClient(AsyncSocket, AsyncCallBacks):
	def __init__(self, deviceId: str = None, socket_debug: bool = False, run_socket: bool = True, language: str = "en-US", country_code: str = "en", time_zone: int = 180):
		self.api = 'https://api.projz.com'
		self.deviceId = deviceId if deviceId else gen.deviceId()
		self.profile = objects.User()
		self.language = language
		self.country_code = country_code
		self.time_zone = time_zone
		self.run_socket = run_socket

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


	async def upload_media(self, file: AsyncBufferedReader, fileType: str, target: int = 1, returnType: str = 'object', duration: int = 0):

		if fileType == "audio":
			t = "audio/aac"
		elif fileType == "image":
			t = "image/jpg"
		else: raise exceptions.WrongType(fileType)

		file_content = await file.read()
		content = BytesIO()
		writer = MultipartWriter()
		part = writer.append(file_content, {"Content-Type": t})
		part.set_content_disposition("form-data", name="media", filename=file.name)
		await writer.write(objects.CopyToBufferWriter(content))
		endpoint = f"/v1/media/upload?target={target}&duration={duration}"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, content_type=f"multipart/form-data; boundary={writer.boundary}", data=content.getvalue()), data=content.getvalue()) as response:
			if response.status != 200:return exceptions.CheckException(await response.text())
			else:
				return objects.Media(loads(await response.text())) if returnType == 'object' else loads(await response.text())


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
				if self.run_socket:await self.connect()
				return self.profile


	async def logout(self):
		endpoint = '/v1/auth/logout'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			if response.status != 200: return exceptions.CheckException(await response.text())
			else:
				self.profile = objects.User()
				if self.run_socket:await self.disconnect()
				return response.status

	async def Online(self):
		if not self.run_socket:return
		if self.online_loop_active: return
		self.online_loop_active = create_task(self.online_loop())
		return self.online_loop_active

	async def Offline(self):
		if not self.run_socket:return
		if self.online_loop_active:
			self.online_loop_active.cancel()
			self.online_loop_active = None
		return self.online_loop_active


	async def join_chat(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}/members'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status



	async def leave_chat(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}/members'
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def get_from_link(self, link: str):

		data = dumps({"link": link})
		endpoint = f"/v1/links/path"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.FromLink(loads(await response.text()))


	async def get_link(self, userId: int = None, chatId: int = None, circleId: int = None, blogId: int = None):

		data = {
			"objectId": 0,
			"objectType": 0,
			"parentId": 0,
			"circleIdForCircleAnnouncement": 0,
			"parentType": 0
		}

		if userId:
			data["path"] = f"user/{userId}"

		elif chatId:
			data["path"] = f"chat/{chatId}"

		elif circleId:
			data["objectType"] = 5
			data["objectId"] = circleId
			data["path"] = f"circle/{circleId}"

		elif blogId:
			data["path"] = f"blog/{blogId}"

		else:
			raise exceptions.WrongType(fileType)

		data = dumps(data)

		endpoint = '/v1/links/share'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.FromLink(loads(await response.text()))

	async def get_my_chats(self, start: int = 0, size: int = 20, type: str = 'managed'):

		endpoint = f'/v1/chat/joined-threads?start={start}&size={size}&type={type}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else  objects.Thread(loads(await response.text()))


	async def send_message(self, chatId: int, message: str = None, file: AsyncBufferedReader = None, fileType: str = None, file_duration: int = None, message_type: int = 1, replyTo: int = None, pollId: int = None, diceId: int = None): 
		if not self.run_socket:return
		data = {
			"threadId": chatId,
			"uid": self.profile.uid,
			"seqId": randint(0, maxsize),
			"extensions": {}
		}
		if message:
			data["content"]=message
			data["type"]=message_type
		elif file:
			data["type"]= 2 if fileType == "image" else 6
			data["media"] = await self.upload_media(file=file, fileType=fileType, target= 8 if fileType == "image" else 10, returnType='dict', duration=file_duration*1000 if file_duration else 0)
		else:
			raise exceptions.WrongType('Specify the "message" or "file" argument')

		if replyTo: data["extensions"]["replyMessageId"] = replyTo
		if pollId: data["extensions"]["pollId"] = pollId
		if diceId: data["extensions"]["diceId"] = diceId

		resp = await self.send(t=1, data=data, threadId=chatId)
		return resp



	async def send_verify_code(self, email: str, country_code: str = None):
		data = dumps({
			"authType": 1,
			"purpose": 1,
			"email": email,
			"password": "",
			"phoneNumber": "",
			"securityCode": "",
			"invitationCode": "",
			"secret": "",
			"gender": 0,
			"birthday": "1990-01-01",
			"requestToBeReactivated": False,
			"countryCode": country_code if country_code else self.country_code,
			"suggestedCountryCode": country_code.upper() if country_code else self.country_code.upper(),
			"ignoresDisabled": True,
			"rawDeviceIdThree": gen.generate_device_id_three()
		})
		
		endpoint = '/v1/auth/request-security-validation'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status

	async def register(self, email: str, password: str, code: str, icon: Union[AsyncBufferedReader, objects.Media], country_code: str = None, invitation_code: str = None, nickname: str = 'XsarzyBest', tag_line: str = 'projectZ', gender: int = 100, birthday: str = '1990-01-01'):
		data = dumps({
			"authType": 1,
			"purpose": 1,
			"email": email,
			"password": password,
			"securityCode": code,
			"invitationCode": invitation_code or "",
			"nickname": nickname,
			"tagLine": tag_line,
			"icon": icon.json if isinstance(icon, objects.Media) else await self.upload_media(icon, returnType='dict', fileType="image"),
			"nameCardBackground": None,
			"gender": gender,
			"birthday": birthday,
			"requestToBeReactivated": False,
			"countryCode": country_code if country_code else self.country_code,
			"suggestedCountryCode": country_code.upper() if country_code else self.country_code.upper(),
			"ignoresDisabled": True,
			"rawDeviceIdThree": gen.generate_device_id_three()
		})

		endpoint = '/v1/auth/register'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def visit(self, userId):

		endpoint = f'/v1/users/profile/{userId}/visit'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def add_to_favorites(self, userId: Union[list, int]):

		userIds = userId if isinstance(userId, list) else [userId]
		data = dumps({"targetUids": userIds})
		endpoint = '/v1/users/membership/favorites'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def report(self, userId: int, message: str, images: Union[AsyncBufferedReader, list[AsyncBufferedReader]], flagType: int = 100):

		media = list()
		if isinstance(images, AsyncBufferedReader):images=[images]
		elif isinstance(images, list):pass
		else:raise exceptions.WrongType()
		data = {
			"objectId": userId,
			"objectType": 4,
			"flagType": flagType,
			"message": message,
		}
		for image in images:
			media.append(await self.upload_media(image, returnType='dict', fileType="image"))
		data["mediaList"] = media


		data = dumps(data)
		endpoint = f'/v1/flags'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def delete_message(self, chatId: int, messageId: int):

		endpoint = f'/v1/chat/threads/{chatId}/messages/{messageId}'
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status

	async def kick(self, chatId: int, userId: int, denyEntry: bool = False, removeContent: bool = False):
		
		endpoint = f"/v1/chat/threads/{chatId}/members/{userId}?block={str(denyEntry).lower()}&removeContent={str(removeContent).lower()}"
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def pin_chat(self, chatId):

		endpoint = f'/v1/chat/threads/{chatId}/pin'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status

	async def apply_bubble(self, chatId: int, bubbleColor: str):

		data = dumps({"threadId": chatId, "bubbleColor": bubbleColor})
		endpoint = f'/v1/chat/apply-bubble'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def invite_to_co_host(self, chatId: int, userId: Union[list, int]):
		#TODO
		if isinstance(userId, int): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else:raise exceptions.WrongType('Specify the "message" or "file" argument')
		data = dumps({"coHostUids": userIds})
		endpoint = f"/v1/chat/threads/{chatId}/invite-co-host"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def invite_to_host(self, chatId: int, userId: int):
		#TODO
		endpoint = f"/v1/chat/threads/{chatId}/invite-host/{userId}"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def accept_co_host(self, chatId: int):

		endpoint = f"/v1/chat/threads/{chatId}/accept-as-co-host"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def accept_host(self, chatId: int):
		
		endpoint = f"/v1/chat/threads/{chatId}/accept-as-host"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def auto_offline(self, chatId: int, switch: bool = False):

		endpoint = f"/v1/chat/threads/{chatId}/auto-offline/{'disable' if switch == False else 'enable'}"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def check_in(self):
		endpoint = f"/v1/users/check-in"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			response = exceptions.CheckException(await response.text()) if response.status != 200 else objects.OrderInfo(loads(await response.text()))
		await self.claim_transfer_orders(orderId=response.orderId)

		return response

	async def claim_transfer_orders(self, orderId: int):

		endpoint = f"/biz/v3/transfer-orders/{orderId}/claim"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())#response.status


	async def claim_gift_boxes(self, orderId: int):
		endpoint = f"/v1/gift-boxes/{orderId}/claim"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def get_transfer_order_info(self, orderId: int):

		endpoint = f"/biz/v1/transfer-orders/{orderId}"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())

	async def send_coins(self, wallet_password: int, userId: int, amount: int, title: str = "All the best!"):

		data = dumps({
			"toObjectId": userId,
			"amount": f"{amount}000000000000000000",
			"paymentPassword": str(wallet_password),
			"toObjectType": 4,
			"currencyType": 100,
			"title": title
		})

		endpoint = f"/biz/v1/gift-boxes"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def online_chat_status(self, chatId: int, online: bool = True):

		data = dumps({"partyOnlineStatus": 1 if online else 2})
		endpoint = f"/v1/chat/threads/{chatId}/party-online-status"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def get_user_info(self, userId: int):

		endpoint = f'/v1/users/profile/{userId}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.UserProfile(loads(await response.text()))



	async def get_circles(self, type: str = 'recommend', categoryId: int = 0, size: int = 10):

		endpoint = f'/v1/circles?type={type}&categoryId={categoryId}&size={size}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.CirclesList(loads(await response.text()))


	async def get_blocked_users(self):

		endpoint = '/v1/users/block-uids'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.BlockedUsers(loads(await response.text()))


	async def get_blogs(self, type: str = 'recommend', size: int = 10):

		endpoint = f'/v1/blogs?type={type}&size={size}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Blogs(loads(await response.text()))


	async def mark_as_read(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}/mark-as-read'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status

	async def get_chat_threads(self, chatId: int):

		endpoint=f'/v1/chat/threads/{chatId}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())

	async def get_online_chat_members(self, chatId: int):

		endpoint=f'/v1/chat/threads/{chatId}/online-members'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def get_chat_messages(self, chatId: int, size: int = 10):

		endpoint=f'/v1/chat/threads/{chatId}/messages?size={size}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())

	async def get_mention_candidates(self, chatId: int, size: int = 10, queryWord: str = ''):
		
		endpoint = f'/v1/chat/threads/{chatId}/mention-candidates?size={size}&queryWord={queryWord}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.MentionCandidates(loads(await response.text()))


	async def get_comments(self, userId: int, type: int = 4, replyId: int= 0, size: int = 30, onlyPinned: int = 0):

		endpoint = f'/v1/comments?parentId={userId}&parentType={type}&replyId={replyId}&size={size}&onlyPinned={onlyPinned}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Comments(loads(await response.text()))


	async def block(self, userId: int):

		endpoint = f'/v1/users/block/{userId}'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def unblock(self, userId: int):

		endpoint = f'/v1/users/block/{userId}'
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def accept_chat_invitation(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}/accept-invitation'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status

	async def join_circle(self, circleId):
		data = dumps({"joinMethod": 1})

		endpoint = f'/v1/circles/{circleId}/members'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def leave_circle(self, circleId):

		endpoint = f'/v1/circles/{circleId}/members'
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def get_circle_info(self, circleId: int):

		endpoint = f'/v1/circles/{circleId}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Circle(loads(await response.text()))


	async def get_chat_info(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.ChatInfo(loads(await response.text()))


	async def follow(self, userId: int):

		endpoint = f'/v1/users/membership/{userId}'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def unfollow(self, userId: int):

		endpoint = f'/v1/users/membership/{userId}'
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def like(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339):

		data = {
			"createdTime": 0,
			"stickerId": stickerId,
			"count": 0,
			"justAddTimeMs": 0
		}

		if commentId:
			data['objectType'] = 3
			data['objectId'] = commentId

		elif blogId:
			data['objectType'] = 2
			data['objectId'] = blogId

		else:
			raise exceptions.WrongType()

		data = dumps(data)
		endpoint = f'/v1/reactions'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def unlike(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339):

		if commentId:
			endpoint = f'/v1/reactions?objectId={commentId}&objectType=3&stickerId={stickerId}'
		elif blogId:
			endpoint = f'/v1/reactions?objectId={blogId}&objectType=2&stickerId={stickerId}'
		else:
			raise exceptions.WrongType()

		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def invite_to_chat(self, userId: Union[int, list], chatId: int):
		if isinstance(userId, int): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else:raise exceptions.WrongType()

		data = dumps({"invitedUids": userIds})

		endpoint = f'/v1/chat/threads/{chatId}/members-invite'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def get_my_invitation_code(self):

		endpoint = f'/v1/users/multi-invitation-code'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.invitationCode(loads(await response.text()))


	async def get_circles_members(self, circleId: int, size: int = 30, type :str = 'normal', pageToken: str = None):

		endpoint = f'/v1/circles/{circleId}/members?type={type}&size={size}&isExcludeManger=false{f"&pageToken={pageToken}" if pageToken else ""}'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.CirclesMembers(loads(await response.text()))



	async def get_baners(self):

		endpoint = '/v2/banners'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Baners(loads(await response.text()))


	async def activate_wallet(self, wallet_password: str, code: str, email: str = None):

		data = dumps({
			"authType": 1,
			"identity": email if email else self.profile.email if self.profile.email else exceptions.NotLoggined('You are not authorized'),
			"paymentPassword": wallet_password,
			"securityCode": code
		})

		endpoint = '/biz/v1/wallet/0/activate'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status

	async def activate_shop(self):

		endpoint = '/biz/v1/activate-store'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.ActivateShop(loads(await response.text()))

	async def wallet_info(self):

		endpoint = '/biz/v1/wallet'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.WalletInfo(loads(await response.text()))


	async def my_nfts(self):

		endpoint = '/biz/v1/nfts/count'
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Nfts(loads(await response.text()))



	async def comment(self, message: str, userId: int = None, blogId: int = None, replyId: dict = None):

		data = {
			"commentId": 0,
			"status":1,
			"parentId": userId,
			"replyId": 0,
			"circleId": 0,
			"uid": 0,
			"content": message,
			"mediaList": [],
			"commentType": 1,
			"subComments": [],
			"subCommentsCount": 0,
			"isPinned": False
		}

		if userId:
			data['parentType'] = 4

		elif blogId:
			data['parentType'] = 2

		else:
			raise exceptions.WrongType()


		if replyId:
			data['replyId'] = replyId['commentId']
			data['extensions'] = {"replyToUid": replyId['userId'], "contentStatus": 1}

		data = dumps(data)
		endpoint = f'/v1/comments'
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Comments(loads(await response.text()))



	async def get_alerts(groupId: int = 3, size: int = 30):

		endpoint = f"/v1/alerts?groupId={groupId}&size={size}"
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())

	async def get_moods(self):
		endpoint = f"/v1/moods"
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())



	async def change_password(self, oldPassword: str, newPassword: str):

		data = dumps({"oldPassword": oldPassword, "newPassword": newPassword})
		endpoint="/v1/auth/change-password"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def get_message_info(self, chatId: int, messageId: int):

		endpoint = f"/v1/chat/threads/{chatId}/messages/{messageId}"
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def delete_chat(self, chatId: int):

		endpoint = f"/v1/chat/threads/{chatId}"
		async with self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else response.status


	async def qivotes_chat(self, chatId: int):

		data = dumps({
			"uid": 0,
			"objectId": {chatId},
			"objectType": 1,
			"timezone": self.time_zone,
			"votedCount": 1,
			"votedDate": 0,
			"createdTime": 0,
			"lastVoteTime": 0
		})
		endpoint = "/v1/qivotes"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def get_user_tasks(self):

		endpoint = f"/v2/user-tasks"
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())


	async def get_my_gifts(self, size: int = 60):
		endpoint = f"/biz/v2/transfer-orders?size={size}"
		async with self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else objects.Gifts(loads(await response.text()))


	async def gift_withdrawn(self, orderId):

		endpoint = f"/biz/v1/gift-boxes/{orderId}/withdrawn"
		async with self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint)) as response:
			return exceptions.CheckException(await response.text()) if response.status != 200 else loads(await response.text())
