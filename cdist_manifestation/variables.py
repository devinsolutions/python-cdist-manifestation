import os
import sys


class _Variables:
    def __getattr__(self, name):
        value = os.getenv(f'__{name}')

        if value is None:
            raise AttributeError(name)

        return value


sys.modules[__name__] = _Variables()
