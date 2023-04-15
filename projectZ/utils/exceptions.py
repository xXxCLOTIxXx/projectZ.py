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

class NotLoggined(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class AlreadyRegistered(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class BadMedia(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)

class NoWalletError(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class InvalidFile(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class InvalidEmail(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class EmailNotRegistered(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class TooManyRequests(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


class WalletNotActivated(Exception):
	def __init__(*args, **kwargs):
		Exception.__init__(*args, **kwargs)


errors = {
	2009: EmailNotRegistered,
	2022: InvalidEmail,
	4604: InvalidLink,
	2010: IncorrectPassword,
	2038: AlreadyRegistered,
	6107: TooManyRequests,
	7008: BadMedia,
	1000004: NoWalletError,
	1000108: WalletNotActivated
}

def CheckException(data):
	try:
		data = loads(data)
		code = data["apiCode"]
	except:
		raise UnknownError(data)
	if code in errors: raise errors[code](data)
	else:raise UnknownError(data)