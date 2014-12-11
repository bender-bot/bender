from bender.decorators import respond, script_initialize
import bender_hooks as hooks


class HelloScript(object):

    def __init__(self):
        self.initialized = False

    @script_initialize
    def init(self):
        self.initialized = True

    @respond(r'hey|hello|hi')
    def hello(self, msg):
        """
        Send greetings to Bender

        > hey
        Hi <user>, you bastard.
        """
        msg.reply('Hi %s, you bastard.' % msg.get_sender())

    @respond(r'shutdown|quit|exit')
    def shutdown(self, msg, bender):
        """
        Shutdown Bender handling. Careful!

        > shutdown
        I'm outta here!
        """
        msg.reply("I'm outta here!")
        bender.request_shutdown()

    @respond(r'help')
    def help(self, msg, bender):
        """
        Beg for help
        """
        lines = [
            'Here are the commands I understand:',
            '',
        ]
        for name, script in bender.iter_scripts():
            for hook in hooks.find_hooks(script, 'respond_hook'):
                docstring = hook.__doc__
                if not docstring:
                    docstring = '<no docstring :(>'
                doc_lines = [x.strip() for x in docstring.splitlines()
                             if x.strip()]
                text = '{regex}: {summary}'
                lines.append(
                    text.format(summary=doc_lines[0],
                                regex=repr(hook.inputs['regex'])))
            lines.append('')

        msg.reply('\n'.join(lines))
