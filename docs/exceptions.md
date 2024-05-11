<div>
	<h4>
	<a href="main.md">go to main </a>
	</h4>
</div>

<h2 align="center">Using</h2>

```python
from projectZ import exceptions
try: #some code
except exceptions.UnknownError as e:
	print(f"Unknown error: {e}")
```
<div>
	<h4 align="center">
	<a href="https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/projectZ/utils/exceptions.py">Show all exceptions in code</a>
	</h4>
</div>
<hr>

<h3 align="center">All exceptions</h3>

1. **UnknownError**: An exception that occurs when an unknown error or situation that was not anticipated in the program happens.

2. **InvalidLink**: An exception that occurs when attempting to use an invalid link.

3. **IncorrectPassword**: An exception that occurs when an incorrect password is entered.

4. **NotLoggined**: An exception that occurs when attempting to perform an action requiring authentication without logging in first.

5. **AlreadyRegistered**: An exception that occurs when attempting to register a user who is already registered.

6. **BadMedia**: An exception that occurs when processing an invalid media file.

7. **NoWalletError**: An exception that occurs when attempting to perform an operation that requires a wallet when it is not available.

8. **InvalidFile**: An exception that occurs when attempting to process an invalid file.

9. **InvalidEmail**: An exception that occurs when entering an invalid email address.

10. **EmailNotRegistered**: An exception that occurs when attempting to use an unregistered email address.

11. **TooManyRequests**: An exception that occurs when exceeding the limit of requests to the server.

12. **WalletNotActivated**: An exception that occurs when attempting to perform an operation with a wallet that is not activated.

13. **UnsupportedMediaFormat**: An exception that occurs when attempting to use an unsupported media file format.

14. **WrongType**: An exception that occurs when an incorrect type is passed to a function or data.

