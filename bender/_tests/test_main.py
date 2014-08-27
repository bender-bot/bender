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
    """
    Test that we can select backbones from the command line.
    """
    quitter = install_quitter_backbone(mock)
    mock.patch.object(bender._main, 'get_brain', return_value=VolatileBrain())
    assert bender._main.main(['', '--backbone', 'quitter']) == 0
    assert quitter.started


def install_quitter_backbone(mock):
    """
    installs a "quitter" backbone: a backbone that immediately quits right
    after starting.

    It is installed as a distutils entry point by  mocking the relevant methods,
    as close to distutils as possible to ensure all our code is tested.

    This can be moved into a fixture, or even make QuitterBackbone
    available in bender.testing.
    """
    class QuitterBackbone(object):

        def __init__(self):
            self.on_message_received = None
            self.started = False

        @backbone_start
        def start(self):
            self.on_message_received(DumbMessage('quit', 'user'))
            self.started = True

    quitter = QuitterBackbone()
    factory = lambda: quitter

    class EntryPoint(object):
        pass

    quitter_entry_point = EntryPoint()
    quitter_entry_point.name = 'quitter'
    quitter_entry_point.load = lambda: factory

    original_entry_points = pkg_resources.iter_entry_points

    def iter_entry_points(name):
        if name == 'bender_backbone':
            return [quitter_entry_point]
        else:
            return original_entry_points(name)

    mock.patch.object(pkg_resources, 'iter_entry_points', iter_entry_points)
    return quitter
