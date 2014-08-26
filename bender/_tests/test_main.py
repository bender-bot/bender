from io import StringIO
import pytest
import threading

import bender._main
from bender.backbones.console import BenderConsole
from bender.testing import VolatileBrain


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
    assert bender._main.main() == 0
    assert 'Hey, my name is Bender' in stdout.getvalue()
