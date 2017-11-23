from itertools import chain
from subprocess import run
import sys


class Types:
    def __getattr__(self, name):
        def func(object_id=None, **kwargs):
            process_args = [f'__{name}']

            if object_id is not None:
                process_args.append(str(object_id))

            for param_name, param_value in kwargs.items():
                param_name = f"--{param_name.replace('_', '-')}"

                if hasattr(param_value, '__iter__') and not isinstance(param_value, str):
                    parameters = chain((param_name, str(value)) for value in param_value)
                else:
                    parameters = param_name, str(param_value)

                process_args.extend(parameters)

            run(process_args)

        return func


sys.modules[__name__] = Types()
