from bender.backbones.console import ConsoleMessage
from bender.brain import Brain
from io import StringIO
import pickle
import sys
from mock import patch



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

@patch.object(Brain, '_get_brain_filename')
def test_console_message_brain(mock_Brain, tmpdir):
    mock_Brain.return_value = unicode(tmpdir.join('brain.cfg'))

    # Creating a new brain and dumping its contents.
    brain_1 = Brain()
    brain_1['main'] = {
        'alpha': 'Alpha',
        'bravo': ['Bravo'],
        'charlie': {
            'messages': {
                'key 1': [
                    ConsoleMessage('first message'),
                    ConsoleMessage('second message'),
                ],
            }
        }
    }
    brain_1.dump()

    # Creating a new brain and loading contents from existing file.
    brain_2 = Brain()
    brain_2.load()

    # Both objects must have the same contents.
    assert brain_1.items() == brain_2.items()
