from aiohttp import ClientSession, WSMsgType
from .utils import objects, exceptions
from asyncio import create_task, sleep
from json import dumps, loads
from traceback import format_exc


class AsyncSocket:
	def __init__(self, headers, debug: bool = False):
		self.socket_url = "wss://ws.projz.com"
		self.debug=debug
		self.headers = headers

		self.task_resolve = None
		self.socket = None
		self.connection = None

		self.online_loop_active = None

	async def resolve(self):
		while True:
			msg = await self.connection.receive()
			data = loads(msg.data)
			await self.on_all(data)
			await self.methods.get(data['msg']['type'])(data)


	async def connect(self):
		try:
			if self.debug:
				print(f"[socket][start] Starting Socket")
			self.socket = ClientSession(base_url=self.socket_url)
			self.connection = await self.socket.ws_connect("/v1/chat/ws",headers=self.headers(endpoint='/v1/chat/ws'))
			self.task_resolve = create_task(self.resolve())
			if self.debug:
				print(f"[socket][start] Socket Started")
		except Exception as e:
			if self.debug:
				print(f"[socket][start] Error while starting Socket : {e}")


	async def disconnect(self):
		if self.debug:
			print(f"[socket][close] Closing Socket")
		try:
			if self.task_resolve: self.task_resolve.cancel()
			if self.online_loop_active: self.online_loop_active.cancel()
			if self.connection:
				await self.connection.close()
				self.connection = None
			if self.socket:
				await self.socket.close()
				self.socket = None
			if self.debug:
				print(f"[socket][close] Socket closed")
		except Exception as e:
			if self.debug:
				print(f"[socket][close] Error while closing Socket : {e}")


	async def online_loop(self):
		while True:
			try:
				await self.send()
			except Exception as e:
				if self.debug:
					print('[socket][_online_loop][error] ', e)
			await sleep(3)



	async def send(self, t: int = 8, data = None, threadId: int = None):
		d = {'t': t}
		if threadId:d['threadId'] = threadId
		if data:d['msg'] = data
		if self.debug is True:
			print(f"[socket][send] Sending Data : {d}")
		await self.connection.send_str(dumps(d))


class AsyncCallBacks:

	def __init__(self):

		self.handlers = {}

		self.methods = {
			1: self.on_text_message,
			2: self.on_image_message,
			3: self.on_audio_message,
			4: self.on_video_message,
			5: self.on_delete_message,
			10: self.on_user_join,
			11: self.on_user_leave,
			12: self.on_user_invite,
			13: self.on_user_kick,
			14: self.on_user_remove,
			15: self.on_cohost_remove,
			16: self.on_cohost_add,
			17: self.on_host_delete_message,
			18: self.on_cohost_delete_message,
			20: self.on_role_play_invite,
			21: self.on_free_talk_start,
			22: self.on_free_talk_end,
			23: self.on_role_play_start,
			24: self.on_role_play_end,
			25: self.on_voice_call_start,
			26: self.on_voice_call_end,
			27: self.on_voice_call_reject,
			28: self.on_voice_call_cancel,
			29: self.on_voice_call_accept,
			30: self.on_free_talk_add_user,
			31: self.on_free_talk_remove_user,
			32: self.on_free_talk_invite,
			33: self.on_free_talk_apply,
			34: self.on_free_talk_accept,
			35: self.on_live_talking_users,
			36: self.on_free_talk_apply_count,
			37: self.on_role_play_roles,
			38: self.on_role_play_role_update,
			39: self.on_role_play_apply_count,
			40: self.on_conversation_level,
			41: self.on_role_play_accept_apply,
			42: self.on_role_play_user_role_remove,
			43: self.on_chat_user_online,
			50: self.on_chat_delete,
			51: self.on_chat_host_update,
			53: self.on_chat_disable,
			60: self.on_user_typing,
			90: self.on_chat_activity_type,
			120: self.on_voice_call_not_answered,
		}


	def event(self, type: str):
		def registerHandler(handler):
			if type in self.handlers:
				self.handlers[type].append(handler)
			else:
				self.handlers[type] = [handler]
			return handler
		return registerHandler

	async def call(self, type, data):
		if type in self.handlers:
			for handler in self.handlers[type]:
				try:await handler(objects.Event(data))
				except:
					if self.debug:
						print("[event][call][error]Error calling your function:\n", format_exc(),'\n')

	async def on_text_message(self, data): await self.call(type='on_text_message', data=data)
	async def on_image_message(self, data): await self.call(type='on_image_message', data=data)
	async def on_audio_message(self, data): await self.call(type='on_audio_message', data=data)
	async def on_video_message(self, data): await self.call(type='on_video_message', data=data)
	async def on_delete_message(self, data): await self.call(type='on_delete_message', data=data)
	async def on_user_join(self, data): await self.call(type='on_user_join', data=data)
	async def on_user_leave(self, data): await self.call(type='on_user_leave', data=data)
	async def on_user_invite(self, data): await self.call(type='on_user_invite', data=data)
	async def on_user_kick(self, data): await self.call(type='on_user_kick', data=data)
	async def on_user_remove(self, data): await self.call(type='on_user_remove', data=data)
	async def on_cohost_remove(self, data): await self.call(type='on_cohost_remove', data=data)
	async def on_cohost_add(self, data): await self.call(type='on_cohost_add', data=data)
	async def on_host_delete_message(self, data): await self.call(type='on_host_delete_message', data=data)
	async def on_cohost_delete_message(self, data):await  self.call(type='on_cohost_delete_message', data=data)
	async def on_role_play_invite(self, data): await self.call(type='on_role_play_invite', data=data)
	async def on_free_talk_start(self, data): await self.call(type='on_free_talk_start', data=data)
	async def on_free_talk_end(self, data): await self.call(type='on_free_talk_end', data=data)
	async def on_role_play_start(self, data): await self.call(type='on_role_play_start', data=data)
	async def on_role_play_end(self, data): await self.call(type='on_role_play_end', data=data)
	async def on_voice_call_start(self, data): await self.call(type='on_voice_call_start', data=data)
	async def on_voice_call_end(self, data): await self.call(type='on_voice_call_end', data=data)
	async def on_voice_call_reject(self, data): await self.call(type='on_voice_call_reject', data=data)
	async def on_voice_call_cancel(self, data): await self.call(type='on_voice_call_cancel', data=data)
	async def on_voice_call_accept(self, data): await self.call(type='on_voice_call_accept', data=data)
	async def on_free_talk_add_user(self, data): await self.call(type='on_free_talk_add_user', data=data)
	async def on_free_talk_remove_user(self, data): await self.call(type='on_free_talk_remove_user', data=data)
	async def on_free_talk_invite(self, data): await self.call(type='on_free_talk_invite', data=data)
	async def on_free_talk_apply(self, data): await self.call(type='on_free_talk_apply', data=data)
	async def on_free_talk_accept(self, data): await self.call(type='on_free_talk_accept', data=data)
	async def on_live_talking_users(self, data): await self.call(type='on_live_talking_users', data=data)
	async def on_free_talk_apply_count(self, data): await self.call(type='on_free_talk_apply_count', data=data)
	async def on_role_play_roles(self, data): await self.call(type='on_role_play_roles', data=data)
	async def on_role_play_role_update(self, data): await self.call(type='on_role_play_role_update', data=data)
	async def on_role_play_apply_count(self, data): await self.call(type='on_role_play_apply_count', data=data)
	async def on_conversation_level(self, data): await self.call(type='on_conversation_level', data=data)
	async def on_role_play_accept_apply(self, data): await self.call(type='on_role_play_accept_apply', data=data)
	async def on_role_play_user_role_remove(self, data): await self.call(type='on_role_play_user_role_remove', data=data)
	async def on_chat_user_online(self, data): await self.call(type='on_chat_user_online', data=data)
	async def on_chat_delete(self, data): await self.call(type='on_chat_delete', data=data)
	async def on_chat_host_update(self, data): await self.call(type='on_chat_host_update', data=data)
	async def on_chat_disable(self, data): await self.call(type='on_chat_disable', data=data)
	async def on_user_typing(self, data): await self.call(type='on_user_typing', data=data)
	async def on_chat_activity_type(self, data): await self.call(type='on_chat_activity_type', data=data)
	async def on_voice_call_not_answered(self, data): await self.call(type='on_voice_call_not_answered', data=data)
	async def on_all(self, data): await self.call(type='on_all', data=data)