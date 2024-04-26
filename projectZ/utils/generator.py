from hashlib import sha1, sha256 
from hmac import HMAC
from base64 import b64encode
from typing import Optional
from uuid import uuid4

from ..objects.constants import (
	prefix, SIG_KEY, DEVICE_KEY,
	get_signable_header_keys
)



def gen_signature(path: str, headers: dict, body: bytes) -> str:
	mac = HMAC(key=SIG_KEY, msg=path.encode("utf-8"), digestmod=sha256)
	for header in [headers[signable] for signable in get_signable_header_keys() if signable in headers]:
		mac.update(header.encode("utf-8"))
	if body:mac.update(body)
	return b64encode(prefix + mac.digest()).decode("utf-8")




def gen_deviceId(installation_id: str = None):
	if not installation_id:installation_id=str(uuid4())
	_prefix = prefix + sha1(installation_id.encode("utf-8")).digest()
	return ( _prefix + sha1( _prefix + sha1(DEVICE_KEY).digest() ).digest() ).hex()