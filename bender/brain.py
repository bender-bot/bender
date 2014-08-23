import os
import yaml


#===================================================================================================
# Brain
#===================================================================================================
class Brain(dict):

    def _get_brain_filename(self):
        return os.path.expanduser('~/.bender.yaml')


    def dump(self):
        with file(self._get_brain_filename(), 'w') as stream:
            yaml.dump(self.items(), stream)


    def load(self):
        filename = self._get_brain_filename()
        if not os.path.isfile(filename):
            return

        with file(filename, 'r') as stream:
            self.update(yaml.load(stream))
