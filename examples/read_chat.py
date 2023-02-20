import projectZ

client = projectZ.Client()
client.login(email='email', password='password')


@client.event("on_text_message")
def on_msg(data):
	msg = data.content
	print(f'new message!\n{msg}\n')
