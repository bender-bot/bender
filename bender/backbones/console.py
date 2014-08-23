import getpass
import threading


#===================================================================================================
# BenderConsole
#===================================================================================================
class BenderConsole(object):


    def __init__(self):
        self.on_message_received = None

    def start(self):
        t = threading.Thread(target=self._raw_input)
        t.start()

    def send_message(self, msg):
        print msg


    def _raw_input(self):
        while True:
            user_input = raw_input('> ')
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
