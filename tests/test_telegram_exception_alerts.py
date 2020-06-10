import pytest


def test_decorator(notifier, monkeypatch):
    @notifier
    def func():
        raise RuntimeError("test_exception")

    # monkeypatch.setattr(
    #     notifier, "send_message", lambda *args, **kwargs: (args, kwargs)
    # )

    with pytest.raises(RuntimeError):
        func()
