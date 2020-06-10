from telegram_exception_alerts import TelegramNotifier

import pytest


@pytest.fixture
def notifier():
    return TelegramNotifier(
        bot_token="419870734:AAEijbQFv0irstDqVcf01W7zz2RjenE4o8s", chat_id=22039771
    )
