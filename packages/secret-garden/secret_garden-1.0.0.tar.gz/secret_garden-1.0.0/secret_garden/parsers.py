"""Read and load the environment variable strings"""

# Built-in imports
from ast import literal_eval
from os import environ
from typing import Callable

# Second-party imports
from .errors import (
    FormatReaderMissingError,
    FormatUndeclaredError,
    InvalidFormatError,
    UnexpectedFormatError,
)
from .readers import (
    env_reader,
    environ_reader,
    json_reader,
    toml_reader,
    yaml_reader,
)
from .utils import (
    Path,
    PathLike,
)


__all__ = [
    "EnvironParser",
    "FileParser",
]


class Parser:
    """Read and load the environment variable strings"""

    def __init__(
        self, format_: str, format_input: Path | PathLike | str | list[str]
    ) -> None:

        # Check if format is declared and is valid
        FormatUndeclaredError(format_).check()
        InvalidFormatError(format_).check()

        # Get environment variables to exclude
        self.exclude = literal_eval(environ.get("EXCLUDE", "[]"))

        self.format = format_

        self.vars = {
            var: val
            for var, val in self.__get_loader(format_input).items()
            if var not in self.exclude
        }

    @property
    def __get_loader(self) -> Callable:
        """Get the loader function for a given format from the global namespace"""

        try:
            loader = globals()[f"{self.format}_reader"]
        except KeyError as key_error:
            FormatReaderMissingError(self.format, key_error).check()

        return loader


class EnvironParser(Parser):
    """Read and load the environment variable strings from os environment namespace"""

    def __init__(self, include: list[str]) -> None:
        super().__init__("environ", include)


class FileParser(Parser):
    """Read and load the environment variable strings from a file"""

    def __init__(self, path: Path | PathLike | str, format_) -> None:

        self.path = Path(path)
        self.format = format_

        # Ensure file extension and declared format match
        UnexpectedFormatError(self.path, self.format).check()
        super().__init__(format_, path)
