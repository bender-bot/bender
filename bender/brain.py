import os
import yaml


#===================================================================================================
# Brain
#===================================================================================================
class Brain(dict):

    def _get_brain_filename(self):
        return os.path.expanduser('~/.bender.yaml')


    def dump(self):
        with open(self._get_brain_filename(), 'w') as stream:
            yaml.dump(self.items(), stream)


    def load(self):
        filename = self._get_brain_filename()
        if not os.path.isfile(filename):
            return

        with open(filename, 'r') as stream:
            self.update(yaml.safe_load(stream))
