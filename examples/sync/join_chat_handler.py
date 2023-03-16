import projectZ

client = projectZ.Client()
client.login(email='email', password='password')


@client.event("on_text_message")
def on_join(data):
	messageType = data.messageType
	chatId = data.threadId
	nickname = data.nickname

	if messageType == 11:
		client.send_message(chatId=chatId, message=f'Bye, {nickname}.')

	elif messageType == 10:
		client.send_message(chatId=chatId, message=f'Hello, {nickname}.')