from typing import Optional, Union
from requests import Session
from aiohttp import ClientSession, MultipartWriter
from io import BytesIO
from ujson import dumps
from time import time
from uuid import uuid4
from ujson import loads


from .objects.constants import (
	api_url, web_api_url, get_persistent_headers
)
from .objects.objects import CopyToBufferWriter
from .objects.profile import profile as auth
from .utils.generator import gen_signature
from .utils.exceptions import CheckException

class requester:
	session = Session()
	profile: auth
	def __init__(self, profile_data: auth):
		self.profile=profile_data

	def request(self, method: str, endpoint: str, body: Union[bytes, str, dict] = None, content_type: Optional[str] = "application/json; charset=UTF-8", web: bool = False, successful_code: int = 200) -> dict:
		if not endpoint.startswith("/"): endpoint = f"/{endpoint}"
		if web: endpoint = f"/api/f{endpoint}"
		if body:
			content = BytesIO()
			if isinstance(body, bytes): content.write(body)
			elif isinstance(body, str): content.write(body.encode("utf-8"))
			elif isinstance(body, dict): content.write(dumps(body).encode("utf-8"))
			else: raise ValueError(f"Invalid request body type: \"{body.__class__.__name__}\"")
			body = content.getvalue()
		result = self.session.request(method, f"{web_api_url if web else api_url}{endpoint}", data=body, headers=self.build_headers(
			endpoint=endpoint,
			body=body,
			content_type=content_type
		) if not web else dict())
		return CheckException(result.text) if result.status_code != successful_code else result.json()


	def build_headers(self, endpoint: str, body: Optional[bytes] = None, content_type: str = None) -> dict:
		headers = get_persistent_headers()
		headers.update({
			"rawDeviceId": self.profile.deviceId,
			"nonce": str(uuid4()),
			"Accept-Language": self.profile.language,
			"countryCode": self.profile.country_code.upper(),
			"carrierCountryCodes": self.profile.country_code,
			"timeZone": str(self.profile.time_zone),
			"reqTime": str(int(time() * 1000)),
		})
		if self.profile.sid is not None: headers["sId"] = self.profile.sid
		headers.update({"Content-Type": content_type} if content_type else {})
		headers["HJTRFS"] = gen_signature(path=endpoint, headers=headers, body=body or bytes())
		return headers


class AsyncRequester:
	session = ClientSession()
	profile: auth
	def __init__(self, profile_data: auth):
		self.profile=profile_data


	async def request(self, method: str, endpoint: str, body: Union[bytes, str, dict, MultipartWriter] = None, content_type: Optional[str] = "application/json; charset=UTF-8", web: bool = False, successful_code: int = 200) -> dict:
		if not endpoint.startswith("/"): endpoint = f"/{endpoint}"
		if web: endpoint = f"/api/f{endpoint}"
		if body:
			content = BytesIO()
			if isinstance(body, bytes): content.write(body)
			elif isinstance(body, str): content.write(body.encode("utf-8"))
			elif isinstance(body, dict): content.write(dumps(body).encode("utf-8"))
			elif isinstance(body, MultipartWriter): await body.write(CopyToBufferWriter(content))
			else: raise ValueError(f"Invalid request body type: \"{body.__class__.__name__}\"")
			body = content.getvalue()
		result = await self.session.request(method, f"{web_api_url if web else api_url}{endpoint}", data=body, headers=self.build_headers(
			endpoint=endpoint,
			body=body,
			content_type=content_type
		) if not web else dict())
		return CheckException(await result.text()) if result.status != successful_code else loads(await result.text())



	def build_headers(self, endpoint: str, body: Optional[bytes] = None, content_type: str = None) -> dict:
		headers = get_persistent_headers()
		headers.update({
			"rawDeviceId": self.profile.deviceId,
			"nonce": str(uuid4()),
			"Accept-Language": self.profile.language,
			"countryCode": self.profile.country_code.upper(),
			"carrierCountryCodes": self.profile.country_code,
			"timeZone": str(self.profile.time_zone),
			"reqTime": str(int(time() * 1000)),
		})
		if self.profile.sid is not None: headers["sId"] = self.profile.sid
		headers.update({"Content-Type": content_type} if content_type else {})
		headers["HJTRFS"] = gen_signature(path=endpoint, headers=headers, body=body or bytes())
		return headers