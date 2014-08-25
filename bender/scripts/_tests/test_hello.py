import pytest
from bender.scripts.hello import HelloScript


@pytest.mark.parametrize('greeting', ['hey', 'hello', 'hi'])
def test_hello(bender_tester, greeting):
    assert isinstance(bender_tester.get_script('hello'), HelloScript)
    assert bender_tester.get_script('hello').initialized
    m = bender_tester.user_send(greeting, sender='Fry')
    bender_tester.assert_reply(m, 'Hi Fry, you bastard.')
    bender_tester.assert_replies(m, ['Hi Fry, you bastard.'])


def test_help(bender_tester):
    m = bender_tester.user_send('help')
    expected = [
        'Here are the commands I understand:',
        '',
        "Send greetings to Bender (regex: 'hey|hello|hi')",
        "Beg for help (regex: 'help')",
        "Shutdown Bender handling. Careful! (regex: 'shutdown|quit|exit')",
        '',
    ]
    bender_tester.assert_reply(m, '\n'.join(expected))
