from bender.backbones.console import BenderConsole
from bender.brain import Brain
from collections import OrderedDict
from concurrent.futures.thread import ThreadPoolExecutor
import re
import threading


#===================================================================================================
# Bender
#===================================================================================================
class Bender(object):

    def __init__(self, backbone):
        self._backbone = backbone
        self._brain = Brain()
        self._brain_lock = threading.Lock()
        self._pool = ThreadPoolExecutor(max_workers=4)
        self._regex_to_response = OrderedDict()
        self._scripts = []

    
    def register_script(self, inst):
        for attr in dir(inst):
            value = getattr(inst, attr)
            if getattr(value, 'response', False):
                regex = value.regex
                self._regex_to_response[regex] = value

        self._scripts.append(inst)


    def start(self):
        self._brain.load()
        self._backbone.on_message_received = self.on_message_received
        self._backbone.start()

        for script in self._scripts:
            script.initialize(self._brain)


    def on_message_received(self, msg):
        
        def foo(func, brain, msg, match):
            try:
                func(self._brain, msg, match)
            except Exception as e:
                self._backbone.send_message('*BZZT* %s' %e)
            else:
                with self._brain_lock:
                    brain.dump()
        

        handled = False
        for regex, func in self._regex_to_response.iteritems():
            match = re.match(regex, msg.get_body(), re.IGNORECASE | re.DOTALL)
            if match:
                self._pool.submit(foo, func, self._brain, msg, match)
                handled = True

        if not handled:
            msg.reply('Command not recognized')



