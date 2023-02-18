import projectZ

client = projectZ.Client()
client.login(email='rolaaav11@gmail.com', password='9379992p!')


@client.event("on_text_message")
def on_msg(data):
	msg = data.content
	print(f'new message!\n{msg}\n')