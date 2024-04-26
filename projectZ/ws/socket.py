from websocket import WebSocketApp, enableTrace
from websocket import _exceptions as WSexceptions
from threading import Thread
from ujson import loads, dumps
from time import sleep

from ..objects.constants import (
	ws_url, ws_endpoint, LoggerLevel,
	log_level_string, ws_ping_interval, SocketEventTypes
)

from ..utils.exceptions import NotLoggined
from ..objects.objects import Event
from ..objects.ws_types import *


class WsMessageHandler:
	handlers = {}

	def call(self, data: dict):
		data = Event(data)
		method = message_methods.get(data.json['msg']['type'])
		if method in self.handlers.keys():
			for func in self.handlers[method]:
				try:func(data)
				except Exception as e:
					print(f"[event][{func}]Error: {e}")

	def event(self, type: str):
		def registerHandler(handler):
			if type in self.handlers:self.handlers[type].append(handler)
			else:self.handlers[type] = [handler]
			return handler
		return registerHandler



class WsRequester:
	pass


class Socket(WsMessageHandler, WsRequester):
	active = False

	def __init__(self, debug: LoggerLevel = LoggerLevel.WARNING, sock_trace: bool = False):
		self.socket = None
		self.debug=debug
		enableTrace(sock_trace)
	

	def socket_log(self, message: str, level: LoggerLevel = LoggerLevel.INFO):
		if level >= self.debug and level != LoggerLevel.OFF:
			print(f"[Socket][{log_level_string.get(level, 'UNKNOWN')}]{message}")

	def ws_resolve(self, ws, data):
		try:data = loads(data)
		except:
			self.socket_log(f"[recive] The socket received an unreadable message: {data}", LoggerLevel.DEBUG)
			return
		self.socket_log(f"[recive]: {data}", LoggerLevel.DEBUG)
		if data["t"] == SocketEventTypes.MESSAGE.value:self.call(data)
		elif data["t"] == SocketEventTypes.ACK.value:
			ack = data["serverAck"]
			print(ack)



	def ws_on_close(self, ws, data, status):
		self.socket_log(f"[close] Socket closed: {data} [status: {status}]", LoggerLevel.DEBUG)

	def ws_on_error(self, ws, error):
		self.socket_log(f"[on_error]: {error}", LoggerLevel.ERROR)

	def ws_on_open(self, ws):
		self.active = True
		self.socket_log(f"[start] Socket Started", LoggerLevel.INFO)

	def ws_connect(self, headers: dict):
		if self.socket or self.active:
			self.socket_log(f"[start] The socket is already running.", LoggerLevel.WARNING)
			return
		try:
			self.socket = WebSocketApp(
				f"{ws_url}{ws_endpoint}",
				header = headers,
				on_message=self.ws_resolve,
				on_open=self.ws_on_open,
				on_error=self.ws_on_error,
				on_close=self.ws_on_close,
			)
			Thread(target=self.socket.run_forever, kwargs={
				"ping_interval": ws_ping_interval,
				"ping_payload": '{"t": 8}'
			}).start()
		except Exception as e:
			self.socket_log(f"[start] Error while starting Socket : {e}", LoggerLevel.ERROR)


	def ws_disconnect(self):
		if self.socket or self.active:
			self.socket_log(f"[stop] closing socket...", LoggerLevel.INFO)
			try:
				self.socket.close()
				self.active = False
			except Exception as e:
					self.socket_log(f"[stop] Error while closing Socket : {e}", LoggerLevel.ERROR)
		else:
			self.socket_log(f"[stop] Socket not running.", LoggerLevel.WARNING)

	def ws_send(self, req_t: int, **kwargs):
		if not self.active:raise NotLoggined('You are not logged in')
		data = dumps(dict(t=req_t, **kwargs))
		self.socket_log(f"[send] Sending Data : {data}", LoggerLevel.DEBUG)
		try:return self.socket.send(data)
		except WSexceptions.WebSocketConnectionClosedException:
			self.socket_log(f"[send] Socket not available : {data}", LoggerLevel.ERROR)