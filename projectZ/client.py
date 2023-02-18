
from .utils import exceptions, generator, headers, objects
from .socket import Socket, CallBacks

from json import dumps, loads
from requests import Session
from random import randint
from sys import maxsize
from uuid import UUID
from typing import BinaryIO
from binascii import hexlify
from os import urandom

gen = generator.Generator()

class Client(Socket, CallBacks):
	def __init__(self, deviceId: str = None, proxies: dict = None, socket_debug: bool = False, sock_trace: bool = False, language: str = "en-US", country_code: str = "en", time_zone: int = 180):
		self.api = 'https://api.projz.com'
		self.session = Session()
		self.proxies = None
		self.deviceId = deviceId if deviceId else gen.deviceId()
		self.profile = objects.User()

		self.language = language
		self.country_code = country_code
		self.time_zone = time_zone
		self.header = headers.Headers(deviceId=self.deviceId, time_zone=self.time_zone, country_code=self.country_code, language=self.language)

		Socket.__init__(self, sock_trace=sock_trace, debug=socket_debug)
		CallBacks.__init__(self)


	def get_headers(self, endpoint: str, data = None, content_type: str = 'application/json') -> dict:
		head = self.header.get_persistent_headers()
		head.update(self.header.Headers(sid=self.profile.sid))
		head.update({"Content-Type": content_type} if content_type else {})
		head["HJTRFS"] = gen.signature(path=endpoint, headers=head, body=data or bytes())
		return head

	def set_proxies(self, proxy = None):
		if type(proxy) == type({}):
			self.proxies = proxy
		elif type(proxy) == type(''):
			self.proxies={"http": proxy, "https": proxy}
		elif type(proxy) == type(None):
			self.proxies=None
		else:
			raise exceptions.WrongType(type(proxy))

	def upload_media(self, file: BinaryIO, target: int = 1):
		#TODO
		return None



	def login(self, email: str, password: str):

		data = dumps({
			"authType": 1,
			"email": email,
			"password": password
		})
		endpoint = '/v1/auth/login'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		if response.status_code != 200:return exceptions.CheckException(response.text)
		else:
			self.profile = objects.User(loads(response.text))
			self.profile.User
			self.connect(self.get_headers)
			return self.profile

	def logout(self):

		endpoint = '/v1/auth/logout'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		self.profile = objects.User()
		self.disconnect()
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def join_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def leave_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def get_from_link(self, link: str):
		data = dumps({"link": link})

		endpoint = f"/v1/links/path"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.FromLink(loads(response.text)).FromLink

	def get_link(self, userId: int = None, chatId: int = None, circleId: int = None):
		data = {
			"objectId": 0,
			"objectType": 0,
			"parentId": 0,
			"circleIdForCircleAnnouncement": 0,
			"parentType": 0
		}
		if userId:data['path'] = f"user/{userId}"
		elif chatId: data['path'] = f"chat/{chatId}"
		elif circleId: data['path'] = f"circle/{circleId}"
		else: raise exceptions.WrongType


		data = dumps(data)
		endpoint = '/v1/links/share'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.FromLink(loads(response.text)).FromLink

	def get_my_chats(self, start: int = 0, size: int = 20, type: str = 'managed'):

		endpoint = f'/v1/chat/joined-threads?start={start}&size={size}&type={type}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Thread(loads(response.text)).Thread


	def send_message(self, chatId: int, message: str, message_type: int = 1, reply_to: int = None, poll_id: int = None, dice_id: int = None):

		data = {
			"type": message_type,
			"threadId": chatId,
			"uid": self.profile.uid,
			"seqId": randint(0, maxsize),
			"extensions": {}
		}
		data["content"] = message

		if reply_to: data["extensions"]["replyMessage"] = reply_to
		if poll_id: data["extensions"]["pollId"] = poll_id
		if dice_id: data["extensions"]["diceId"] = dice_id

		resp = self.socket.send(t=1, data=data, threadId=chatId)
		return resp

	def get_verify_code(self, email: str):

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
			"countryCode": self.country_code,
			"suggestedCountryCode": self.country_code.upper(),
			"ignoresDisabled": True,
			"rawDeviceIdThree": gen.generate_device_id_three()
		})

		endpoint = '/v1/auth/request-security-validation'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def register(self, email: str, password: str, code: str, icon: BinaryIO, invitation_code: str = None, nickname: str = 'XsarzyBest', tag_line: str = 'XsarzBot', gender: int = 100, birthday: str = '1990-01-01'):

		data = dumps({
			"authType": 1,
			"purpose": 1,
			"email": email,
			"password": password,
			"securityCode": code,
			"invitationCode": invitation_code or "",
			"nickname": nickname,
			"tagLine": tag_line,
			"icon": self.upload_media(target=1, file=icon),
			"nameCardBackground": None,
			"gender": gender,
			"birthday": birthday,
			"requestToBeReactivated": False,
			"countryCode": self.country_code,
			"suggestedCountryCode": self.country_code.upper(),
			"ignoresDisabled": True,
			"rawDeviceIdThree": gen.generate_device_id_three()
		})

		endpoint = '/v1/auth/register'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def visit(self, userId):

		endpoint = f'/v1/users/profile/{userId}/visit'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def activate_wallet(self, wallet_password: str, code: str, email: str = None):


		data = dumps({
			"authType": 1,
			"identity": email if email else self.profile.email if self.profile.email else exceptions.NotLoggined('You are not authorized'),
			"paymentPassword": wallet_password,
			"securityCode": code
		})

		endpoint = '/biz/v1/wallet/0/activate'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def activate_shop(self):

		endpoint = '/biz/v1/activate-store'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def wallet_info(self):

		endpoint = '/biz/v1/wallet'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def my_nfts(self):

		endpoint = '/biz/v1/nfts/count'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text


	def get_baners(self):

		endpoint = '/v2/banners'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def get_circles(self, type: str = 'recommend', categoryId: int = 0, size: int = 10):

		endpoint = f'/v1/circles?type={type}&categoryId={categoryId}&size={size}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def get_blocked_users(self):

		endpoint = '/v1/users/block-uids'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def get_blogs(self, type: str = 'recommend', size: int = 10):

		endpoint = f'/v1/blogs?type={type}&size={size}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text


	def mark_as_read(self, chatId):

		endpoint = f'/v1/chat/threads/{chatId}/mark-as-read'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def get_chat_threads(self, chatId):

		endpoint=f'/v1/chat/threads/{chatId}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def get_online_chat_members(self, chatId):

		endpoint=f'/v1/chat/threads/{chatId}/online-members'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text


	def get_chat_messages(self, chatId, size: int = 10):

		endpoint=f'/v1/chat/threads/{chatId}/messages?size={size}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text

	def get_circles_blogs(self, circleId: int, type: str = "popular", size: int = 10):

		if type == 'popular': endpoint=f'/v1/circles/{circleId}/popular-blogs?size={size}'
		elif type == 'pinned': endpoint = f'v1/circles/{circleId}/pinned-blogs'

		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text


	def get_circles_info(self, circleId: int):

		endpoint=f'/v1/circles/{circleId}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.get_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.text