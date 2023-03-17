from hashlib import sha1, sha256 
from hmac import HMAC
from base64 import b64encode, urlsafe_b64encode
from typing import Optional
from os import urandom
from json import load, dumps
from uuid import uuid4

class Generator:
	def __init__(self):
		self.prefix = bytes.fromhex("01")
		self.SIG_KEY = bytes.fromhex("ebefcf164b887da7f924c948e1fc3e40faf230eb7d491c1de1150134b8517189")
		self.DEVICE_KEY = bytes.fromhex("dcfed9e64710da3a8458298424ff88e47375")

	def get_signable_header_keys(self) -> list[str]: return [
		"rawDeviceId", "rawDeviceIdTwo", "rawDeviceIdThree",
		"appType", "appVersion", "osType",
		"deviceType", "sId", "countryCode",
		"reqTime", "User-Agent", "contentRegion",
		"nonce", "carrierCountryCodes"
	]



	def _jwt_hs256(self, header: dict, data: dict, key: bytes) -> str:
		header_json = dumps(dict(alg="HS256", **header))
		data_json = dumps(data)
		body_str = f"{urlsafe_b64encode(header_json.encode('utf-8')).decode('utf-8')}" f".{urlsafe_b64encode(data_json.encode('utf-8')).decode('utf-8')}"

		sign = HMAC(key=key, msg=body_str.encode("utf-8"), digestmod=sha256).digest()
		return f"{body_str}.{urlsafe_b64encode(sign).decode('utf-8')}".replace("=", "")


	def signature(self, path: str, headers: dict, body) -> str:
		mac = HMAC(key=self.SIG_KEY, msg=path.encode("utf-8"), digestmod=sha256)
		for header in [headers[signable] for signable in self.get_signable_header_keys() if signable in headers]:
			mac.update(header.encode("utf-8"))
		if body: mac.update(body if isinstance(body, bytes) else body.encode("utf-8"))
		return b64encode(self.prefix + mac.digest()).decode("utf-8")

	def deviceId(self, installation_id: str = None):
		if not installation_id:installation_id=str(uuid4())
		prefix = self.prefix + sha1(installation_id.encode("utf-8")).digest()
		return ( prefix + sha1( prefix + sha1(self.DEVICE_KEY).digest() ).digest() ).hex()


	def generate_device_id_three(self, data: Optional[dict] = None) -> str:
		return "D" + self._jwt_hs256({
			"organization": "BU0gJ0gB5TFcCfN329Vx",
			"os": "android",
			"appId": "default",
			"encode": 1,
			"data": self._jwt_hs256(data or {
				"a1": "exception",
				"a6": "android",
				"a7": "3.0.6",
				"a2": "",
				"a10": "7.1.2",
				"a13": "ASUS_Z01QD",
				"a96": "BU0gJ0gB5TFcCfN329Vx",
				"a11": "default",
				"a98": b64encode("BU0gJ0gB5TFcCfN329Vx_bzcVDxF2PO"
								 "/ArnWpiOIWhT0WwjQ76FZ6BqAnhQpqI"
								 "OeGJYJvV5bcTZQ0lgjRQNAcyAqhRi7Ym"
								 "7tNesvah21ROA==".encode('utf-8')).decode("utf-8"),
				"e": "",
				"a97": "",
			}, {}, urandom(256)),
			"tn": "",
			"ep": "",
		}, {}, urandom(256))