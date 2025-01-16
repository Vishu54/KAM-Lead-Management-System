import logging

logger = logging.getLogger(__name__)


class AppRuntimeException(Exception):
    def __init__(self, error_code: int = 500, message: str = "Unexpected Error Occurred"):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)


def handle_exception(error_code: int = 500, message: str = "Unexpected Error Occurred", should_log_exception: bool = True):
    logger.error(message, exc_info=should_log_exception)
    raise AppRuntimeException(error_code, message)
