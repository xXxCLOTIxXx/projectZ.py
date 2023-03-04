
__all__ = ['Media', 'User', 'FromLink', 'ThreadList', 'Thread', 'Event', 'ActivateShop', 'WalletInfo']


class Media:
	def __init__(self, data: dict = {}):
		self.json = data
		self.mediaId = self.json.get('mediaId', None)
		self.baseUrl = self.json.get('baseUrl', None)
		self.resourceList = list()

		for res in self.json.get('resourceList', []):
			self.resourceList.append(self.Resources(res))


	class Resources:
		def __init__(self, data: dict = {}):
			self.json = data
			self.width = self.json.get('width', None)
			self.height = self.json.get('height', None)
			self.url = self.json.get('url', None)
			self.thumbnail = self.json.get('thumbnail', None)



class User:
	def __init__(self, data: dict = {}):
		self.json = data
		account = self.json.get('account', {})
		userProfile = self.json.get('userProfile', {})

		self.sid = self.json.get('sId', None)
		self.secret = self.json.get('secret', None)
		self.uid = account.get('uid', None)
		self.email = account.get('email', None)
		self.createdTime = account.get('createdTime', None)
		self.deviceId = account.get('deviceId', None)
		self.googleId = account.get('googleId', None)
		self.nickname = userProfile.get('nickname', None)
		self.socialId = userProfile.get('socialId', None)
		self.gender = userProfile.get('gender', None)
		self.socialIdModified = userProfile.get('socialIdModified', None)



class FromLink:
	def __init__(self, data: dict = {}):
		self.json = data
		self.path = self.json.get('path', None)
		self.objectId = self.json.get('objectId', None)
		self.objectType = self.json.get('objectType', None)
		self.parentId = self.json.get('parentId', None)
		self.parentType = self.json.get('parentType', None)
		self.shareLink = self.json.get('shareLink', None)

class ThreadList:
	def __init__(self, data: dict = {}):
		self.json = data
		self.threadId = list()
		self.title = list()
		self.hostUid = list()

		for thread in self.json:
			self.threadId.append(thread.get('threadId', None))
			self.hostUid.append(thread.get('hostUid', None))
			self.title.append(thread.get('title', None))


class Thread:
	def __init__(self, data: dict = {}):
		self.json = data
		self.beMentionedThreadIdList = self.json.get('beMentionedThreadIdList', None)
		self.isEnd = self.json.get('isEnd', None)
		self.ThreadList = ThreadList(self.json.get('list', []))
		self.threadCheckList = self.json.get('threadCheckList', None)


class Event:
	def __init__(self, data: dict = {}):
		self.json = data
		msg = self.json.get('msg', {})
		author = msg.get('author', {})
		extensions = msg.get('extensions', {})
		richFormat = msg.get('richFormat', {})
		authorExtensions = author.get('extensions', {})

		self.type = self.json.get('t', None)
		self.threadId = msg.get('threadId', None)
		self.messageId = msg.get('messageId', None)
		self.userId = author.get('uid', None)
		self.createdTime = msg.get('createdTime', None)
		self.messageType = msg.get('type', None)
		self.asSummary = msg.get('asSummary', None)
		self.seqId = msg.get('seqId', None)
		self.content = msg.get('content', None)
		self.roleContentStatus = extensions.get('roleContentStatus', None)
		self.richFormatVersion = richFormat.get('version', None)
		self.nickname = author.get('nickname', None)
		self.gender = author.get('gender', None)
		self.status = author.get('status', None)
		self.icon = Media(author.get('icon', {}))
		self.adminPartyOnlineStatus = authorExtensions.get('adminPartyOnlineStatus', None)
		self.bubbleColor = msg.get('bubbleColor', None)
		self.ref = msg.get('ref', {})



class ActivateShop:
	def __init__(self, data: dict = {}):
		self.json=data

		background = self.json.get('background', {})
		extensions = self.json.get('extensions', {})

		self.storeId = self.json.get('storeId', None)
		self.storeType = self.json.get('storeType', None)
		self.contentRegion = self.json.get('contentRegion', None)
		self.storeStatus = self.json.get('storeStatus', None)
		self.status = self.json.get('status', None)
		self.name = self.json.get('name', None)
		self.description = self.json.get('description', None)
		self.icon = Media(self.json.get('icon', None))
		self.backgroundColor = background.get('backgroundColor', None)
		self.displayMode = background.get('displayMode', None)

		self.ownerId = self.json.get('ownerId', None)
		self.ownerType = self.json.get('ownerType', None)
		self.lastActivateTime = extensions.get('lastActivateTime', None)
		self.isShowDefaultIcon = extensions.get('isShowDefaultIcon', None)
		self.isShowDefaultDescription = extensions.get('isShowDefaultDescription', None)
		self.createdTime = self.json.get('createdTime', None)
		self.owner = self.Owner(self.json.get('owner', {}))


	class Owner:
		def __init__(self, data: dict = {}):
			self.json=data

			extensions = self.json.get('extensions', {})
			userVisitorInfo = self.json.get('userVisitorInfo', {})

			self.userId = self.json.get('uid', None)
			self.nickname = self.json.get('nickname', None)
			self.socialId = self.json.get('socialId', None)
			self.socialIdModified = self.json.get('socialIdModified', None)
			self.gender = self.json.get('gender', None)
			self.status = self.json.get('status', None)
			self.storeId = self.json.get('storeId', None)
			self.icon = Media(self.json.get('icon', {}))
			self.chatInvitationStatus = self.json.get('chatInvitationStatus', None)
			self.publicChatInvitationStatus = self.json.get('publicChatInvitationStatus', None)
			self.privateChatInvitationStatus = self.json.get('privateChatInvitationStatus', None)
			self.circleInvitationStatus = self.json.get('circleInvitationStatus', None)
			self.adminPartyOnlineStatus = extensions.get('adminPartyOnlineStatus', None)
			self.openDaysInRow = extensions.get('openDaysInRow', None)
			self.maxOpenDaysInRow = extensions.get('maxOpenDaysInRow', None)
			self.lastOpenDate = extensions.get('lastOpenDate', None)
			self.showRecentVisitor = extensions.get('showRecentVisitor', None)
			self.onlineStatus = self.json.get('onlineStatus', None)
			self.createdTime = self.json.get('createdTime', None)
			self.contentRegion = self.json.get('contentRegion', None)
			self.contentRegionName = self.json.get('contentRegionName', None)
			self.userMood = self.UserMood(self.json.get('userMood', {}))
			self.showsSchool = self.json.get('showsSchool', None)
			self.lastActiveTime = self.json.get('lastActiveTime', None)
			self.showsLocation = self.json.get('showsLocation', None)
			self.location = self.json.get('location', None)
			self.nameCardEnabled = self.json.get('nameCardEnabled', None)
			self.matchEnabled = self.json.get('matchEnabled', None)
			self.tagline = self.json.get('tagline', None)
			self.totalViewCount = userVisitorInfo.get('totalViewCount', None)
			self.unreadViewCount = userVisitorInfo.get('unreadViewCount', None)
			self.userProfileVisitMode = userVisitorInfo.get('userProfileVisitMode', None)


		class UserMood:
			def __init__(self, data: dict = {}):
				self.json = data
				self.type = self.json.get('type', None)
				self.stickerId = self.json.get('stickerId', None)
				self.text = self.json.get('text', None)
				self.onlineStatus = self.json.get('onlineStatus', None)
				self.sticker = self.Sticker(self.json.get('sticker', {}))

			class Sticker:
				def __init__(self, data: dict = {}):
					self.json = data
					self.stickerId = self.json.get('stickerId', None)
					self.name = self.json.get('name', None)
					self.media = Media(self.json.get('media', {}))



class WalletInfo:
	def __init__(self, data: dict = {}):
		self.json = data
		self.userId = self.json.get('uid', None)
		self.activateStatus = self.json.get('activateStatus', None)
		self.status = self.json.get('status', None)
		self.createdTime = self.json.get('createdTime', None)
		self.walletExtension = self.json.get('walletExtension', {})
		self.unreadTransferOrderCount = self.json.get('unreadTransferOrderCount', None)
		self.latestTransferOrder = self.LatestTransfer(self.json.get('latestTransferOrder', {}))
		self.regularAccount = self.Account(self.json.get('regularAccount', {}))
		self.storeAccount = self.Account(self.json.get('storeAccount', {}))

	class LatestTransfer:
		def __init__(self, data: dict = {}):
			self.json = data

			extensions = self.json.get('extensions', {})

			self.orderId = self.json.get('orderId', None)
			self.orderType = self.json.get('orderType', None)
			self.currencyType = self.json.get('currencyType', None)
			self.orderStatus = self.json.get('orderStatus', None)
			self.fromUid = self.json.get('fromUid', None)
			self.toUid = self.json.get('toUid', None)
			self.amount = self.json.get('amount', None)
			self.duration = self.json.get('duration', None)
			self.minClaimedTime = self.json.get('minClaimedTime', None)
			self.createdTime = self.json.get('createdTime', None)
			self.returnTime = self.json.get('returnTime', None)
			self.giftBoxId = extensions.get('status', None)
			self.expiredTime = self.json.get('expiredTime', None)
			self.currency = self.Currency(self.json.get('currency', {}))


		class Currency:
			def __init__(self, data: dict = {}):
				self.json = data
				self.name = self.json.get('name', None)
				self.symbol = self.json.get('symbol', None)
				self.icon = Media(self.json.get('icon', {}))
				self.decimals = self.json.get('decimals', None)
				self.currencyType = self.json.get('currencyType', None)
				self.amount = self.json.get('amount', None)





	class Account:
		def __init__(self, data: dict = {}):
			self.json = data
			self.accountId = self.json.get('accountId', None)
			self.accountType = self.json.get('accountType', None)
			self.status = self.json.get('status', None)
			self.createdTime = self.json.get('createdTime', None)
			self.ownerId = self.json.get('ownerId', None)
			self.ownerType = self.json.get('ownerType', None)
			self.currencyList = self.json.get('currencyList', None)




class ChatInfo:
	def __init__(self, data: dict = {}):
		self.json = data



class CircleInfo:
	def __init__(self, data: dict = {}):
		self.json = data


class Comments:
	def __init__(self, data: dict = {}):
		self.json = data



class MentionCandidates:
	def __init__(self, data: dict = {}):
		self.json = data


class Blogs:
	def __init__(self, data: dict = {}):
		self.json = data



class Baners:
	def __init__(self, data: dict = {}):
		self.json = data


class Nfts:
	def __init__(self, data: dict = {}):
		self.json = data