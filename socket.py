from websocket import WebSocketApp, enableTrace
from .utils import exceptions
from threading import Thread
from time import sleep
from json import dumps, loads
from .utils import objects

class Socket:
	def __init__(self, client, debug: bool = False, sock_trace: bool = False):
		self.socket_url = "wss://ws.projz.com"
		self.socket = None
		self.debug=debug

		self.client = client
		self.active = False
		enableTrace(sock_trace)


	def resolve(self, ws, data):
		data = loads(data)
		self.on_all(data)
		self.methods.get(data['t'])(data)

	def connect(self):
		try:
			if self.debug:
				print(f"[socket][start] Starting Socket")

			self.socket = WebSocketApp(
				f"{self.socket_url}/v1/chat/ws",
				header = self.client.parse_headers(endpoint='/v1/chat/ws'),
				on_message=self.resolve
			)
			self.socket_thread = Thread(target=self.socket.run_forever)
			self.socket_thread.start()
			self.active = True
			Thread(target=self.ping).start()
			
			if self.debug:
				print(f"[socket][start] Socket Started")
		except Exception as e:
			print(e)

	def disconnect(self):
		if self.debug:
			print(f"[socket][close] Closing Socket")
		try:
			self.socket.close()
			self.active = False
		except Exception as e:
			if self.debug:
				print(f"[socket][close] Error while closing Socket : {e}")
		return


	def ping(self):
		sleep(1.5)
		while self.active:
			self.send()
			sleep(3)


	def send(self, t: int = 8, data = None, threadId: int = None):
		
		if not self.socket_thread:
			raise exceptions.NotLoggined('You are not logged in')
		d = {'t': t}
		if threadId:d['threadId'] = threadId
		if data:d['msg'] = data
		if self.debug is True:
			print(f"[socket][send] Sending Data : {d}")
		self.socket.send(dumps(d))


class CallBacks:
	def __init__(self):

		self.handlers = {}

		self.methods = {
			1: self.on_text_message
		}


	def event(self, type: str):
		def registerHandler(handler):
			if type in self.handlers:
				self.handlers[type].append(handler)
			else:
				self.handlers[type] = [handler]
			return handler
		return registerHandler

	def call(self, type, data):
		if type in self.handlers:
			for handler in self.handlers[type]:
				handler(objects.Event(data).Event)


	def on_text_message(self, data): self.call(type='on_text_message', data=data)
	def on_all(self, data): self.call(type='on_all', data=data)