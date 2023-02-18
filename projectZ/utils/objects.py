
class Icon:
	def __init__(self, data: dict = None):
		self.json = data
		try:self.mediaId = self.json['mediaId']
		except:self.mediaId = None
		try:self.baseUrl = self.json['baseUrl']
		except:self.baseUrl = None
		try:self.resourceList = self.json['resourceList']
		except:self.resourceList = None



class User:
	def __init__(self, data: dict = None):
		self.json = data
		self.sid = None
		self.email = None
		self.secret = None
		self.uid = None
		self.createdTime = None
		self.deviceId = None
		self.googleId = None
		self.nickname = None
		self.socialId = None
		self.gender = None
		self.socialIdModified = None

	@property
	def User(self):
		try:self.sid = self.json['sId']
		except:pass
		try:self.secret = self.json['secret']
		except:pass
		try:self.uid = self.json['account']['uid']
		except:pass
		try:self.email = self.json['account']['email']
		except:pass
		try:self.createdTime = self.json['account']['createdTime']
		except:pass
		try:self.deviceId = self.json['account']['deviceId']
		except:pass
		try:self.googleId = self.json['account']['googleId']
		except:pass
		try:self.nickname = self.json['userProfile']['nickname']
		except:pass
		try:self.socialId = self.json['userProfile']['socialId']
		except:pass
		try:self.gender = self.json['userProfile']['gender']
		except:pass
		try:self.socialIdModified = self.json['userProfile']['socialIdModified']
		except:pass

		return self


class FromLink:
	def __init__(self, data):
		self.json = data
		self.path = None
		self.objectId = None
		self.objectType = None
		self.parentId = None
		self.parentType = None
		self.shareLink = None


	@property
	def FromLink(self):
		try:self.path = self.json['path']
		except:pass
		try:self.objectId = self.json['objectId']
		except:pass
		try:self.objectType = self.json['objectType']
		except:pass
		try:self.parentId = self.json['parentId']
		except:pass
		try:self.parentType = self.json['parentType']
		except:pass
		try:self.shareLink = self.json['shareLink']
		except:pass

		return self


class ThreadList:
	def __init__(self, data):
		self.json = data
		self.threadId = []
		self.title = []
		self.hostUid = []

	@property
	def ThreadList(self):
		for thread in self.json:
			self.threadId.append(thread['threadId'])
			self.hostUid.append(thread['hostUid'])
			self.title.append(thread['title'])


		return self

class Thread:
	def __init__(self, data):
		self.json = data
		self.beMentionedThreadIdList = None
		self.isEnd = None
		self.ThreadList = None
		self.threadCheckList = None

	@property
	def Thread(self):
		try:self.beMentionedThreadIdList = self.json['beMentionedThreadIdList']
		except:pass
		try:self.isEnd = self.json['isEnd']
		except:pass
		try:self.ThreadList = ThreadList(self.json['list']).ThreadList
		except:pass
		try:self.threadCheckList = self.json['threadCheckList']
		except:pass

		return self


class Event:
	def __init__(self, data):
		self.json = data
		self.type = None
		self.threadId = None
		self.messageId = None
		self.userId = None
		self.createdTime = None
		self.messageType = None
		self.asSummary = None
		self.seqId = None
		self.content = None
		self.roleContentStatus = None
		self.richFormatVersion = None
		self.nickname = None
		self.gender = None
		self.status = None
		self.icon = None
		self.adminPartyOnlineStatus = None
		self.bubbleColor = None
		self.ref = None





	@property
	def Event(self):
		try:self.type = self.json['t']
		except:pass
		try:self.threadId = self.json['msg']['threadId']
		except:pass
		try:self.messageId = self.json['msg']['messageId']
		except:pass
		try:self.userId = self.json['msg']['author']['uid']
		except:pass
		try:self.createdTime = self.json['msg']['createdTime']
		except:pass
		try:self.messageType = self.json['msg']['type']
		except:pass
		try:self.asSummary = self.json['msg']['asSummary']
		except:pass
		try:self.seqId = self.json['msg']['seqId']
		except:pass
		try:self.content = self.json['msg']['content']
		except:pass
		try:self.roleContentStatus = self.json['msg']['extensions']['roleContentStatus']
		except:pass
		try:self.richFormatVersion = self.json['msg']['richFormat']['version']
		except:pass
		try:self.nickname = self.json['msg']['author']['nickname']
		except:pass
		try:self.gender = self.json['msg']['author']['gender']
		except:pass
		try:self.status = self.json['msg']['author']['status']
		except:pass
		try:self.icon = Icon(self.json['msg']['author']['icon'])
		except:pass
		try:self.adminPartyOnlineStatus = self.json['msg']['author']['extensions']['adminPartyOnlineStatus']
		except:pass
		try:self.bubbleColor = self.json['msg']['bubbleColor']
		except:pass
		try:self.ref = self.json['msg']['ref']
		except:pass

		return self