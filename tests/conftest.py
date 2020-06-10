from telegram_exception_alerts import Alerter

import pytest


@pytest.fixture
def notifier():
    return Alerter(
        bot_token="foo", chat_id=11111
    )
