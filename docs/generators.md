<div>
	<h4>
	<a href="main.md">go to main </a>
	</h4>
</div>

<h3 align="center">Gen deviceId</h3>

```python
from projectZ import Client, gen_deviceId
deviceId=gen_deviceId()
print(deviceId
client = Client(deviceId=deviceId)
```

<h3 align="center">Gen sirnature</h3>

```python
from projectZ import gen_signature
from json import dumps
from io import BytesIO


content = BytesIO()

endpoint="/auth/login/ect"
headers = {
	"countryCode": "us"
}

content.write(dumps({
	"name": "exmpl",
	"pswd": "1111111"
}).encode("utf-8"))

sig = gen_signature(path=endpoint, headers=headers, body=content.getvalue())
print(sig)
```
