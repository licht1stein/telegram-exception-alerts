# Telegram Exception Alerts


## Installation

```bash
pip install telegram_exception_alerts
```
or
```bash
poetry add telegram_exception_alerts
```

## Usage

After you initialize the alerter instance you can attach the decorator to any function. If it 
raises an exception information will be send to the chat specified in `chat_id` (don't forget 
that if you want to send notification to a channel you need to prepend that `chat_id` with `-100`).

```python
from telegram_exception_alerts import Alerter

alerter = Alerter(bot_token='YOUR_BOT_TOKEN', chat_id='YOUR_CHAT_ID')

@alerter.exception_alert
def some_func_that_can_raise_an_exception():
    raise RuntimeError('this is an exception')
```

You can also initialize the alerter from environment variables:

* `ALERT_BOT_TOKEN` - your bot token
* `ALERT_CHAT_ID` - your chat id to receive notifications

```python
from telegram_exception_alerts import Alerter

alerter = Alerter.from_environment()

@alerter.exception_alert
def some_func_that_can_raise_an_exception():
    raise RuntimeError('this is an exception')
```
