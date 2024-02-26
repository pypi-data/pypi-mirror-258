"""Errors for secret_garden"""

# Second-party imports
from .utils import ALLOWED_FORMATS, get_extension, Path, PathLike


__all__ = [
    "EnvironVarUndeclaredError",
    "FormatReaderMissingError",
    "FormatUndeclaredError",
    "InvalidFormatError",
    "UnexpectedFormatError",
]


class TypedEnvError(Exception):
    """Base error class for secret_garden"""

    def __init__(
        self,
        message: str = "",
        check_condition: bool = True,
        raised_from=None,
    ):
        self.check_condition = check_condition
        self.message = message
        self.raised_from = raised_from

    def check(self):
        """Check the condition and raise the error if it is met"""

        if self.check_condition:
            return False
        else:
            super().__init__(f"{self.message}")

            if self.raised_from is not None:
                raise self from self.raised_from
            else:
                raise self


class ReaderError(TypedEnvError):
    """Error experienced during the reading process"""


class EnvironVarUndeclaredError(ReaderError):
    """Environment variable undeclared error"""

    def __init__(self, var_name: str, var_val: str | None):

        message = f'Environment variable "{var_name}" not found'
        check_condition = var_val is not None

        super().__init__(message, check_condition)


class ParserError(TypedEnvError):
    """Error experienced during the parsing process"""


class FormatReaderMissingError(ParserError):
    """Format loader missing error"""

    def __init__(self, format_: str, key_error: KeyError = KeyError()):

        message = f'Format reader missing for "{format_}"'
        check_condition = False

        super().__init__(message, check_condition, raised_from=key_error)


class FormatUndeclaredError(ParserError):
    """Format undeclared error"""

    def __init__(self, format_: str | None):

        message = "Format undeclared, please declare a format"
        check_condition = format_ is not None

        super().__init__(message, check_condition)


class InvalidFormatError(ParserError):
    """Invalid file format error"""

    def __init__(self, format_: str):

        message = (
            f'Invalid file format: "{format_}"; Only {ALLOWED_FORMATS} are allowed'
        )
        check_condition = format_ in ALLOWED_FORMATS

        super().__init__(message, check_condition)


class UnexpectedFormatError(ParserError):
    """Invalid file format error"""

    def __init__(self, path: Path | PathLike | str, expected_format: str):

        self.path = Path(path)
        self.expected_format = expected_format
        self.path_extension = get_extension(self.path.name)

        message = (
            f'Unexpected file format for "{self.path}" in "{self.expected_format}"'
        )
        check_condition = self.path_extension == self.expected_format

        super().__init__(message, check_condition)


class LoaderError(TypedEnvError):
    """Error experienced during the loading process"""
