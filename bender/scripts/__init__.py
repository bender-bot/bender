from . import hello


def get_builtin_scripts():
    return [
        ("hello", hello.HelloScript()),
    ]