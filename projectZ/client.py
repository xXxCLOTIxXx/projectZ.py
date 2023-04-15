
from .utils import exceptions, generator, headers, objects
from .socket import Socket, CallBacks

from json import dumps, loads
from requests import Session
from random import randint
from sys import maxsize
from uuid import UUID
from typing import BinaryIO, Union
from binascii import hexlify
from os import urandom
from threading import Thread
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

		Socket.__init__(self, headers=self.parse_headers, sock_trace=sock_trace, debug=socket_debug)
		CallBacks.__init__(self)


	def parse_headers(self, endpoint: str, data = None, content_type: str = 'application/json') -> dict:
		h = headers.Headers(deviceId=self.deviceId, sid=self.profile.sid, time_zone=self.time_zone, country_code=self.country_code, language=self.language)
		head = h.get_persistent_headers()
		head.update(h.Headers())
		head.update({"Content-Type": content_type} if content_type else {})
		head["HJTRFS"] = gen.signature(path=endpoint, headers=head, body=data or bytes())
		return head

	def set_proxies(self, proxy: Union[dict, str, None] = None):
		if isinstance(proxy, dict):
			self.proxies = proxy
		elif isinstance(proxy, str):
			self.proxies={"http": proxy, "https": proxy}
		elif proxy is None:
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
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		if response.status_code != 200:return exceptions.CheckException(response.text)
		else:
			self.profile = objects.User(loads(response.text))
			self.connect()
			return self.profile

	def logout(self):

		endpoint = '/v1/auth/logout'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		self.profile = objects.User()
		self.disconnect()
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def Online(self):
		if self.online_loop_active: return
		
		self.online_loop_active = True
		Thread(target=self.online_loop).start()
		return self.online_loop_active

	def Offline(self):
		self.online_loop_active = False
		return self.online_loop_active

	def join_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def leave_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def get_from_link(self, link: str):
		data = dumps({"link": link})

		endpoint = f"/v1/links/path"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.FromLink(loads(response.text))



	def get_link(self, userId: int = None, chatId: int = None, circleId: int = None, blogId: int = None):

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
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.FromLink(loads(response.text))

	def get_my_chats(self, start: int = 0, size: int = 20, type: str = 'managed'):

		endpoint = f'/v1/chat/joined-threads?start={start}&size={size}&type={type}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Thread(loads(response.text))


	def send_message(self, chatId: int, message: str, message_type: int = 1, replyTo: int = None, pollId: int = None, diceId: int = None):

		data = {
			"type": message_type,
			"threadId": chatId,
			"uid": self.profile.uid,
			"seqId": randint(0, maxsize),
			"extensions": {}
		}
		data["content"] = message

		if replyTo: data["extensions"]["replyMessageId"] = replyTo
		if pollId: data["extensions"]["pollId"] = pollId
		if diceId: data["extensions"]["diceId"] = diceId

		resp = self.send(t=1, data=data, threadId=chatId)
		return resp

	def send_verify_code(self, email: str, country_code: str = None):

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
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def register(self, email: str, password: str, code: str, icon: BinaryIO, country_code: str = None, invitation_code: str = None, nickname: str = 'XsarzyBest', tag_line: str = 'projectZ', gender: int = 100, birthday: str = '1990-01-01'):

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
			"countryCode": country_code if country_code else self.country_code,
			"suggestedCountryCode": country_code.upper() if country_code else self.country_code.upper(),
			"ignoresDisabled": True,
			"rawDeviceIdThree": gen.generate_device_id_three()
		})

		endpoint = '/v1/auth/register'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def visit(self, userId):

		endpoint = f'/v1/users/profile/{userId}/visit'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def activate_wallet(self, wallet_password: str, code: str, email: str = None):


		data = dumps({
			"authType": 1,
			"identity": email if email else self.profile.email if self.profile.email else exceptions.NotLoggined('You are not authorized'),
			"paymentPassword": wallet_password,
			"securityCode": code
		})

		endpoint = '/biz/v1/wallet/0/activate'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def activate_shop(self):

		endpoint = '/biz/v1/activate-store'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.ActivateShop(loads(response.text))

	def wallet_info(self):

		endpoint = '/biz/v1/wallet'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else  objects.WalletInfo(loads(response.text))


	def my_nfts(self):

		endpoint = '/biz/v1/nfts/count'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Nfts(loads(response.text))


	def get_baners(self):

		endpoint = '/v2/banners'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Baners(loads(response.text))

	def get_circles(self, type: str = 'recommend', categoryId: int = 0, size: int = 10):

		endpoint = f'/v1/circles?type={type}&categoryId={categoryId}&size={size}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.CirclesList(loads(response.text))

	def get_blocked_users(self):

		endpoint = '/v1/users/block-uids'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.BlockedUsers(loads(response.text))

	def get_blogs(self, type: str = 'recommend', size: int = 10):

		endpoint = f'/v1/blogs?type={type}&size={size}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Blogs(loads(response.text))


	def mark_as_read(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}/mark-as-read'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def get_chat_threads(self, chatId: int):

		endpoint=f'/v1/chat/threads/{chatId}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)

	def get_online_chat_members(self, chatId: int):

		endpoint=f'/v1/chat/threads/{chatId}/online-members'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)


	def get_chat_messages(self, chatId: int, size: int = 10):

		endpoint=f'/v1/chat/threads/{chatId}/messages?size={size}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)

	def get_mention_candidates(self, chatId: int, size: int = 10, queryWord: str = ''):
		
		endpoint = f'/v1/chat/threads/{chatId}/mention-candidates?size={size}&queryWord={queryWord}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else  objects.MentionCandidates(loads(response.text))

	def comment(self, message: str, userId: int = None, blogId: int = None, replyId: dict = None):

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
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Comments(loads(response.text))


	def get_comments(self, userId: int, type: int = 4, replyId: int= 0, size: int = 30, onlyPinned: int = 0):

		endpoint = f'/v1/comments?parentId={userId}&parentType={type}&replyId={replyId}&size={size}&onlyPinned={onlyPinned}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Comments(loads(response.text))


	def block(self, userId: int):

		endpoint = f'/v1/users/block/{userId}'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def unblock(self, userId: int):

		endpoint = f'/v1/users/block/{userId}'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code



	def accept_chat_invitation(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}/accept-invitation'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def join_circle(self, circleId):
		data = dumps({"joinMethod": 1})

		endpoint = f'/v1/circles/{circleId}/members'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def leave_circle(self, circleId):

		endpoint = f'/v1/circles/{circleId}/members'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def get_circle_info(self, circleId: int):

		endpoint = f'/v1/circles/{circleId}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Circle(loads(response.text))


	def get_chat_info(self, chatId: int):

		endpoint = f'/v1/chat/threads/{chatId}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.ChatInfo(loads(response.text))


	def get_user_info(self, userId: int):

		endpoint = f'/v1/users/profile/{userId}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.UserProfile(loads(response.text))


	def follow(self, userId: int):

		endpoint = f'/v1/users/membership/{userId}'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def unfollow(self, userId: int):

		endpoint = f'/v1/users/membership/{userId}'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code



	def like(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339):

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
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def unlike(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339):

		if commentId:
			endpoint = f'/v1/reactions?objectId={commentId}&objectType=3&stickerId={stickerId}'
		elif blogId:
			endpoint = f'/v1/reactions?objectId={blogId}&objectType=2&stickerId={stickerId}'
		else:
			raise exceptions.WrongType()

		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def invite_to_chat(self, userId: Union[int, list], chatId: int):
		if isinstance(userId, int): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else:raise exceptions.WrongType()

		data = dumps({"invitedUids": userIds})

		endpoint = f'/v1/chat/threads/{chatId}/members-invite'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def get_my_invitation_code(self):

		endpoint = f'/v1/users/multi-invitation-code'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.invitationCode(loads(response.text))

	def get_circles_members(self, circleId: int, size: int = 30, type :str = 'normal', pageToken: str = None):

		endpoint = f'/v1/circles/{circleId}/members?type={type}&size={size}&isExcludeManger=false{f"&pageToken={pageToken}" if pageToken else ""}'
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.CirclesMembers(loads(response.text))


	def add_to_favorites(self, userId: Union[list, int]):

		userIds = userId if isinstance(userId, list) else [userId]
		data = dumps({"targetUids": userIds})
		endpoint = '/v1/users/membership/favorites'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code



	def delete_message(self, chatId: int, messageId: int):

		endpoint = f'/v1/chat/threads/{chatId}/messages/{messageId}'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def kick(self, chatId: int, userId: int, denyEntry: bool = False, removeContent: bool = False):
		
		endpoint = f"/v1/chat/threads/{chatId}/members/{userId}?block={str(denyEntry).lower()}&removeContent={str(removeContent).lower()}"
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def pin_chat(self, chatId):

		endpoint = f'/v1/chat/threads/{chatId}/pin'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def apply_bubble(self, chatId: int, bubbleColor: str):

		data = dumps({"threadId": chatId, "bubbleColor": bubbleColor})
		endpoint = f'/v1/chat/apply-bubble'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def accept_co_host(self, chatId: int):

		endpoint = f"/v1/chat/threads/{chatId}/accept-as-co-host"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def accept_host(self, chatId: int):
		
		endpoint = f"/v1/chat/threads/{chatId}/accept-as-host"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def auto_offline(self, chatId: int, switch: bool = False):

		endpoint = f"/v1/chat/threads/{chatId}/auto-offline/{'disable' if switch == False else 'enable'}"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def check_in(self):
		endpoint = f"/v1/users/check-in"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		response = exceptions.CheckException(response.text) if response.status_code != 200 else objects.OrderInfo(loads(response.text))
		self.claim_transfer_orders(orderId=response.orderId)
		return response

	def claim_transfer_orders(self, orderId: int):

		endpoint = f"/biz/v3/transfer-orders/{orderId}/claim"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def claim_gift_boxes(self, orderId: int):
		endpoint = f"/v1/gift-boxes/{orderId}/claim"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def get_transfer_order_info(self, orderId: int):

		endpoint = f"/biz/v1/transfer-orders/{orderId}"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)


	def send_coins(self, wallet_password: int, userId: int, amount: int, title: str = "Всего Наилучшего!"):

		data = dumps({
			"toObjectId": userId,
			"amount": f"{amount}000000000000000000",
			"paymentPassword": str(wallet_password),
			"toObjectType": 4,
			"currencyType": 100,
			"title": title
		})

		endpoint = f"/biz/v1/gift-boxes"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)


	def online_chat_status(self, chatId: int, online: bool = True):

		data = dumps({"partyOnlineStatus": 1 if online else 2})
		endpoint = f"/v1/chat/threads/{chatId}/party-online-status"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)


	def get_alerts(groupId: int = 3, size: int = 30):

		endpoint = f"/v1/alerts?groupId={groupId}&size={size}"
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)

	def get_moods(self):
		endpoint = f"/v1/moods"
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)



	def change_password(self, oldPassword: str, newPassword: str):

		data = dumps({"oldPassword": oldPassword, "newPassword": newPassword})
		endpoint="/v1/auth/change-password"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code



	def get_message_info(self, chatId: int, messageId: int):

		endpoint = f"/v1/chat/threads/{chatId}/messages/{messageId}"
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)


	def delete_chat(self, chatId: int):

		endpoint = f"/v1/chat/threads/{chatId}"
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def qivotes_chat(self, chatId: int):

		data = dumps({
			"uid": 0,
			"objectId": chatId,
			"objectType": 1,
			"timezone": self.time_zone,
			"votedCount": 1,
			"votedDate": 0,
			"createdTime": 0,
			"lastVoteTime": 0
		})
		endpoint = "/v1/qivotes"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)


	def get_user_tasks(self):

		endpoint = f"/v2/user-tasks"
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else loads(response.text)

	def get_my_gifts(self, size: int = 60):
		endpoint = f"/biz/v2/transfer-orders?size={size}"
		response = self.session.get(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.Gifts(loads(response.text))

	def gift_withdrawn(self, orderId):

		endpoint = f"/biz/v1/gift-boxes/{orderId}/withdrawn"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status != 200 else loads(response.text)
