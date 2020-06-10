from __future__ import annotations

import os
import traceback
from functools import wraps

import attr
import requests


@attr.s
class Alerter:
    bot_token: str = attr.ib(repr=False)
    chat_id: int = attr.ib()
    base_url: str = attr.ib(init=False, repr=False)

    def __attrs_post_init__(self):
        self.base_url = f'https://api.telegram.org/bot{self.bot_token}'

    @classmethod
    def from_environment(cls) -> Alerter:
        try:
            token: str = os.environ['ALERT_BOT_TOKEN']
        except KeyError:
            raise KeyError('ALERT_BOT_TOKEN must be set in environment variables')

        try:
            chat_id = os.environ['ALERT_CHAT_ID']
        except KeyError:
            raise KeyError('ALERT_CHAT_ID must be set in environment variables')

        return cls(bot_token=token, chat_id=int(chat_id))

    def send_message(self, chat_id: int, *, text: str, parse_mode: str = None):
        return requests.post(self.base_url + '/sendMessage',
                          params={'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode})

    def exception_alert(self, func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                self.send_message(self.chat_id,
                                  text=f'{type(e).__name__}({e}) in {func.__name__}\n\n{traceback.format_exc()}')
                raise

        return inner
