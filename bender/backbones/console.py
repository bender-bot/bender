import getpass
import threading


#===================================================================================================
# BenderConsole
#===================================================================================================
class BenderConsole(object):


    def __init__(self):
        self.on_message_received = None
        self._thread = None

    def start(self):
        self._thread = threading.Thread(target=self._raw_input)
        self._thread.start()

    def send_message(self, text):
        print('\n' + text)

    def _raw_input(self):
        while True:
            try:
                user_input = raw_input('> ')
            except EOFError:
                return
            if user_input:
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
        self._backbone.send_message(message)


    def get_sender(self):
        return getpass.getuser()
