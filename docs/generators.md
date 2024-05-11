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

endpoint="/auth/login/ect"
headers = {
	"countryCode": "us"
}

data = dumps({
	"name": "exmpl",
	"pswd": "1111111"
})

sig = gen_signature(path=endpoint, headers=headers, body=data)
print(sig)
```
