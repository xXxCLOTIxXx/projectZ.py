from io import BytesIO


class CopyToBufferWriter:
	def __init__(self, buffer: BytesIO):
		self.buffer = buffer

	async def write(self, data: bytes):
		self.buffer.write(data)



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



class Message:
	def __init__(self, data: dict = {}):
		self.json = data
		self.chatId = self.json.get("threadId", None)
		self.messageId = self.json.get("messageId", None)
		self.userId = self.json.get("uid", None)
		self.createdTime = self.json.get("createdTime", None)
		self.type = self.json.get("type", None)
		self.seqId = self.json.get("seqId", None)
		self.content = self.json.get("content", None)
		self.extensions = self.json.get("extensions", None)
		self.richFormat = self.json.get("richFormat", None)
		self.author = self.Author(self.json.get("richFormat", {}))

	class Author:
		def __init__(self, data: dict = {}):
			self.json = data
			self.userId = self.json.get("uid", None)
			self.nickname = self.json.get("nickname", None)
			self.gender = self.json.get("gender", None)
			self.status = self.json.get("status", None)
			self.icon = Media(self.json.get("icon", {}))
			self.extensions = self.json.get("extensions", None)


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



class UserProfile:
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
		self.followMeStatus = self.json.get('followMeStatus', None)
		self.followedByMeStatus = self.json.get('followedByMeStatus', None)
		self.followedByMeStatusV2 = self.json.get('followedByMeStatusV2', None)
		self.language = self.json.get('language', None)
		self.bio = self.json.get('bio', None)
		self.nameCardBackground = Media(self.json.get('nameCardBackground', {}))
		self.background = Media(self.json.get('background', {}))


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
		self.owner = UserProfile(self.json.get('owner', {}))



class WalletInfo:
	def __init__(self, data: dict = {}):
		self.json = data
		self.userId = self.json.get('uid', None)
		self.activateStatus = self.json.get('activateStatus', None)
		self.status = self.json.get('status', None)
		self.createdTime = self.json.get('createdTime', None)
		self.walletExtension = self.json.get('walletExtension', {})
		self.unreadTransferOrderCount = self.json.get('unreadTransferOrderCount', None)
		self.latestTransferOrder = LatestTransfer(self.json.get('latestTransferOrder', {}))
		self.regularAccount = self.Account(self.json.get('regularAccount', {}))
		self.storeAccount = self.Account(self.json.get('storeAccount', {}))

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




class ChatInfo:
	def __init__(self, data: dict = {}):
		self.json = data
		self.chatId = self.json.get('threadId', None)
		self.status = self.json.get('status', None)
		self.type = self.json.get('type', None)
		self.hostId = self.json.get('hostUid', None)
		self.title = self.json.get('title', None)
		self.icon = Media(self.json.get('icon', {}))
		self.content = self.json.get('content', None)
		self.latestMessageId = self.json.get('latestMessageId', None)
		self.membersCount = self.json.get('membersCount', None)
		self.allMembersCount = self.json.get('allMembersCount', None)
		self.contentRegion = self.json.get('contentRegion', None)
		self.background = Media(self.json.get('background', {}))
		self.welcomeMessage = self.json.get('welcomeMessage', None)
		self.createdTime = self.json.get('createdTime', None)
		self.updatedTime = self.json.get('updatedTime', None)
		self.language = self.json.get('language', None)
		self.visibility = self.json.get('visibility', None)
		self.rolesCount = self.json.get('rolesCount', None)
		self.qiVotedCount = self.json.get('qiVotedCount', None)
		self.usingRoleCount = self.json.get('usingRoleCount', None)
		self.talkingMemberCount = self.json.get('talkingMemberCount', None)
		self.roleplayerCount = self.json.get('roleplayerCount', None)
		self.mentionedBy = self.json.get('mentionedBy', None)
		self.plt = self.json.get('plt', None)
		self.category = self.json.get('category', None)
		self.extensions = self.json.get('extensions', None)
		self.currentMemberInfo = self.CurrentMemberInfo()
		self.latestMessage = Message(self.json.get('latestMessage', {}))
		self.host = UserProfile(self.json.get('host', {}))
		self.membersList = list()

		for member in self.json.get('membersSummary', []):
			self.membersList.append(UserProfile(member))


	class CurrentMemberInfo:
		def __init__(self, data: dict = {}):
			self.json = data

			extensions = self.json.get('extensions', {})

			self.chatMemberStatus = self.json.get('chatMemberStatus', None)
			self.chatMemberStatusV2 = self.json.get('chatMemberStatusV2', None)
			self.alertOption = self.json.get('alertOption', None)
			self.lastReadMessageId = self.json.get('lastReadMessageId', None)
			self.createdTime = self.json.get('createdTime', None)
			self.joinedTimeMs = self.json.get('joinedTimeMs', None)
			self.bubbleColor = extensions.get('bubbleColor', None)

class Comments:
	def __init__(self, data: dict = {}):
		self.json = data



class MentionCandidates:
	def __init__(self, data: dict = {}):
		self.json = data


class Blogs:
	def __init__(self, data: dict = {}):
		self.json = data



class BlockedUsers:
	def __init__(self, data: dict = {}):
		self.json = data




class Baners:
	def __init__(self, data: dict = {}):
		self.json = data
		self.showAtTop = self.json.get("showAtTop", None)
		self.banersList = list()
		for baner in self.json.get("list", {}):
			self.banersList.append(self.Baner(baner))


	class Baner:
		def __init__(self, data: dict = {}):
			self.json=data
			self.bannerId = self.json.get("bannerId", None)
			self.scenario = self.json.get("scenario", None)
			self.targetUrl = self.json.get("targetUrl", None)
			self.status = self.json.get("status", None)
			self.createdTime = self.json.get("createdTime", None)
			self.creatorId = self.json.get("creatorUid", None)
			self.position = self.json.get("position", None)
			self.contentRegion = self.json.get("contentRegion", None)
			self.note = self.json.get("note", None)
			self.bannerImage = Media(self.json.get("bannerImage", {}))




class Nfts:
	def __init__(self, data: dict = {}):
		self.json = data
		self.count = self.json.get("count", None)


class CirclesList:
	def __init__(self, data: dict = {}):
		self.json = data

		pagination = self.json.get("pagination", {})
		
		self.totalPages = pagination.get("total", None)
		self.nextPageToken = pagination.get("nextPageToken", None)
		self.categoryList = list()
		self.circlesList = list()

		for circle in self.json.get("list", []):
			self.circlesList.append(Circle(circle))

		for category in self.json.get("list", []):
			self.categoryList.append(Category(category))

class Circle:
	def __init__(self, data: dict = {}):
		self.json = data

		sInfo = self.json.get("sInfo", {})

		self.extensions = self.json.get("extensions", {})
		self.status = self.json.get("status", None)
		self.createdTime = self.json.get("createdTime", None)
		self.contentRegion = self.json.get("contentRegion", None)
		self.circleId = self.json.get("circleId", None)
		self.categoryId = self.json.get("categoryId", None)
		self.conceptId = self.json.get("conceptId", None)
		self.socialId = self.json.get("socialId", None)
		self.socialIdModified = self.json.get("socialIdModified", None)
		self.updatedTime = self.json.get("updatedTime", None)
		self.verifiedStatus = self.json.get("verifiedStatus", None)
		self.name = self.json.get("name", None)
		self.tagline = self.json.get("tagline", None)
		self.language = self.json.get("language", None)
		self.membersCount = self.json.get("membersCount", None)
		self.dailyActiveUser = self.json.get("dailyActiveUser", None)
		self.dailyNewPostCount = self.json.get("dailyNewPostCount", None)
		self.privacy = self.json.get("privacy", None)
		self.joinPermission = self.json.get("joinPermission", None)
		self.visibility = self.json.get("visibility", None)
		self.discoverability = self.json.get("discoverability", None)
		self.themeColor = self.json.get("themeColor", None)
		self.joinedStatus = self.json.get("joinedStatus", None)
		self.uid = self.json.get("uid", None)
		self.rootFolderId = self.json.get("rootFolderId", None)
		self.recallType = sInfo.get("recallType", None)
		self.background = Media(self.json.get("background", {}))
		self.description = self.json.get("description", None)
		self.icon = Media(self.json.get("icon", {}))
		self.cover = Media(self.json.get("cover", {}))
		self.circleIcon = Media(self.json.get("circleIcon", {}))
		self.tagList = list()

		for tag in self.json.get("tagList", []):
			self.tagList.append(Tag(tag))

class Tag:
	def __init__(self, data: dict = {}):
		self.json = data

		style = self.json.get("style", {})

		self.tagId = self.json.get("tagId", None)
		self.tagName = self.json.get("tagName", None)
		self.source = self.json.get("source", None)
		self.status = self.json.get("status", None)
		self.order = self.json.get("order", None)
		self.backgroundColor = style.get("backgroundColor", None)
		self.textColor = style.get("textColor", None)
		self.borderColor = style.get("borderColor", None)
		self.solidColor = style.get("solidColor", None)



class Category:
	def __init__(self, data: dict = {}):
		self.json = data

		sticker = self.json.get("sticker", {})
		tagInfo = self.json.get("tagInfo", {})
		tagStyle = tagInfo.get("style", {})

		self.categoryId = self.json.get("categoryId", None)
		self.stickerId = self.json.get("stickerId", None)
		self.name = self.json.get("name", None)
		self.title = self.json.get("title", None)
		self.lowerCaseName = self.json.get("lowerCaseName", None)
		self.contentRegion = self.json.get("contentRegion", None)
		self.status = self.json.get("status", None)
		self.objectType = self.json.get("objectType", None)
		self.score = self.json.get("score", None)
		self.createdTime = self.json.get("createdTime", None)
		self.conceptId = self.json.get("conceptId", None)
		self.conceptName = self.json.get("conceptName", None)
		self.categoryConcept = self.json.get("createdTime", None)
		self.extensions = self.json.get("extensions", None)
		self.stickerId = sticker.get("stickerId", None)
		self.stickerName = sticker.get("name", None)
		self.stickerMedia = Media(sticker.get("media", {}))
		self.tagId = tagInfo.get("tagId", None)
		self.tagName = tagInfo.get("tagName", None)
		self.tagTitle = tagInfo.get("title", None)
		self.tagLowerCaseName = tagInfo.get("lowerCaseName", None)
		self.languageCode = tagInfo.get("languageCode", None)
		self.tagStatus = tagInfo.get("status", None)
		self.officialVerified = tagInfo.get("officialVerified", None)
		self.tagType = tagInfo.get("tagType", None)
		self.tagCreatedTime = tagInfo.get("createdTime", None)
		self.tagBackgroundColor = tagStyle.get("backgroundColor", None)
		self.tagTextColor = tagStyle.get("textColor", None)
		self.tagBorderColor = tagStyle.get("borderColor", None)
		self.tagSolidColor = tagStyle.get("solidColor", None)


class invitationCode:
	def __init__(self, data: dict = {}):
		self.json = data
		self.userId = self.json.get("uid", None)
		self.code = self.json.get("code", None)
		self.createdTime = self.json.get("createdTime", None)
		self.status = self.json.get("status", None)
		self.label = self.json.get("label", None)
		self.generation = self.json.get("generation", None)
		self.operatorUid = self.json.get("operatorUid", None)
		self.type = self.json.get("type", None)
		self.totalUsedCount = self.json.get("totalUsedCount", None)
		self.usedCount = self.json.get("usedCount", None)


class CirclesMembers:
	def __init__(self, data: dict = {}):
		self.json = data

		pagination = self.json.get("pagination", None)

		self.nextPageToken = pagination.get("nextPageToken", None)
		self.members = list()
		for member in self.json.get("list", []):
			self.members.append(UserProfile(member))


class OrderInfo:
	def __init__(self, data: dict = {}):
		self.json = data
		self.logId = self.json.get("logId")
		self.userId = self.json.get("uid")
		self.checkInDate = self.json.get("checkInDate")
		self.orderId = self.json.get("orderId")
		self.continuousCheckInDays = self.json.get("continuousCheckInDays")
		self.createdTime = self.json.get("createdTime")
		self.checkInDateUnix = self.json.get("checkInDateUnix")
		self.nextMultipleStr = self.json.get("nextMultipleStr")
		self.needDays = self.json.get("needDays")
		self.decimals = self.json.get("decimals")
		self.currencyType = self.json.get("currencyType")
		self.currency = self.json.get("currency", {})
		self.amount = self.currency.get("amount")



class Gifts:
	def __init__(self, data: dict = {}):
		self.json = data
		self.pagination = self.json.get("pagination")
		self.gifts = list()
		for gift in self.json.get("list", []):
			self.gifts.append(LatestTransfer(gift))