import importlib
import json
import os


class Brain(dict):

    def _get_brain_filename(self):
        return os.path.expanduser('~/.bender.cfg')

    def dump(self):
        with open(self._get_brain_filename(), 'w') as stream:
            json.dump(self, stream, indent=2, default=_to_json, sort_keys=True)

    def load(self):
        filename = self._get_brain_filename()
        if not os.path.isfile(filename):
            return

        with open(filename, 'r') as stream:
            self.update(json.load(stream, object_hook=_from_json))


def _to_json(o):
    # Using the same strategy used by pickle.
    if hasattr(o, '__reduce__'):
        result = o.__reduce__()
        class_ = result[0]
        args = result[1]
        return {
            '__class__': class_.__name__,
            '__module__': class_.__module__,
            'args': args,
        }
    return o


def _from_json(o):
    if '__module__' in o and '__class__' in o:
        module = importlib.import_module(o['__module__'])
        class_ = getattr(module, o['__class__'])
        return class_(*o['args'])
    return o
