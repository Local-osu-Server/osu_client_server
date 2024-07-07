import pprint
from enum import Enum
from inspect import currentframe
from typing import Any

from common.log import LogTypes, log, logger, setup_logging


class ServerErrorType(Enum):
    ...


class AdapterAPIError(ServerErrorType):
    LOGIN_FAILED = "LOGIN_FAILED"
    GET_PROFILE_FAILED = "GET_PROFILE_FAILED"
    GET_RANK_FAILED = "GET_RANK_FAILED"


class ApplicationRepoError(ServerErrorType):
    OSU_NOT_FOUND = "OSU_NOT_FOUND"
    CONFIG_API_FAILED = "CONFIG_API_FAILED"


class ServerError:
    def __init__(
        self,
        error_name: ServerErrorType,
        message: str | None = None,
        file_location: str | None = None,
        line: int | None = None,
        in_scope_variables: list[str] | None = None,
        global_variables: dict[str, Any] | None = None,
        local_variables: dict[str, Any] | None = None,
        status_code: int = 500,
        log_now: bool = True,
    ) -> None:
        self.error_name = error_name
        self.message = message
        self.file_location = file_location
        self.line = line

        self.in_scope_variables = in_scope_variables
        self.global_variables = global_variables
        self.local_variables = local_variables

        self.status_code = status_code

        if log_now:
            self.print_error(detailed=True)

    def to_dict(self, json_able: bool = True) -> dict[str, Any]:
        if json_able:
            return {
                "error_name": self.error_name.value,
                "message": self.message,
                "file_location": self.file_location,
                "line": self.line,
                "in_scope_variables": pprint.pformat(self.in_scope_variables),
                "global_variables": pprint.pformat(self.global_variables),
                "local_variables": pprint.pformat(self.local_variables),
                "status_code": self.status_code,
            }
        else:
            return {
                "error_name": self.error_name,
                "message": self.message,
                "file_location": self.file_location,
                "line": self.line,
                "in_scope_variables": pprint.pformat(self.in_scope_variables),
                "global_variables": pprint.pformat(self.global_variables),
                "local_variables": pprint.pformat(self.local_variables),
                "status_code": self.status_code,
            }

    @staticmethod
    def get_current_line() -> int:
        cf = currentframe()
        return cf.f_back.f_lineno  # type: ignore

    @property
    def error_message(self) -> str:
        return f"{self.error_name} was raised at {self.file_location}:{self.line} with message: {self.message}"

    @property
    def detailed_error_message(self) -> str:
        return (
            f"{self.error_name} was raised at {self.file_location}:{self.line} with message: {self.message}\n\n"
            f"in_scope_variables: {self.in_scope_variables}\n\n"
            f"global_variables: {self.global_variables}\n\n"
            f"local_variables: {self.local_variables}"
        )

    def print_error(self, detailed: bool = False) -> None:
        global logger
        if logger is None:
            logger = setup_logging()

        if detailed:
            log(self.detailed_error_message, LogTypes.ERROR)
            logger.error(self.detailed_error_message)
        else:
            log(self.detailed_error_message, LogTypes.ERROR)
            logger.error(self.error_message)
