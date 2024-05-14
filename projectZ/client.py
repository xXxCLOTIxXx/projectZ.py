from sys import maxsize
from random import randint
from typing import Union, BinaryIO
from requests_toolbelt.multipart.encoder import MultipartEncoder
from mimetypes import guess_type

from .ws.socket import Socket
from .requests_builder import requester
from .objects.profile import profile
from .objects.objects import *
from .objects.constants import LoggerLevel, ws_endpoint
from .objects.ChatMessageTypes import ChatMessageTypes
from .utils.exceptions import (
	WrongType
)

class Client(Socket):
	req: requester
	def __init__(self, deviceId: str = None, language: str = "en-US", country_code: str = "us", time_zone: int = 180, socket_trace: bool = False, socket_debug: LoggerLevel = LoggerLevel.OFF):
		self.req = requester(profile(
			deviceId=deviceId,
			language=language,
			country_code=country_code,
			time_zone=time_zone
		))
		Socket.__init__(self, sock_trace=socket_trace, debug=socket_debug)

	@property
	def userId(self):
		return self.req.profile.uid

	@property
	def sid(self):
		return self.req.profile.sid

	@property
	def deviceId(self):
		return self.req.profile.deviceId


	def upload_media(self, file: BinaryIO, target: int, duration: int = 0) -> Media:
		data = MultipartEncoder({
        	'media': (file.name, file.read(), guess_type(file.name)[0])
   		 })
		return Media(self.req.request("POST", f"/v1/media/upload?target={target}&duration={duration}", data, content_type=data.content_type))


	def login(self, email: str, password: str) -> User:
		result = User(self.req.request("POST", "/v1/auth/login", {
			"password":password,
			"email":email,
			"authType":1
		}))
		self.req.profile.sid, self.req.profile.uid = result.sid, result.uid
		self.ws_connect(self.req.build_headers(ws_endpoint))
		return result


	def logout(self) -> dict:

		result = self.req.request("POST", "/v1/auth/logout")
		self.req.profile.sid, self.req.profile.uid = '', None
		self.ws_disconnect()
		return result

	def join_chat(self, chatId: int) -> dict:
		return self.req.request("POST", f"/v1/chat/threads/{chatId}/members")

	def leave_chat(self, chatId: int) -> dict:
		return self.req.request("DELETE", f"/v1/chat/threads/{chatId}/members")

	def get_from_link(self, link: str) -> FromLink:
		return FromLink(self.req.request("POST", f"/v1/links/path", {"link": link}))

	def get_link(self, userId: int = None, chatId: int = None, circleId: int = None, blogId: int = None) -> FromLink:

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
		else:raise WrongType("ID not specified.")
		return FromLink(self.req.request("POST", f"/v1/links/share"))


	def get_my_chats(self, start: int = 0, size: int = 20, type: str = 'managed'):	
		return Thread(self.req.request("GET", f"/v1/chat/joined-threads?start={start}&size={size}&type={type}"))


	def send_message(self, chatId: int, message: str = None, media: Media = None, message_type: int = ChatMessageTypes.TEXT, replyTo: int = None, pollId: int = None, diceId: int = None) -> None:
		data = {
			"type": message_type,
			"threadId": chatId,
			"uid": self.req.profile.uid,
			"seqId": randint(0, maxsize),
			"extensions": {}
		}
		if message:
			data["content"] = message
			if replyTo: data["extensions"]["replyMessageId"] = replyTo
		elif media: data["media"] = media.json
		if pollId: data["extensions"]["pollId"] = pollId
		if diceId: data["extensions"]["diceId"] = diceId
		self.ws_send(req_t=1, **dict(threadId=chatId, msg=data))

	def send_text_message(self, chatId: int, message: str) -> None:
		self.send_message(chatId=chatId, message=message, message_type=ChatMessageTypes.TEXT)

	def send_audio_message(self, chatId: int, audio: Media) -> None:
		self.send_message(chatId=chatId, media=audio, message_type=ChatMessageTypes.AUDIO)

	def send_image_message(self, chatId: int, image: Media) -> None:
		self.send_message(chatId=chatId, media=image, message_type=ChatMessageTypes.MEDIA)

	def send_video_message(self, chatId: int, video: Media) -> None:
		self.send_message(chatId=chatId, media=video, message_type=ChatMessageTypes.VIDEO)

	def typing(self, chatId: int) -> None:
		self.send_message(chatId=chatId, message_type=ChatMessageTypes.TYPING)


	def visit(self, userId) -> dict:
		return self.req.request("POST", f"/v1/users/profile/{userId}/visit")
	

	def activate_wallet(self, email: str, wallet_password: str, code: str) -> dict:
		return self.req.request("POST", f"/biz/v1/wallet/0/activate", {
			"authType": 1,
			"identity": email,
			"paymentPassword": wallet_password,
			"securityCode": code
		})

	def activate_shop(self) -> ActivateShop:
		return ActivateShop(self.req.request("POST", f"/biz/v1/activate-store"))
	

	def wallet_info(self) -> WalletInfo:
		return WalletInfo(self.req.request("GET", f"/biz/v1/wallet"))

	def my_nfts(self) -> Nfts:
		return Nfts(self.req.request("GET", f"/biz/v1/nfts/count"))

	def get_baners(self) -> Baners:
		return Baners(self.req.request("GET", f"/v2/banners"))

	def get_circles(self, type: str = 'recommend', categoryId: int = 0, size: int = 10) -> CirclesList:
		return CirclesList(self.req.request("GET", f"/v1/circles?type={type}&categoryId={categoryId}&size={size}"))
        def get_visitors(self, userId: int, size: int =30):
                return self.req.request("GET", f"/v1/users/membership/{userId}?type=visitor&size={size}")

	def get_blocked_users(self) -> BlockedUsers:
		return BlockedUsers(self.req.request("GET", f"/v1/users/block-uids"))


	def get_blogs(self, type: str = 'recommend', size: int = 10) -> Blogs:
		return Blogs(self.req.request("GET", f'/v1/blogs?type={type}&size={size}'))


	def mark_as_read(self, chatId: int) -> dict:
		return self.req.request("POST", f'/v1/chat/threads/{chatId}/mark-as-read')
	
	def get_chat_threads(self, chatId: int) -> dict:
		return self.req.request("GET", f'/v1/chat/threads/{chatId}')

	def get_online_chat_members(self, chatId: int) -> dict:
		return self.req.request("GET", f'/v1/chat/threads/{chatId}/online-members')


	def get_chat_messages(self, chatId: int, size: int = 10) -> dict:
		return self.req.request("GET", f'/v1/chat/threads/{chatId}/messages?size={size}')

	def get_mention_candidates(self, chatId: int, size: int = 10, queryWord: str = '') -> MentionCandidates:
		return MentionCandidates(self.req.request("GET", f'/v1/chat/threads/{chatId}/mention-candidates?size={size}&queryWord={queryWord}'))

	def comment(self, message: str, userId: int = None, blogId: int = None, replyId: dict = None) -> Comments:
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
		if userId:data['parentType'] = 4
		elif blogId:data['parentType'] = 2
		else:raise WrongType()
		if replyId:
			data['replyId'] = replyId['commentId']
			data['extensions'] = {"replyToUid": replyId['userId'], "contentStatus": 1}
		return Comments(self.req.request("POST", '/v1/comments', data))

	def get_comments(self, userId: int, type: int = 4, replyId: int= 0, size: int = 30, onlyPinned: int = 0) -> Comments:
		return Comments(self.req.request("GET", f'/v1/comments?parentId={userId}&parentType={type}&replyId={replyId}&size={size}&onlyPinned={onlyPinned}'))

	def block(self, userId: int) -> dict:
		return self.req.request("POST", f'/v1/users/block/{userId}')

	def unblock(self, userId: int) -> dict:
		return self.req.request("DELETE", f'/v1/users/block/{userId}')

	def accept_chat_invitation(self, chatId: int) -> dict:
		return self.req.request("POST", f'/v1/chat/threads/{chatId}/accept-invitation')

	def join_circle(self, circleId) -> dict:
		return self.req.request("POST", f'/v1/circles/{circleId}/members', {"joinMethod": 1})

	def leave_circle(self, circleId) -> dict:
		return self.req.request("DELETE", f'/v1/circles/{circleId}/members')

	def get_circle_info(self, circleId: int) -> Circle:
		return Circle(self.req.request("GET", f'/v1/circles/{circleId}'))

	def get_chat_info(self, chatId: int) -> ChatInfo:
		return ChatInfo(self.req.request("GET", f'/v1/chat/threads/{chatId}'))

	def get_user_info(self, userId: int) -> UserProfile:
		return UserProfile(self.req.request("GET", f'/v1/users/profile/{userId}'))

	def follow(self, userId: int) -> dict:
		return self.req.request("POST", f'/v1/users/membership/{userId}')

	def unfollow(self, userId: int) -> dict:
		return self.req.request("DELETE", f'/v1/users/membership/{userId}')

	def like(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339) -> dict:
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
		else:raise WrongType()
		return self.req.request("POST", '/v1/reactions',data)

	def unlike(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339) -> dict:
		if commentId:endpoint = f'/v1/reactions?objectId={commentId}&objectType=3&stickerId={stickerId}'
		elif blogId:endpoint = f'/v1/reactions?objectId={blogId}&objectType=2&stickerId={stickerId}'
		else:raise WrongType()
		return self.req.request("DELETE", endpoint)

	def invite_to_chat(self, userId: Union[int, list], chatId: int) -> dict:
		if isinstance(userId, int): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else:raise WrongType(type(userId))
		return self.req.request("POST", f'/v1/chat/threads/{chatId}/members-invite', {"invitedUids": userIds})

	def get_my_invitation_code(self) -> dict:
		return self.req.request("GET", f'/v1/users/multi-invitation-code')

	def get_circles_members(self, circleId: int, size: int = 30, type :str = 'normal', pageToken: str = None) -> CirclesMembers:
		return CirclesMembers(self.req.request("GET", f'/v1/circles/{circleId}/members?type={type}&size={size}&isExcludeManger=false{f"&pageToken={pageToken}" if pageToken else ""}'))

	def add_to_favorites(self, userId: Union[list, int]) -> dict:
		return self.req.request("POST", f'/v1/users/membership/favorites', {"targetUids": userId if isinstance(userId, list) else [userId]})

	def delete_message(self, chatId: int, messageId: int) -> dict:
		return self.req.request("DELETE", f'/v1/chat/threads/{chatId}/messages/{messageId}')

	def kick(self, chatId: int, userId: int, denyEntry: bool = False, removeContent: bool = False) -> dict:
		return self.req.request("DELETE", f"/v1/chat/threads/{chatId}/members/{userId}?block={str(denyEntry).lower()}&removeContent={str(removeContent).lower()}")

	def pin_chat(self, chatId) -> dict:
		return self.req.request("POST", f'/v1/chat/threads/{chatId}/pin')

	def apply_bubble(self, chatId: int, bubbleColor: str) -> dict:
		return self.req.request("POST", f'/v1/chat/apply-bubble', {"threadId": chatId, "bubbleColor": bubbleColor})

	def accept_co_host(self, chatId: int) -> dict:
		return self.req.request("POST", f"/v1/chat/threads/{chatId}/accept-as-co-host")

	def accept_host(self, chatId: int) -> dict:
		return self.req.request("POST", f"/v1/chat/threads/{chatId}/accept-as-host")

	def auto_offline(self, chatId: int, switch: bool = False) -> dict:
		return self.req.request("POST", f"/v1/chat/threads/{chatId}/auto-offline/{'disable' if switch == False else 'enable'}")

	def check_in(self) -> OrderInfo:
		return OrderInfo(self.req.request("POST", f'/v1/users/check-in'))

	def claim_transfer_orders(self, orderId: int) -> dict:
		return self.req.request("POST", f'/biz/v3/transfer-orders/{orderId}/claim')

	def claim_gift_boxes(self, orderId: int) -> dict:
		return self.req.request("POST", f'/v1/gift-boxes/{orderId}/claim')

	def get_transfer_order_info(self, orderId: int) -> dict:
		return self.req.request("GET", f'/biz/v1/transfer-orders/{orderId}')

	def send_coins(self, wallet_password: int, userId: int, amount: int, title: str = "Всего Наилучшего!") -> dict:
		return self.req.request("POST", f'/biz/v1/gift-boxes', {
			"toObjectId": userId,
			"amount": f"{amount}000000000000000000",
			"paymentPassword": str(wallet_password),
			"toObjectType": 4,
			"currencyType": 100,
			"title": title
		})

	def send_nft(self, wallet_password: int, userId: int, nftId: int, amount: int = 0, title: str = "Muitas Felicidades!!!") -> dict:
		return self.req.request("POST", f'/biz/v1/gift-boxes', {
			"toObjectId": userId,
			"assetId": nftId,
			"amount": str(amount),
			"paymentPassword": str(wallet_password),
			"toObjectType": 4,
			"currencyType": 105,
			"title": str(title),
			"maxClaimedCount": 1,
			"distributeMode": 3
		})

	def online_chat_status(self, chatId: int, online: bool = True) -> dict:
		return self.req.request("POST", f'/v1/chat/threads/{chatId}/party-online-status', {"partyOnlineStatus": 1 if online else 2})

	def get_alerts(self, groupId: int = 3, size: int = 30) -> dict:
		return self.req.request("GET", f'/v1/alerts?groupId={groupId}&size={size}')

	def get_moods(self) -> dict:
		return self.req.request("GET", '/v1/moods')

	def change_password(self, oldPassword: str, newPassword: str) -> dict:
		return self.req.request("POST", f'/v1/auth/change-password', {"oldPassword": oldPassword, "newPassword": newPassword})

	def get_message_info(self, chatId: int, messageId: int) -> dict:
		return self.req.request("GET", f'/v1/chat/threads/{chatId}/messages/{messageId}')

	def delete_chat(self, chatId: int) -> dict:
		return self.req.request("DELETE", f'/v1/chat/threads/{chatId}')

	def qivotes_chat(self, chatId: int) -> dict:
		return self.req.request("POST", f'/v1/qivotes', {
			"uid": 0,
			"objectId": chatId,
			"objectType": 1,
			"timezone": self.time_zone,
			"votedCount": 1,
			"votedDate": 0,
			"createdTime": 0,
			"lastVoteTime": 0
		})

	def get_user_tasks(self) -> dict:
		return self.req.request("GET", f'/v2/user-tasks')

	def get_my_gifts(self, size: int = 60) -> Gifts:
		return Gifts(self.req.request("GET", f"/biz/v2/transfer-orders?size={size}"))

	def gift_withdrawn(self, orderId) -> dict:
		return self.req.request("GET", f'/biz/v1/gift-boxes/{orderId}/withdrawn')

	def report(self, userId: int, message: str, images: Union[Media, list[Media]], flagType: int = 100) -> dict:

		media = list()
		if isinstance(images, Media):images=[images]
		elif isinstance(images, list):pass
		else:raise WrongType()
		data = {
			"objectId": userId,
			"objectType": 4,
			"flagType": flagType,
			"message": message,
		}
		for image in images:
			media.append(image.json)
		data["mediaList"] = media
		return self.req.request("POST", f'/v1/flags', data)

	def get_my_companion(self) -> dict:
		return self.req.request("GET", f'/v1/companion')

	def set_companion(self, nftId: int) -> dict:
		return self.req.request("POST", f'/v1/companion', {"nftId": nftId})

	def get_build_in_companions(self, size: int = 10) -> dict:
		return self.req.request("GET", f'/biz/v1/build-in-character-list?size={size}')

	def get_nft_info(self, nftId: int) -> dict:
		return self.req.request("GET", f'/biz/v1/nft/{nftId}')
