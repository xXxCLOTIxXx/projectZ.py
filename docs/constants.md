<div>
	<h4>
	<a href="main.md">go to main </a>
	</h4>
</div>


# MediaTargets
Used to download media files

```python
class MediaTargets:
    USER_ICON = 1
    BACKGROUND = 2
    FOREGROUND = 3
    BLOG_AUDIO = 5
    MESSAGE = 8
    MESSAGE_AUDIO = 10
    USER_NAME_CARD_BACKGROUND = 11
```

### usage

```python
import projectZ
c = projectZ.Client()
c.upload_media(file=file, target=projectZ.MediaTargets.BACKGROUND)
```

---

# ChatMessageTypes
Used to send different types of chat messages

```python

class ChatMessageTypes:
    TEXT = 1
    MEDIA = 2
    VIDEO = 4
    AUDIO = 6
    STICKER = 7
    DICE = 44
    POLL = 45
    TYPING = 60
    GIFTBOX = 128
```


### usage

```python
import projectZ
c = projectZ.Client()
c.send_message(chatId="12343", message="hi", message_type=projectZ.ChatMessageTypes.TEXT)
```

---

# WsMethods
Used to indicate the event type

[event types](https://github.com/xXxCLOTIxXx/projectZ.py/blob/main/projectZ/objects/ws_types.py)




### usage

```python
import projectZ
c = projectZ.Client()
@c.event(projectZ.WsMethods.on_text_message)
def message(data):
    print(data.json)
```
