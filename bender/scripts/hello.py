from bender.decorators import respond


class HelloScript(object):

    def initialize(self, brain):
        pass

    @respond(r'hey|hello|hi')
    def hello(self, brain, msg, match):
        msg.reply('Hi, %s, you bastard.' % msg.get_sender())
