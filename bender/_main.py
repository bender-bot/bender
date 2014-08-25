import sys

from ._bender import Bender
from bender.backbones.console import BenderConsole


def get_console():
    return BenderConsole()


def main(argv=None):
    if argv is None:
        # later we will probably use this to configure which backbone to use
        argv = sys.argv
    bot = Bender(get_console())
    bot.loop()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))