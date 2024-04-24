from hashlib import sha1, sha256 
from hmac import HMAC
from base64 import b64encode, urlsafe_b64encode
from typing import Optional
from os import urandom
from uuid import uuid4
from io import BytesIO
from ujson import dumps
from json import loads 

class Generator:
	def __init__(self):
		self.prefix = bytes.fromhex("04")
		self.SIG_KEY = bytes.fromhex("ce070279278de1b6390b76942c13a0b0aa0fda6aedd6f2d655eda7cf6543b35f" + ("6a" * 32))
		self.DEVICE_KEY = bytes.fromhex("997ec928a85f539e3fa124761e7572ef852e")

	def get_signable_header_keys(self) -> list[str]: return [
		"rawDeviceId", "rawDeviceIdTwo", "rawDeviceIdThree",
		"appType", "appVersion", "osType",
		"deviceType", "sId", "countryCode",
		"reqTime", "User-Agent", "contentRegion",
		"nonce", "carrierCountryCodes"
	]



	def signature(self, path: str, headers: dict, body) -> str:
		headers = {'appType': 'MainApp', 'appVersion': '2.27.1', 'osType': '2', 'deviceType': '1', 'flavor': 'google', 'User-Agent': 'com.projz.z.android/2.27.1-25104 (Linux; U; Android 7.1.2; ASUS_Z01QD; Build/Asus-user 7.1.2 2017)', 'rawDeviceId': '04d953bc0e4af2f412ee7665456670345aa53a552d9c98c1474cc47361ecf7c02d097519bf1680efa5', 'nonce': '5f642562-dabc-440f-9b34-6b03c8277e72', 'Accept-Language': 'en-US', 'countryCode': 'US', 'carrierCountryCodes': 'us', 'timeZone': '180', 'reqTime': '1713991567051', 'sId': '', 'Content-Type': 'application/json; charset=UTF-8'}
		mac = HMAC(key=bytes.fromhex("ce070279278de1b6390b76942c13a0b0aa0fda6aedd6f2d655eda7cf6543b35f" + ("6a" * 32)),
				   msg=path.encode("utf-8"),
				   digestmod=sha256)
		for header in [headers[signable] for signable in self.get_signable_header_keys() if signable in headers]:
			mac.update(header.encode("utf-8"))
		if body:
			print(body)
			print(headers)
			c = BytesIO()
			c.write(dumps(loads(body)).encode("utf-8"))
			mac.update(c.getvalue())
		print(mac.digest())
		print(b64encode(self.prefix + mac.digest()).decode("utf-8"))
		return b64encode(self.prefix + mac.digest()).decode("utf-8")







	def deviceId(self, installation_id: str = None):
		if not installation_id:installation_id=str(uuid4())
		prefix = self.prefix + sha1(installation_id.encode("utf-8")).digest()
		return ( prefix + sha1( prefix + sha1(self.DEVICE_KEY).digest() ).digest() ).hex()


	def generate_device_id_three(self, data: Optional[dict] = None) -> str:
		raise Exception("Not supported")
