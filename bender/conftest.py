import pytest
from bender._bender import Bender
from bender.scripts.hello import HelloScript


@pytest.yield_fixture
def bender_tester():
    tester = BenderTester()
    yield tester
    tester.shutdown()


class DumbBackbone(object):

    def __init__(self):
        self.on_message_received = None
        self.sent_messages = []

    def start(self):
        pass

    def send_message(self, msg):
        self.sent_messages.append(msg)


class DumbMessage(object):

    def __init__(self, body, sender):
        self._body = body
        self._sender = sender
        self.replies = []

    def reply(self, text):
        self.replies.append(text)

    def get_body(self):
        return self._body

    def get_sender(self):
        return self._sender


class BenderTester(object):

    def __init__(self):
        self._backbone = DumbBackbone()
        self._bender = Bender(self._backbone)
        self._bender.register_builtin_scripts()
        self._bender.start()

    def get_script(self, name):
        return self._bender.get_script(name)

    def shutdown(self):
        pass

    def user_send(self, text, sender='user'):
        m = DumbMessage(text, sender)
        self._backbone.on_message_received(m)
        self._bender.wait_all_messages()
        return m

    def assert_reply(self, msg, expected_reply):
        __tracebackhide__ = True
        assert len(msg.replies) == 1, 'expected a single reply, but obtained %d' % len(msg.replies)
        assert msg.replies[0] == expected_reply

    def assert_replies(self, msg, expected_replies):
        __tracebackhide__ = True
        assert msg.replies == expected_replies

