from time import time
from uuid import uuid4

class Headers:
	def __init__(self, deviceId: str, sid: str = None, time_zone: int = 180, country_code: str = "en", language: str = "en-US"):
		self.sid = sid
		self.deviceId = deviceId
		self.time_zone = time_zone
		self.country_code = country_code
		self.language = language

	def Headers(self):

		headers = {
			"rawDeviceId": self.deviceId,
			"nonce": str(uuid4()),
			"Accept-Language": self.language,
			"countryCode": self.country_code.upper(),
			"carrierCountryCodes": self.country_code,
			"timeZone": str(self.time_zone),
			"reqTime": str(int(time() * 1000)),
			"sId": self.sid if self.sid else ''
		}

		return headers

	def get_persistent_headers(self) -> dict: return {
		"appType": "MainApp", "appVersion": "2.3.1",
		"osType": "1", "deviceType": "1", "flavor": "google",
		"User-Agent": "com.projz.z.android/1.24.7-13774 (Linux; U; Android 7.1.2; ASUS_Z01QD; Build/Asus-user 7.1.2 2017)"
	}