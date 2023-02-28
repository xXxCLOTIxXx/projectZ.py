
class Icon:
	def __init__(self, data: dict = {}):
		self.json = data
		self.mediaId = self.json.get('mediaId', None)
		self.baseUrl = self.json.get('baseUrl', None)
		self.resourceList = self.json.get('resourceList', None)



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
		self.icon = Icon(author.get('icon', {}))
		self.adminPartyOnlineStatus = authorExtensions.get('adminPartyOnlineStatus', None)
		self.bubbleColor = msg.get('bubbleColor', None)
		self.ref = msg.get('ref', {})