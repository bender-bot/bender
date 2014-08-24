import sys

from bender._bender import Bender
from bender.backbones.console import BenderConsole

def main(argv=None):
    if argv is None:
        argv = sys.argv
    backbone = BenderConsole()
    bot = Bender(backbone)
    bot.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print 'Bye'

if __name__ == '__main__':
    sys.exit(main(sys.argv))