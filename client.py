from typing import Union
from .utils import exceptions, generator, headers, objects
from json import dumps, loads
from requests import Session

gen = generator.Generator()

class Client:
	def __init__(self, deviceId: str = None, proxies: dict = None, language: str = "en-US", country_code: str = "en", time_zone: int = 180):
		self.api = 'https://api.projz.com'
		self.web_api = 'https://www.projz.com'
		self.session = Session()
		self.proxies = None
		self.deviceId = deviceId if deviceId else gen.deviceId()
		self.profile = objects.User()

		self.language = language
		self.country_code = country_code
		self.time_zone = time_zone


	def parse_headers(self, endpoint: str, data = None, content_type: str = 'application/json') -> dict:
		h = headers.Headers(deviceId=self.deviceId, sid=self.profile.sid, time_zone=self.time_zone, country_code=self.country_code, language=self.language)
		head = h.get_persistent_headers()
		head.update(h.Headers())
		head.update({"Content-Type": content_type} if content_type else {})
		head["HJTRFS"] = gen.signature(path=endpoint, headers=head, body=data or bytes())
		return head

	def set_proxies(self, proxy = None):
		if type(proxy) == type({}):
			self.proxies = proxy
		elif type(proxy) == type(''):
			self.proxies={"http": proxy, "https": proxy}
		elif type(proxy) == type(None):
			self.proxies=None
		else:
			raise exceptions.WrongType(type(proxy))

	def login(self, email: str, password: str):

		data = dumps({
			"authType": 1,
			"email": email,
			"password": password
		})
		endpoint = '/v1/auth/login'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		if response.status_code != 200:return exceptions.CheckException(response.text)
		else:
			self.profile = objects.User(loads(response.text))
			return self.profile.User

	def logout(self):

		endpoint = '/v1/auth/logout'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		self.profile = objects.User()
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code


	def join_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def leave_chat(self, chatId: int) -> None:

		endpoint = f'/v1/chat/threads/{chatId}/members'
		response = self.session.delete(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint), proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else response.status_code

	def get_from_link(self, link: str):
		data = dumps({"link": link})

		endpoint = f"/v1/links/path"
		response = self.session.post(f"{self.api}{endpoint}", headers=self.parse_headers(endpoint=endpoint, data=data), data=data, proxies=self.proxies)
		return exceptions.CheckException(response.text) if response.status_code != 200 else objects.FromLink(loads(response.text)).FromLink


