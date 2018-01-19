from itertools import chain
import os
import shutil
from subprocess import Popen
import sys


class _Types:
    """
    This is a helper class that enables us to use __getattr__ for dynamic type
    importing.
    """

    class InstantiationError(Exception):
        """
        This error is raised when a type exits with non-zero return code.
        """
        pass

    def __getattr__(self, name):  # noqa: C901
        type_name = f'__{name}'

        if shutil.which(type_name) is None:
            raise AttributeError(name)

        def type_func(object_id=None, **kwargs):
            """
            This function generates a cdist type command that will be called
            upon the function execution.

            Args:
                object_id: An object ID (optional)
                kwargs: Additional type parameters. Hyphens in parameter name
                    must be replaced with underscores.

            Returns:
                The object dependecy string.
            """
            process_args = [type_name]

            if object_id is not None:
                process_args.append(str(object_id))

            for param_name, param_value in kwargs.items():
                param_name = f"--{param_name.replace('_', '-')}"

                if isinstance(param_value, bool):
                    if param_value:
                        parameters = [param_name]
                    else:
                        continue
                elif hasattr(param_value, '__iter__') and not isinstance(param_value, str):
                    parameters = chain.from_iterable(
                        (param_name, str(value)) for value in param_value
                    )
                else:
                    parameters = param_name, str(param_value)

                process_args.extend(parameters)

            environment = dict(os.environ)

            from cdist_manifestation.dependencies import _dependencies, _order_dependency

            if len(_dependencies) > 0:
                environment['require'] = ' '.join(_dependencies)

            if _order_dependency:
                environment['CDIST_ORDER_DEPENDENCY'] = 'on'

            process = Popen(process_args, env=environment)
            process.wait()

            if process.returncode != 0:
                raise self.InstantiationError(f"Failed to instantiate type '{name}'")

            if object_id is None:
                return type_name

            return f"{type_name}/{str(object_id).lstrip('/')}"

        return type_func


sys.modules[__name__] = _Types()
