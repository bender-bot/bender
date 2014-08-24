import functools
import inspect


def _get_only_args_spec(f):
    spec = inspect.getargspec(f)
    assert spec.varargs is None, 'func %s cannot contain *args' % f
    assert spec.keywords is None, 'func %s cannot contain ***kwargs' % f
    assert spec.defaults is None, 'func %s cannot contain defaults' % f
    return spec


def make_decorator(hook_decl, inputs=()):
    hook_spec = _get_only_args_spec(hook_decl)
    inputs = inputs if type(inputs) in (tuple, list) else [inputs]

    def make_decorated(f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            return f(*args, **kwargs)
        decorated.hook_name = hook_decl.__name__
        decorated.spec = spec = _get_only_args_spec(f)

        diff_specs = set(spec.args).difference(hook_spec.args)
        diff_specs.discard('self')
        if diff_specs:
            msg = 'function <{name}>: argument names {args} are not valid for '\
                  'hook "{hook}"'
            raise HookError(msg.format(name=f.__name__, args=list(diff_specs),
                                       hook=hook_decl.__name__))
        return decorated

    if inputs:
        def decorator(*args):
            def inner(f):
                wrapped = make_decorated(f)
                wrapped.inputs = {k: args[i] for (i, k) in enumerate(inputs)}
                return wrapped
            return inner
    else:
        def decorator(f):
            inner = make_decorated(f)
            inner.inputs = {}
            return inner

    return decorator


def call(hook, **kwargs):
    if not hasattr(hook, 'hook_name'):
        raise HookError('%s is not a hook' % hook)
    if hook.spec.args:
        accepts_kwargs = set(hook.spec.args).intersection(kwargs)
        new_kwargs = {k: kwargs[k] for k in accepts_kwargs}
    else:
        new_kwargs = {}
    return hook(**new_kwargs)


def find_hooks(obj, hook_name):
    result = []
    for name in dir(obj):
        value = getattr(obj, name)
        if getattr(value, 'hook_name', None) == hook_name:
            result.append(value)
    return result


def call_all_hooks(obj, hook_name, **kwargs):
    for hook in find_hooks(obj, hook_name):
        call(hook, **kwargs)
    return None


def call_unique_hook(obj, hook_name, **kwargs):
    found = find_hooks(obj, hook_name)
    if len(found) > 1:
        raise HookError(
            '%s can implement %s at most one time' % (obj, hook_name))
    elif len(found) == 1:
        return call(found[0], **kwargs)


class HookError(RuntimeError):
    pass
