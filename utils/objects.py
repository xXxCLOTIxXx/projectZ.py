

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