from contextlib import contextmanager

_dependencies = []


@contextmanager
def require(*args):
    global _dependencies

    orig_deps = list(_dependencies)
    _dependencies.extend(args)

    yield

    _dependencies = orig_deps
