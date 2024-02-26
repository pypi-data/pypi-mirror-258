"""A better way to manage your dotenv variables"""

# Second-party imports
from .parsers import (
    EnvironParser,
    FileParser,
)
from .utils import Path, PathLike


__all__ = [
    "load",
    "load_space",
    "load_file",
]


def load_space(include: list[str], globals_: dict = None) -> dict | None:
    """Load the environment variables from the environment namespace

    Args:
        include (list[str]): The environment variables to include
        globals_ (dict, optional): The globals dictionary to use when loading

    Returns:
        dict: The environment variables
    """

    vars_ = EnvironParser(include).vars

    if globals_ is None:
        return vars_
    else:
        globals_.update(vars_)


def load_file(
    path: Path | PathLike | str, format_: str, globals_: dict = None
) -> dict | None:
    """Args:
        - format_ (str): The format of the file or string. It can be one of the following:

                - 'env': Load the environment variables from a dotenv file
                - 'json': Load the environment variables from a json file
                - 'toml': Load the environment variables from a toml file
                - 'yaml': Load the environment variables from a yaml file

        - path (Path | PathLike | str): The path to the file or the string containing the environment variables
        - globals_ (dict, optional): The globals to use when loading

    Returns:
        dict: The environment variables
    """

    vars_ = FileParser(path, format_).vars

    if globals_ is None:
        return vars_
    else:
        globals_.update(vars_)


def load(
    *path_or_include: Path | PathLike | str | list[str],
    format_: str = "environ",
    globals_: dict = None,
) -> dict | None:
    """Load the environment variables from a file or a string.

    If both path and include are provided, the variables are loaded from the file and the include argument is ignored.

    If path does not exist, the variables are loaded from the environment namespace and the include argument is used to filter the variables.

    Args:
        - path (Path | PathLike | str): The path to the file containing the environment variables
        - include (list[str]): The variables to include when loading from the environment namespace
        - format_ (str): The format of the file or string. If both path and include are provided, the argument defines the format of the file. It can be one of the following:

            - 'environ': Load the environment variables from the environment namespace
            - 'env': Load the environment variables from a dotenv file
            - 'json': Load the environment variables from a json file
            - 'toml': Load the environment variables from a toml file
            - 'yaml': Load the environment variables from a yaml file

        - globals_ (dict, optional): The globals dictionary to use when loading

    Returns:
        dict: The environment variables
    """
    len_args = len(path_or_include)

    # Decide whether to load from the environment namespace or from a file
    from_file = True
    arg = None

    if len_args == 1:
        arg = path_or_include[0]

        if isinstance(arg, (PathLike, str, Path)):
            pass
        elif isinstance(arg, list):
            from_file = False
        else:
            raise ValueError(f'Invalid type "{arg}" for argument "path_or_include"')

    elif len_args == 2:
        arg = path_or_include[0]

        if isinstance(arg, (PathLike, str, Path)):
            if not arg.exists():
                from_file = False
                arg = path_or_include[1]

        elif isinstance(arg, list):
            arg = path_or_include[1]
            if not arg.exists():
                from_file = False
                arg = path_or_include[0]

        else:
            raise ValueError(
                f'Invalid type "{path_or_include}" for one or both arguments in "path_or_include"'
            )

    else:
        raise ValueError(
            "Please provide a path or a list of environment variables to include or both"
        )

    # Load the environment variables
    if from_file:
        return load_file(arg, format_, globals_)
    else:
        return load_space(arg, globals_)
