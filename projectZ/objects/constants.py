from enum import Enum

api_url="https://api.projz.com"
web_api_url="https://www.projz.com"
ws_url = "wss://ws.projz.com"
ws_endpoint = "/v1/chat/ws"
ws_ping_interval: int = 3

prefix = bytes.fromhex("04")
SIG_KEY = bytes.fromhex("ce070279278de1b6390b76942c13a0b0aa0fda6aedd6f2d655eda7cf6543b35f" + ("6a" * 32))
DEVICE_KEY = bytes.fromhex("997ec928a85f539e3fa124761e7572ef852e")


def get_signable_header_keys() -> list[str]: return [
    "rawDeviceId", "rawDeviceIdTwo", "rawDeviceIdThree",
    "appType", "appVersion", "osType",
    "deviceType", "sId", "countryCode",
    "reqTime", "User-Agent", "contentRegion",
    "nonce", "carrierCountryCodes"
]


def get_persistent_headers() -> dict:
    return {
        "appType": "MainApp", "appVersion": "2.27.1",
        "osType": "2", "deviceType": "1", "flavor": "google",
        "User-Agent": "com.projz.z.android/2.27.1-25104 (Linux; U; Android 7.1.2; ASUS_Z01QD; Build/Asus-user 7.1.2 2017)"
}


class LoggerLevel():
    INFO = 1
    WARNING = 2
    ERROR = 3
    DEBUG = 4
    OFF = 5


log_level_string = {
    1:"INFO",
    2:"WARNING",
    3:"ERROR",
    4:"DEBUG"
}

class SocketEventTypes(Enum):
    MESSAGE = 1
    ACK = 2
    PUSH = 13