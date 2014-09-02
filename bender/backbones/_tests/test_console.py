from io import StringIO
import pickle
import sys

from bender.backbones.console import ConsoleMessage


def test_console_message_pickle():
    '''
    Check if :class:`.ConsoleMessage` is pickable.
    '''
    stream_output = StringIO()
    message = ConsoleMessage('foo', stream_output)
    loaded_message = pickle.loads(pickle.dumps(message))

    assert message.get_body() == loaded_message.get_body()
    assert isinstance(message._stream_output, StringIO)
    assert loaded_message._stream_output is sys.stdout
