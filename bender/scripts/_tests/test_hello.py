import pytest
from bender.scripts.hello import HelloScript


@pytest.mark.parametrize('greeting', ['hey', 'hello', 'hi'])
def test_hello(bender_tester, greeting):
    assert isinstance(bender_tester.get_script('hello'), HelloScript)
    assert bender_tester.get_script('hello').initialized
    m = bender_tester.user_send(greeting, sender='Fry')
    bender_tester.assert_reply(m, 'Hi Fry, you bastard.')
    bender_tester.assert_replies(m, ['Hi Fry, you bastard.'])
