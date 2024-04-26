from aiohttp import ClientSession, WSMsgType, ClientWebSocketResponse
from asyncio import sleep, create_task
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

	async def call(self, data: dict):
		data = Event(data)
		method = message_methods.get(data.json['msg']['type'])
		if method in self.handlers.keys():
			for func in self.handlers[method]:
				try:await func(data)
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

class AsyncSocket(WsMessageHandler, WsRequester):

	def __init__(self, debug: LoggerLevel = LoggerLevel.WARNING):
		self.connection: ClientWebSocketResponse = None
		self.task_receiver = None
		self.task_pinger = None
		self.client_session = None
		self.debug=debug
	

	async def socket_log(self, message: str, level: LoggerLevel = LoggerLevel.INFO):
		if level >= self.debug and level != LoggerLevel.OFF:
			print(f"[Socket][{log_level_string.get(level, 'UNKNOWN')}]{message}")

	async def ws_resolve(self):
		while True:
			msg = await self.connection.receive()
			if msg.type != WSMsgType.TEXT: continue
			try:data = loads(msg.data)
			except:
				await self.socket_log(f"[recive] The socket received an unreadable message: {data}", LoggerLevel.DEBUG)
				return


			await self.socket_log(f"[recive]: {data}", LoggerLevel.DEBUG)
			if data["t"] == SocketEventTypes.MESSAGE.value:await self.call(data)
			elif data["t"] == SocketEventTypes.ACK.value:
				ack = data["serverAck"]
				#print(ack)

	async def ws_connect(self, headers: dict):
		if self.connection:
			await self.socket_log(f"[start] The socket is already running.", LoggerLevel.WARNING)
			return
		try:
			self.client_session = ClientSession(base_url=ws_url)
			self.connection = await self.client_session.ws_connect(ws_endpoint, headers=headers)
			self.task_receiver = create_task(self.ws_resolve())
			self.task_pinger = create_task(self.ws_ping())
			await self.socket_log(f"[start] Socket Started", LoggerLevel.INFO)
		except Exception as e:
			await self.socket_log(f"[start] Error while starting Socket : {e}", LoggerLevel.ERROR)


	async def ws_disconnect(self):
		if self.connection:
			await self.socket_log(f"[stop] closing socket...", LoggerLevel.INFO)
			try:
				self.task_receiver.cancel()
				self.task_pinger.cancel()
				await self.connection.close()
				self.connection = None
				await self.client_session.close()
				self.client_session = None
			except Exception as e:
					await self.socket_log(f"[stop] Error while closing Socket : {e}", LoggerLevel.ERROR)
		else:
			await self.socket_log(f"[stop] Socket not running.", LoggerLevel.WARNING)

	async def ws_send(self, req_t: int, **kwargs):
		if self.connection is None:raise NotLoggined('The socket is not running')
		data = dumps(dict(t=req_t, **kwargs))
		await self.socket_log(f"[send] Sending Data : {data}", LoggerLevel.DEBUG)
		try:return await self.connection.send_str(data)
		except:await self.socket_log(f"[send] Socket not available : {data}", LoggerLevel.ERROR)



	async def ws_ping(self):
		while True:
			await sleep(ws_ping_interval)
			await self.ws_send(8)