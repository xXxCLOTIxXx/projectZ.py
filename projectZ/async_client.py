from sys import maxsize
from random import randint
from aiofiles.threadpool.binary import AsyncBufferedReader
from aiohttp import MultipartWriter
from mimetypes import guess_type
from typing import Union

from .ws.async_socket import AsyncSocket
from .requests_builder import AsyncRequester
from .objects.profile import profile
from .objects.objects import *
from .objects.constants import LoggerLevel, ws_endpoint
from .objects.ChatMessageTypes import ChatMessageTypes

from .utils.exceptions import (
	WrongType
)

class AsyncClient(AsyncSocket):
	req: AsyncRequester
	def __init__(self, deviceId: str = None, language: str = "en-US", country_code: str = "us", time_zone: int = 180, socket_debug: LoggerLevel = LoggerLevel.OFF):
		self.req = AsyncRequester(profile(
			deviceId=deviceId,
			language=language,
			country_code=country_code,
			time_zone=time_zone
		))
		AsyncSocket.__init__(self, debug=socket_debug)

	@property
	def userId(self):
		return self.req.profile.uid

	@property
	def sid(self):
		return self.req.profile.sid

	@property
	def deviceId(self):
		return self.req.profile.deviceId


	async def upload_media(self, file: AsyncBufferedReader, target: int, duration: int = 0) -> Media:
		file_content = await file.read()
		writer = MultipartWriter()
		part = writer.append(file_content, {"Content-Type": guess_type(file.name)[0]})
		part.set_content_disposition("form-data", name="media", filename=file.name)
		return Media(await self.req.request("POST", f"/v1/media/upload?target={target}&duration={duration}", writer, content_type=f"multipart/form-data; boundary={writer.boundary}"))


	async def login(self, email: str, password: str) -> User:
		result = User(await self.req.request("POST", "/v1/auth/login", {
			"password":password,
			"email":email,
			"authType":1
		}))
		self.req.profile.sid, self.req.profile.uid = result.sid, result.uid
		await self.ws_connect(self.req.build_headers(ws_endpoint))
		return result
	


	async def logout(self) -> dict:

		result = await self.req.request("POST", "/v1/auth/logout")
		self.req.profile.sid, self.req.profile.uid = '', None
		await self.ws_disconnect()
		return result
	

	async def join_chat(self, chatId: int) -> dict:
		return await self.req.request("POST", f"/v1/chat/threads/{chatId}/members")

	async def leave_chat(self, chatId: int) -> dict:
		return await self.req.request("DELETE", f"/v1/chat/threads/{chatId}/members")

	async def get_from_link(self, link: str) -> FromLink:
		return FromLink(await self.req.request("POST", f"/v1/links/path", {"link": link}))

	async def get_link(self, userId: int = None, chatId: int = None, circleId: int = None, blogId: int = None) -> FromLink:

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
		return FromLink(await self.req.request("POST", f"/v1/links/share"))


	async def get_my_chats(self, start: int = 0, size: int = 20, type: str = 'managed'):	
		return Thread(await self.req.request("GET", f"/v1/chat/joined-threads?start={start}&size={size}&type={type}"))


	async def send_message(self, chatId: int, message: str = None, media: Media = None, message_type: int = ChatMessageTypes.TEXT, replyTo: int = None, pollId: int = None, diceId: int = None) -> None:
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
		await self.ws_send(req_t=1, **dict(threadId=chatId, msg=data))

	async def send_text_message(self, chatId: int, message: str) -> None:
		await self.send_message(chatId=chatId, message=message, message_type=ChatMessageTypes.TEXT)

	async def send_audio_message(self, chatId: int, audio: Media) -> None:
		await self.send_message(chatId=chatId, media=audio, message_type=ChatMessageTypes.AUDIO)

	async def send_image_message(self, chatId: int, image: Media) -> None:
		await self.send_message(chatId=chatId, media=image, message_type=ChatMessageTypes.MEDIA)

	async def send_video_message(self, chatId: int, video: Media) -> None:
		await self.send_message(chatId=chatId, media=video, message_type=ChatMessageTypes.VIDEO)

	async def typing(self, chatId: int) -> None:
		await self.send_message(chatId=chatId, message_type=ChatMessageTypes.TYPING)


	async def visit(self, userId) -> dict:
		return await self.req.request("POST", f"/v1/users/profile/{userId}/visit")
	

	async def activate_wallet(self, email: str, wallet_password: str, code: str) -> dict:
		return await self.req.request("POST", f"/biz/v1/wallet/0/activate", {
			"authType": 1,
			"identity": email,
			"paymentPassword": wallet_password,
			"securityCode": code
		})

	async def activate_shop(self) -> ActivateShop:
		return ActivateShop(await self.req.request("POST", f"/biz/v1/activate-store"))
	

	async def wallet_info(self) -> WalletInfo:
		return WalletInfo(await self.req.request("GET", f"/biz/v1/wallet"))

	async def my_nfts(self) -> Nfts:
		return Nfts(await self.req.request("GET", f"/biz/v1/nfts/count"))

	async def get_baners(self) -> Baners:
		return Baners(await self.req.request("GET", f"/v2/banners"))

	async def get_circles(self, type: str = 'recommend', categoryId: int = 0, size: int = 10) -> CirclesList:
		return CirclesList(await self.req.request("GET", f"/v1/circles?type={type}&categoryId={categoryId}&size={size}"))


	async def get_blocked_users(self) -> BlockedUsers:
		return BlockedUsers(await self.req.request("GET", f"/v1/users/block-uids"))
        
	async def get_visitors(self, userId: int, size: int =30):
                return await self.req.request("GET", f"/v1/users/membership/{userId}?type=visitor&size={size}")
	

	async def get_blogs(self, type: str = 'recommend', size: int = 10) -> Blogs:
		return Blogs(await self.req.request("GET", f'/v1/blogs?type={type}&size={size}'))


	async def mark_as_read(self, chatId: int) -> dict:
		return await self.req.request("POST", f'/v1/chat/threads/{chatId}/mark-as-read')
	
	async def get_chat_threads(self, chatId: int) -> dict:
		return await self.req.request("GET", f'/v1/chat/threads/{chatId}')

	async def get_online_chat_members(self, chatId: int) -> dict:
		return await self.req.request("GET", f'/v1/chat/threads/{chatId}/online-members')


	async def get_chat_messages(self, chatId: int, size: int = 10) -> dict:
		return await self.req.request("GET", f'/v1/chat/threads/{chatId}/messages?size={size}')

	async def get_mention_candidates(self, chatId: int, size: int = 10, queryWord: str = '') -> MentionCandidates:
		return MentionCandidates(await self.req.request("GET", f'/v1/chat/threads/{chatId}/mention-candidates?size={size}&queryWord={queryWord}'))

	async def comment(self, message: str, userId: int = None, blogId: int = None, replyId: dict = None) -> Comments:
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
		return Comments(await self.req.request("POST", '/v1/comments', data))

	async def get_comments(self, userId: int, type: int = 4, replyId: int= 0, size: int = 30, onlyPinned: int = 0) -> Comments:
		return Comments(await self.req.request("GET", f'/v1/comments?parentId={userId}&parentType={type}&replyId={replyId}&size={size}&onlyPinned={onlyPinned}'))

	async def block(self, userId: int) -> dict:
		return await self.req.request("POST", f'/v1/users/block/{userId}')

	async def unblock(self, userId: int) -> dict:
		return await self.req.request("DELETE", f'/v1/users/block/{userId}')

	async def accept_chat_invitation(self, chatId: int) -> dict:
		return await self.req.request("POST", f'/v1/chat/threads/{chatId}/accept-invitation')

	async def join_circle(self, circleId) -> dict:
		return await self.req.request("POST", f'/v1/circles/{circleId}/members', {"joinMethod": 1})

	async def leave_circle(self, circleId) -> dict:
		return await self.req.request("DELETE", f'/v1/circles/{circleId}/members')

	async def get_circle_info(self, circleId: int) -> Circle:
		return Circle(await self.req.request("GET", f'/v1/circles/{circleId}'))

	async def get_chat_info(self, chatId: int) -> ChatInfo:
		return ChatInfo(await self.req.request("GET", f'/v1/chat/threads/{chatId}'))

	async def get_user_info(self, userId: int) -> UserProfile:
		return UserProfile(await self.req.request("GET", f'/v1/users/profile/{userId}'))

	async def follow(self, userId: int) -> dict:
		return await self.req.request("POST", f'/v1/users/membership/{userId}')

	async def unfollow(self, userId: int) -> dict:
		return await self.req.request("DELETE", f'/v1/users/membership/{userId}')

	async def like(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339) -> dict:
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
		return await self.req.request("POST", '/v1/reactions',data)

	async def unlike(self, commentId: int = None, blogId: int = None, stickerId: int = 65956773102028339) -> dict:
		if commentId:endpoint = f'/v1/reactions?objectId={commentId}&objectType=3&stickerId={stickerId}'
		elif blogId:endpoint = f'/v1/reactions?objectId={blogId}&objectType=2&stickerId={stickerId}'
		else:raise WrongType()
		return await self.req.request("DELETE", endpoint)

	async def invite_to_chat(self, userId: Union[int, list], chatId: int) -> dict:
		if isinstance(userId, int): userIds = [userId]
		elif isinstance(userId, list): userIds = userId
		else:raise WrongType(type(userId))
		return await self.req.request("POST", f'/v1/chat/threads/{chatId}/members-invite', {"invitedUids": userIds})

	async def get_my_invitation_code(self) -> dict:
		return await self.req.request("GET", f'/v1/users/multi-invitation-code')

	async def get_circles_members(self, circleId: int, size: int = 30, type :str = 'normal', pageToken: str = None) -> CirclesMembers:
		return CirclesMembers(await self.req.request("GET", f'/v1/circles/{circleId}/members?type={type}&size={size}&isExcludeManger=false{f"&pageToken={pageToken}" if pageToken else ""}'))

	async def add_to_favorites(self, userId: Union[list, int]) -> dict:
		return await self.req.request("POST", f'/v1/users/membership/favorites', {"targetUids": userId if isinstance(userId, list) else [userId]})

	async def delete_message(self, chatId: int, messageId: int) -> dict:
		return await self.req.request("DELETE", f'/v1/chat/threads/{chatId}/messages/{messageId}')

	async def kick(self, chatId: int, userId: int, denyEntry: bool = False, removeContent: bool = False) -> dict:
		return await self.req.request("DELETE", f"/v1/chat/threads/{chatId}/members/{userId}?block={str(denyEntry).lower()}&removeContent={str(removeContent).lower()}")

	async def pin_chat(self, chatId) -> dict:
		return await self.req.request("POST", f'/v1/chat/threads/{chatId}/pin')

	async def apply_bubble(self, chatId: int, bubbleColor: str) -> dict:
		return await self.req.request("POST", f'/v1/chat/apply-bubble', {"threadId": chatId, "bubbleColor": bubbleColor})

	async def accept_co_host(self, chatId: int) -> dict:
		return await self.req.request("POST", f"/v1/chat/threads/{chatId}/accept-as-co-host")

	async def accept_host(self, chatId: int) -> dict:
		return await self.req.request("POST", f"/v1/chat/threads/{chatId}/accept-as-host")

	async def auto_offline(self, chatId: int, switch: bool = False) -> dict:
		return await self.req.request("POST", f"/v1/chat/threads/{chatId}/auto-offline/{'disable' if switch == False else 'enable'}")

	async def check_in(self) -> OrderInfo:
		return OrderInfo(await self.req.request("POST", f'/v1/users/check-in'))

	async def claim_transfer_orders(self, orderId: int) -> dict:
		return await self.req.request("POST", f'/biz/v3/transfer-orders/{orderId}/claim')

	async def claim_gift_boxes(self, orderId: int) -> dict:
		return await self.req.request("POST", f'/v1/gift-boxes/{orderId}/claim')

	async def get_transfer_order_info(self, orderId: int) -> dict:
		return await self.req.request("GET", f'/biz/v1/transfer-orders/{orderId}')

	async def send_coins(self, wallet_password: int, userId: int, amount: int, title: str = "Всего Наилучшего!") -> dict:
		return await self.req.request("POST", f'/biz/v1/gift-boxes', {
			"toObjectId": userId,
			"amount": f"{amount}000000000000000000",
			"paymentPassword": str(wallet_password),
			"toObjectType": 4,
			"currencyType": 100,
			"title": title
		})

	async def send_nft(self, wallet_password: int, userId: int, nftId: int, amount: int = 0, title: str = "Muitas Felicidades!!!") -> dict:
		return await self.req.request("POST", f'/biz/v1/gift-boxes', {
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

	async def online_chat_status(self, chatId: int, online: bool = True) -> dict:
		return await self.req.request("POST", f'/v1/chat/threads/{chatId}/party-online-status', {"partyOnlineStatus": 1 if online else 2})

	async def get_alerts(self, groupId: int = 3, size: int = 30) -> dict:
		return await self.req.request("GET", f'/v1/alerts?groupId={groupId}&size={size}')

	async def get_moods(self) -> dict:
		return await self.req.request("GET", '/v1/moods')

	async def change_password(self, oldPassword: str, newPassword: str) -> dict:
		return await self.req.request("POST", f'/v1/auth/change-password', {"oldPassword": oldPassword, "newPassword": newPassword})

	async def get_message_info(self, chatId: int, messageId: int) -> dict:
		return await self.req.request("GET", f'/v1/chat/threads/{chatId}/messages/{messageId}')

	async def delete_chat(self, chatId: int) -> dict:
		return await self.req.request("DELETE", f'/v1/chat/threads/{chatId}')

	async def qivotes_chat(self, chatId: int) -> dict:
		return await self.req.request("POST", f'/v1/qivotes', {
			"uid": 0,
			"objectId": chatId,
			"objectType": 1,
			"timezone": self.time_zone,
			"votedCount": 1,
			"votedDate": 0,
			"createdTime": 0,
			"lastVoteTime": 0
		})

	async def get_user_tasks(self) -> dict:
		return await self.req.request("GET", f'/v2/user-tasks')

	async def get_my_gifts(self, size: int = 60) -> Gifts:
		return Gifts(await self.req.request("GET", f"/biz/v2/transfer-orders?size={size}"))

	async def gift_withdrawn(self, orderId) -> dict:
		return await self.req.request("GET", f'/biz/v1/gift-boxes/{orderId}/withdrawn')

	async def report(self, userId: int, message: str, images: Union[Media, list[Media]], flagType: int = 100) -> dict:

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
		return await self.req.request("POST", f'/v1/flags', data)

	async def get_my_companion(self) -> dict:
		return await self.req.request("GET", f'/v1/companion')

	async def set_companion(self, nftId: int) -> dict:
		return await self.req.request("POST", f'/v1/companion', {"nftId": nftId})

	async def get_build_in_companions(self, size: int = 10) -> dict:
		return await self.req.request("GET", f'/biz/v1/build-in-character-list?size={size}')

	async def get_nft_info(self, nftId: int) -> dict:
		return await self.req.request("GET", f'/biz/v1/nft/{nftId}')
