from itertools import chain
import os
from subprocess import Popen
import sys

from cdist_manifestation.dependencies import _dependencies


class Types:
    def __getattr__(self, name):
        def func(object_id=None, *args, **kwargs):
            type_name = f'__{name}'
            process_args = [type_name]

            if object_id is not None:
                process_args.append(str(object_id))

            for argument in args:
                process_args.append(f'--{argument}')

            for param_name, param_value in kwargs.items():
                param_name = f"--{param_name.replace('_', '-')}"

                if hasattr(param_value, '__iter__') and not isinstance(param_value, str):
                    parameters = chain((param_name, str(value)) for value in param_value)
                else:
                    parameters = param_name, str(param_value)

                process_args.extend(parameters)

            Popen(process_args, env=dict(os.environ, require=' '.join(_dependencies))).wait()

            if object_id is None:
                return type_name

            return f"{type_name}/{str(object_id).lstrip('/')}"

        return func


sys.modules[__name__] = Types()
