import pytest


def test_decorator(notifier, monkeypatch):
    @notifier
    def some_func_that_can_raise_an_exception():
        raise RuntimeError("this is an exception")

    monkeypatch.setattr(
        notifier, "send_message", lambda *args, **kwargs: (args, kwargs)
    )

    with pytest.raises(RuntimeError):
        some_func_that_can_raise_an_exception()
