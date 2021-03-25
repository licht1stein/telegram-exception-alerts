from __future__ import annotations

import os
import traceback
from functools import wraps

from urllib import request, parse


class Alerter:
    """
    Alerter class for sending telegram messages and decorating functions for alerts.
    """
    def __init__(self, bot_token, chat_id):
        self.bot_token = bot_token
        self.chat_id = chat_id

    @property
    def base_url(self):
        return f"https://api.telegram.org/bot{self.bot_token}"

    @classmethod
    def from_environment(cls) -> Alerter:
        try:
            token: str = os.environ["ALERT_BOT_TOKEN"]
        except KeyError:
            raise KeyError(
                "ALERT_BOT_TOKEN must be set in environment variables")

        try:
            chat_id = os.environ["ALERT_CHAT_ID"]
        except KeyError:
            raise KeyError(
                "ALERT_CHAT_ID must be set in environment variables")

        return cls(bot_token=token, chat_id=int(chat_id))

    def custom_alert(
        self,
        text: str,
        *,
        parse_mode: str = None,
        disable_web_page_preview: bool = True,
        disable_notification: bool = False,
    ):
        """
        Sends a telegram message to default chat_id. All params according to https://core.telegram.org/bots/api#sendmessage

        :param text: message text
        :param parse_mode: None, 'MARKDOWN' or 'HTML'
        :param disable_web_page_preview: no link preview
        :param disable_notification: send silently
        :return: requests.Response
        """
        return self.send_message(
            chat_id=self.chat_id,
            text=text,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
        )

    def send_message(
        self,
        chat_id: int,
        *,
        text: str,
        parse_mode: str = None,
        disable_web_page_preview: bool = True,
        disable_notification: bool = False,
    ):
        """
        Sends a telegram message to `chat_id`. All params according to https://core.telegram.org/bots/api#sendmessage

        :param chat_id: telegram chat id to send to
        :param text: message text
        :param parse_mode: None, 'MARKDOWN' or 'HTML'
        :param disable_web_page_preview: no link preview
        :param disable_notification: send silently
        :return: requests.Response
        """
        url = self.base_url + "/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": parse_mode,
            "disable_web_page_preview": disable_web_page_preview,
            "disable_notification": disable_notification,
        }
        params_data = parse.urlencode(params).encode()
        req = request.Request(url, method="POST", data=params_data)
        return request.urlopen(req)

    def exception_alert(self, func):
        """
        Telegram exception alert decorator. Sends exception details and traceback to self.chat_id and re-raises the exception
        """
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except BaseException as e:
                text = f"<b>{type(e).__name__}('{e}')</b> in <u>{func.__name__}</u> from <u>{func.__module__}</u>\n\n<pre>{traceback.format_exc()}</pre>"

                self.send_message(self.chat_id, text=text, parse_mode="HTML")
                raise

        return inner

    def __call__(self, func):
        return self.exception_alert(func)
