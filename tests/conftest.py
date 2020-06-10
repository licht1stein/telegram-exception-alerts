from telegram_exception_alerts import Alerter

import pytest


@pytest.fixture
def notifier():
    return Alerter(
        bot_token="YOUR_TOKEN", chat_id=1111111
    )
