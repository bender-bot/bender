from io import StringIO
import threading
import pytest
import bender._main
from bender.backbones.console import BenderConsole


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
    assert bender._main.main() == 0
    assert 'Hey, my name is Bender' in stdout.getvalue()