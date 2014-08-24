from bender.decorators import respond, script_initialize


class HelloScript(object):

    def __init__(self):
        self.initialized = False

    @script_initialize
    def init(self):
        self.initialized = True

    @respond(r'hey|hello|hi')
    def hello(self, msg):
        msg.reply('Hi %s, you bastard.' % msg.get_sender())
