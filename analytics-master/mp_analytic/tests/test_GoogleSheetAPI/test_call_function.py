from FakeService import GSA
from FakeService import HttpError_exception


def some_function():
    return 'answer'


def test_call_function(GSA):
    assert GSA.call_function(some_function) == 'answer'
    assert GSA.call_function(HttpError_exception) is False
