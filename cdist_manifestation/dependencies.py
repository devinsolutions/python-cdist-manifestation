from contextlib import contextmanager

_dependencies = []
_order_dependency = False


@contextmanager
def order_dependency():
    global _order_dependency

    if not _order_dependency:
        _order_dependency = True

        yield

        _order_dependency = False
    else:
        yield


@contextmanager
def require(*args):
    global _dependencies

    _dependencies.extend(args)

    yield

    del _dependencies[-len(args):]
