from bender import hooks


def respond_hook(bender, brain, msg, match):
    """
    Called in scripts whenever a message send by an user matches the regular
    expression defined as parameter to the decorator.

    :param bender: Bender
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


def backbone_start_hook(brain):
    """
    Called in the backbone when it should start receiving messages.
    :param brain: Brain
    """

backbone_start = hooks.make_decorator(backbone_start_hook)


def script_shutdown_hook(brain):
    """called for each script before bender quits; called before
    `backbone_shutdown_hook`
    :param brain: Brain
    """

script_shutdown = hooks.make_decorator(script_shutdown_hook)


def backbone_shutdown_hook(brain):
    """called in the backbone before bender quits; called after all scripts
    are shutdown themselves.
    :param brain: Brain
    """

backbone_shutdown = hooks.make_decorator(backbone_shutdown_hook)

