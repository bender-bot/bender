import getpass
import threading

from bender.decorators import backbone_start, backbone_shutdown


#===================================================================================================
# BenderConsole
#===================================================================================================
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
                msg = ConsoleMessage(self, user_input)
                self.on_message_received(msg)


#===================================================================================================
# ConsoleMessage
#===================================================================================================
class ConsoleMessage(object):
    
    def __init__(self, backbone, msg):
        self._msg = msg
        self._backbone = backbone

    def get_body(self):
        return self._msg

    def reply(self, message):
        self._backbone._send_message(message)

    def get_sender(self):
        return getpass.getuser()
