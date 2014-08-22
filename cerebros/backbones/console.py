from cerebros.backbones.base import BaseCerebrosBackbone, BaseCerebrosMessage
import click
import getpass
import threading


#===================================================================================================
# ConsolecerebrosBackbone
#===================================================================================================
class ConsolecerebrosBackbone(BaseCerebrosBackbone):

    def start(self):
        t = threading.Thread(target=self._raw_input)
        t.start()


    def send_message(self, msg):
        click.echo(msg)


    def _raw_input(self):
        while True:
            msg = ConsolecerebrosMessage(self, click.prompt('>', prompt_suffix=' '))
            self.on_message_received(msg)


#===================================================================================================
# ConsolecerebrosMessage
#===================================================================================================
class ConsolecerebrosMessage(BaseCerebrosMessage):
    
    def __init__(self, backbone, msg):
        self._msg = msg
        self._backbone = backbone


    def get_body(self):
        return self._msg


    def reply(self, message):
        self._backbone.send_message(message)


    def get_sender(self):
        return getpass.getuser()
