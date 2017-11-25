from contextlib import contextmanager

_dependencies = []
_order_dependency = False


@contextmanager
def order_dependency():
    """
    A context manager that emulates functionality of "CDIST_ORDER_DEPENDENCY"
    environmental variable.
    """
    global _order_dependency

    if not _order_dependency:
        _order_dependency = True

        yield

        _order_dependency = False
    else:
        yield


@contextmanager
def require(*args):
    """
    A context manager that emulates functionality of "require" environment
    variable.

    Args:
        args: Dependecy strings to feed "require" environmental variable with
    """
    global _dependencies

    _dependencies.extend(args)

    yield

    del _dependencies[-len(args):]
