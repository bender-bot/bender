import getpass
import sys
import threading

from bender.decorators import backbone_start, backbone_shutdown


class BenderConsole(object):

    def __init__(self, stdout=sys.stdout, stdin=sys.stdin):
        self._stdout = stdout
        self._stdin = stdin
        self.on_message_received = None
        self._thread = None

    @backbone_start
    def start(self):
        self._send_message(u'Hey, my name is Bender. Can I help ya?')
        self._thread = threading.Thread(target=self._raw_input)
        self._thread.start()

    @backbone_shutdown
    def shutdown(self):
        self._stdout.write(u'Hit keyboard interrupt to get out\n')
        try:
            self._thread.join()
        except KeyboardInterrupt:
            pass

    def _send_message(self, text):
        self._stdout.write(u'\n' + text + u'\n')

    def _raw_input(self):
        while True:
            try:
                self._stdout.write(u'\n> ')
                user_input = self._stdin.readline()
            except (EOFError, ValueError):
                return
            if user_input:
                self._stdout.flush()
                msg = ConsoleMessage(user_input, self._stdout)
                self.on_message_received(msg)


class ConsoleMessage(object):

    def __init__(self, msg, stream_output=sys.stdout):
        self._msg = msg
        self._stream_output = stream_output

    def get_body(self):
        return self._msg

    def reply(self, message):
        self._stream_output.write(u'\n' + message + u'\n')

    def get_sender(self):
        return getpass.getuser()

    def __reduce__(self):
        return (self.__class__, (self._msg,))
