import pkg_resources
from bender import scripts
from bender.brain import Brain
from bender import hooks
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
        self._regex_to_response = OrderedDict()
        self._scripts = OrderedDict()

        self._pool = ThreadPoolExecutor(max_workers=4)
        self._futures = []  # list of futures submitted to the pool

    
    def register_script(self, name, script):
        self._scripts[name] = script


    def register_builtin_scripts(self):
        for name, script in scripts.get_builtin_scripts().iteritems():
            self.register_script(name, script)


    def register_setuptools_scripts(self):
        for p in pkg_resources.iter_entry_points('bender_script'):
            class_ = p.load()
            self.register_script(p.name, class_())


    def get_script(self, name):
        return self._scripts[name]


    def start(self):
        self._brain.load()
        self._backbone.on_message_received = self.on_message_received
        hooks.call_unique_hook(self._backbone, 'backbone_start_hook')

        self.register_builtin_scripts()
        self.register_setuptools_scripts()

        for script in self._scripts.itervalues():
            hooks.call_unique_hook(script, 'script_initialize_hook',
                                   brain=self._brain)

    def on_message_received(self, msg):
        
        def thread_exec(hook, brain, msg, match):
            try:
                hooks.call(hook, brain=self._brain, msg=msg, match=match)
            except Exception as e:
                self._backbone.send_message('*BZZT* %s' %e)
            else:
                with self._brain_lock:
                    brain.dump()
        

        handled = False
        for script in self._scripts.itervalues():
            for hook in hooks.find_hooks(script, 'respond_hook'):
                match = re.match(hook.inputs['regex'], msg.get_body(),
                                 re.IGNORECASE | re.DOTALL)
                if match:
                    f = self._pool.submit(thread_exec, hook, self._brain, msg,
                                          match)
                    self._futures.append(f)
                    handled = True

        if not handled:
            msg.reply('Command not recognized')


    def wait_all_messages(self):
        while self._futures:
            f = self._futures.pop()
            f.result()  # wait until future returns



