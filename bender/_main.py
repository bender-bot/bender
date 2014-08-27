import argparse
import sys
import pkg_resources

from bender.backbones.console import BenderConsole

from ._bender import Bender


def get_console():
    return BenderConsole()


def get_brain():
    return None


def get_setuptools_backbones():
    return {p.name: p.load() for p in
            pkg_resources.iter_entry_points('bender_backbone')}


def parse_args(argv, available_backbones, default_backbone):
    parser = argparse.ArgumentParser(description='Bender chat bot')
    parser.add_argument('--backbone', default=default_backbone,
                        choices=[default_backbone] + sorted(
                            available_backbones),
                        help='name of the backbone to use')
    args = parser.parse_args(argv[1:])
    return args


def main(argv=None):
    if argv is None:
        # later we will probably use this to configure which backbone to use
        argv = sys.argv

    available_backbones = get_setuptools_backbones()
    console_name = 'console'

    args = parse_args(argv, available_backbones, console_name)

    if args.backbone == console_name:
        backbone = get_console()
    else:
        backbone_class = available_backbones[args.backbone]
        backbone = backbone_class()  # instantiate class

    bot = Bender(backbone)
    bot.loop()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
