from websocket import WebSocketApp, enableTrace
from websocket import _exceptions as WSexceptions
from .utils import exceptions
from threading import Thread
from time import sleep
from json import dumps, loads
from .utils import objects
from traceback import format_exc

class Socket:
	def __init__(self, headers, debug: bool = False, sock_trace: bool = False):
		self.socket_url = "wss://ws.projz.com"
		self.socket = None
		self.debug=debug

		self.headers = headers
		self.active = False
		self.online_loop_active = False
		self.socket_thread = None
		self.reconnectTime = 90
		self.reconnect_thread = None
		self.buffer = list()
		enableTrace(sock_trace)


	def resolve(self, ws, data):
		data = loads(data)
		try:
			messageId = data['msg']['messageId']
			if messageId in self.buffer:
				return
			self.buffer.append(messageId)
			#I know, it looks like shit, but I haven't come up with another way yet (when the socket is rebooted, all messages that have already come come again)
		except:
			pass
		self.on_all(data)
		self.methods.get(data['msg']['type'])(data)

	def connect(self):
		try:
			if self.debug:
				print(f"[socket][start] Starting Socket")

			self.socket = WebSocketApp(
				f"{self.socket_url}/v1/chat/ws",
				header = self.headers(endpoint='/v1/chat/ws'),
				on_message=self.resolve
			)
			self.socket_thread = Thread(target=self.socket.run_forever)
			self.socket_thread.start()
			self.active = True
			if self.reconnect_thread is None:
				self.reconnect_thread = Thread(target=self.reconnect)
				self.reconnect_thread.start()
			if self.debug:
				print(f"[socket][start] Socket Started")
		except Exception as e:
			if self.debug:
				print(f"[socket][start] Error while starting Socket : {e}")

	def disconnect(self):
		if self.debug:
			print(f"[socket][close] Closing Socket")
		try:
			self.socket.close()
			self.active = False
			self.socket_thread = None
			if self.debug:
				print(f"[socket][close] Socket closed")
		except Exception as e:
			if self.debug:
				print(f"[socket][close] Error while closing Socket : {e}")
		return

	def reconnect(self):
		while True:
			sleep(self.reconnectTime)
			if self.active:
				if self.debug is True:
					print(f"[socket][reconnect_handler] Reconnecting Socket")
				self.disconnect()
				self.connect()

	def online_loop(self):
		sleep(1.5)
		while self.online_loop_active:
			try:
				self.send()
			except Exception as e:
				if self.debug:
					print('[socket][_online_loop][error] ', e)
			sleep(3)



	def send(self, t: int = 8, data = None, threadId: int = None):
		
		if not self.socket_thread:
			raise exceptions.NotLoggined('You are not logged in')
		d = {'t': t}
		if threadId:d['threadId'] = threadId
		if data:d['msg'] = data
		if self.debug is True:
			print(f"[socket][send] Sending Data : {d}")
		
		try:return self.socket.send(dumps(d))
		except WSexceptions.WebSocketConnectionClosedException:
			if self.debug is True:
				print(f"[socket][send][error] Socket not available")


class CallBacks:
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

	def call(self, type, data):
		if type in self.handlers:
			for handler in self.handlers[type]:
				try:handler(objects.Event(data))
				except:
					if self.debug:
						print("[event][call][error]Error calling your function:\n", format_exc(),'\n')

	def on_text_message(self, data): self.call(type='on_text_message', data=data)
	def on_image_message(self, data): self.call(type='on_image_message', data=data)
	def on_audio_message(self, data): self.call(type='on_audio_message', data=data)
	def on_video_message(self, data): self.call(type='on_video_message', data=data)
	def on_delete_message(self, data): self.call(type='on_delete_message', data=data)
	def on_user_join(self, data): self.call(type='on_user_join', data=data)
	def on_user_leave(self, data): self.call(type='on_user_leave', data=data)
	def on_user_invite(self, data): self.call(type='on_user_invite', data=data)
	def on_user_kick(self, data): self.call(type='on_user_kick', data=data)
	def on_user_remove(self, data): self.call(type='on_user_remove', data=data)
	def on_cohost_remove(self, data): self.call(type='on_cohost_remove', data=data)
	def on_cohost_add(self, data): self.call(type='on_cohost_add', data=data)
	def on_host_delete_message(self, data): self.call(type='on_host_delete_message', data=data)
	def on_cohost_delete_message(self, data): self.call(type='on_cohost_delete_message', data=data)
	def on_role_play_invite(self, data): self.call(type='on_role_play_invite', data=data)
	def on_free_talk_start(self, data): self.call(type='on_free_talk_start', data=data)
	def on_free_talk_end(self, data): self.call(type='on_free_talk_end', data=data)
	def on_role_play_start(self, data): self.call(type='on_role_play_start', data=data)
	def on_role_play_end(self, data): self.call(type='on_role_play_end', data=data)
	def on_voice_call_start(self, data): self.call(type='on_voice_call_start', data=data)
	def on_voice_call_end(self, data): self.call(type='on_voice_call_end', data=data)
	def on_voice_call_reject(self, data): self.call(type='on_voice_call_reject', data=data)
	def on_voice_call_cancel(self, data): self.call(type='on_voice_call_cancel', data=data)
	def on_voice_call_accept(self, data): self.call(type='on_voice_call_accept', data=data)
	def on_free_talk_add_user(self, data): self.call(type='on_free_talk_add_user', data=data)
	def on_free_talk_remove_user(self, data): self.call(type='on_free_talk_remove_user', data=data)
	def on_free_talk_invite(self, data): self.call(type='on_free_talk_invite', data=data)
	def on_free_talk_apply(self, data): self.call(type='on_free_talk_apply', data=data)
	def on_free_talk_accept(self, data): self.call(type='on_free_talk_accept', data=data)
	def on_live_talking_users(self, data): self.call(type='on_live_talking_users', data=data)
	def on_free_talk_apply_count(self, data): self.call(type='on_free_talk_apply_count', data=data)
	def on_role_play_roles(self, data): self.call(type='on_role_play_roles', data=data)
	def on_role_play_role_update(self, data): self.call(type='on_role_play_role_update', data=data)
	def on_role_play_apply_count(self, data): self.call(type='on_role_play_apply_count', data=data)
	def on_conversation_level(self, data): self.call(type='on_conversation_level', data=data)
	def on_role_play_accept_apply(self, data): self.call(type='on_role_play_accept_apply', data=data)
	def on_role_play_user_role_remove(self, data): self.call(type='on_role_play_user_role_remove', data=data)
	def on_chat_user_online(self, data): self.call(type='on_chat_user_online', data=data)
	def on_chat_delete(self, data): self.call(type='on_chat_delete', data=data)
	def on_chat_host_update(self, data): self.call(type='on_chat_host_update', data=data)
	def on_chat_disable(self, data): self.call(type='on_chat_disable', data=data)
	def on_user_typing(self, data): self.call(type='on_user_typing', data=data)
	def on_chat_activity_type(self, data): self.call(type='on_chat_activity_type', data=data)
	def on_voice_call_not_answered(self, data): self.call(type='on_voice_call_not_answered', data=data)
	def on_all(self, data): self.call(type='on_all', data=data)