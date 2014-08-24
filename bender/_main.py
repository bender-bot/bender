import sys

from bender._bender import Bender
from bender.backbones.console import BenderConsole

def main(argv=None):
    if argv is None:
        argv = sys.argv
    backbone = BenderConsole()
    bot = Bender(backbone)
    backbone.send_message('Hey, my name is Bender. Can I help ya?')
    bot.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print('Bye')

if __name__ == '__main__':
    sys.exit(main(sys.argv))