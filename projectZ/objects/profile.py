from ..utils.generator import gen_deviceId 

class profile:
    deviceId: str
    sid: str = ''
    uid: str = None
    language: str
    country_code: str
    time_zone: int

    def __init__(self, deviceId: str = None, language: str = "en-US", country_code="en", time_zone = 180):
        self.deviceId=deviceId if deviceId else gen_deviceId()
        self.language=language
        self.country_code=country_code
        self.time_zone=time_zone