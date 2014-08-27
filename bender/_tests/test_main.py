from io import StringIO
import pkg_resources
import pytest
import threading

import bender._main
from bender.backbones.console import BenderConsole
from bender.decorators import backbone_start
from bender.testing import VolatileBrain, DumbMessage


@pytest.mark.timeout(3.0)
def test_main(mock):
    stdout = StringIO()
    stdin = StringIO()
    stdin.write(u'hey\nquit\n')
    stdin.seek(0)

    timer = threading.Timer(1.0, stdin.close)
    timer.start()
    console = BenderConsole(stdout=stdout, stdin=stdin)
    mock.patch.object(bender._main, 'get_console', return_value=console)
    mock.patch.object(bender._main, 'get_brain', return_value=VolatileBrain())
    assert bender._main.main([]) == 0
    assert 'Hey, my name is Bender' in stdout.getvalue()


@pytest.mark.timeout(3.0)
def test_backbone_selection(mock):
    class EntryPoint(object):
        pass

    backbone = QuitterBackbone()
    get = lambda: backbone

    p = EntryPoint()
    p.name = 'quitter'
    p.load = lambda: get

    original_entry_points = pkg_resources.iter_entry_points
    def iter_entry_points(name):
        if name == 'bender_backbone':
            return [p]
        else:
            return original_entry_points(name)

    mock.patch.object(pkg_resources, 'iter_entry_points', iter_entry_points)
    mock.patch.object(bender._main, 'get_brain', return_value=VolatileBrain())
    assert bender._main.main(['', '--backbone', 'quitter']) == 0
    assert backbone.started


class QuitterBackbone(object):

    def __init__(self):
        self.on_message_received = None
        self.started = False

    @backbone_start
    def start(self):
        self.on_message_received(DumbMessage('quit', 'user'))
        self.started = True
