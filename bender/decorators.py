from bender import hooks


def respond_hook(brain, msg, match):
    """
    Called whenever a message send by an user matches the regular expression
    defined as parameter to the decorator.

    :param brain: Brain
    :param msg: ConsoleMessage implementation
    :param match: regex match object
    """


respond = hooks.make_decorator(respond_hook, inputs='regex')


def script_initialize_hook(brain):
    """
    Called in scripts during startup, right after the backbone is setup.

    :param brain: Brain
    """

script_initialize = hooks.make_decorator(script_initialize_hook)