#===================================================================================================
# IBackbone
#===================================================================================================
class IBackbone(object):

    def __init__(self):
        self.on_message_received = None
    
    
    def start(self):
        raise NotImplementedError()


    def send_message(self, msg):
        raise NotImplementedError()


#===================================================================================================
# IMessage
#===================================================================================================
class IMessage(object):

    def reply(self, text):
        raise NotImplementedError()


    def get_body(self):
        raise NotImplementedError()


    def get_sender(self):
        raise NotImplementedError()
