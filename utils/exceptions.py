from json import loads

class WrongType(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class UnknownError(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class InvalidLink(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class IncorrectPassword(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

def CheckException(data):
	try:
		data = loads(data)
		code = data["apiCode"]
	except:
		raise UnknownError(data)

	if code == 4604: raise InvalidLink(data)
	elif code == 2010: raise IncorrectPassword(data)
	else:raise UnknownError(data)