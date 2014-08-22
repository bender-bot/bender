#===================================================================================================
# BaseCerebrosBackbone
#===================================================================================================
class BaseCerebrosBackbone(object):

    def __init__(self):
        self.on_message_received = None
    
    
    def start(self):
        raise NotImplementedError()


    def send_message(self, msg):
        raise NotImplementedError()


#===================================================================================================
# BaseCerebrosMessage
#===================================================================================================
class BaseCerebrosMessage(object):

    def reply(self, message):
        raise NotImplementedError()


    def get_body(self):
        raise NotImplementedError()


    def get_sender(self):
        raise NotImplementedError()
