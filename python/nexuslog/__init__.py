"""Fast async logger with Rust backend."""

from ._logger import (
    PyLevel as Level,
    PyLogger as _PyLogger,
    get_logger as _get_logger,
    basic_config as _basic_config,
)

__all__ = [
    "Level",
    "Logger",
    "basicConfig",
    "getLogger",
]

_DEFAULT_LEVEL = Level.Info


def basicConfig(log_file: str | None = None, level: Level = Level.Info) -> None:
    """Configure the default log file and level for getLogger()."""
    global _DEFAULT_LEVEL
    _basic_config(log_file)
    _DEFAULT_LEVEL = level


class Logger:
    """Fast async logger instance.

    Args:
        name: Logger name, shown in log output as [time name LEVEL]
        path: Optional file path prefix for log files. If None, logs to stdout.
              Log files are rotated daily with format: {path}_YYYYMMDD.log
        level: Minimum log level to record. Default is Level.Info.
    """

    def __init__(
        self, name: str, path: str | None = None, level: Level = Level.Info
    ) -> None:
        self._logger = _PyLogger(name, path, level)

    def shutdown(self) -> None:
        """Shutdown the logger and flush remaining messages."""
        self._logger.shutdown()

    def trace(self, message: str) -> None:
        """Log a trace message."""
        self._logger.trace(message)

    def debug(self, message: str) -> None:
        """Log a debug message."""
        self._logger.debug(message)

    def info(self, message: str) -> None:
        """Log an info message."""
        self._logger.info(message)

    def warning(self, message: str) -> None:
        """Log a warning message."""
        self._logger.warn(message)

    def error(self, message: str) -> None:
        """Log an error message."""
        self._logger.error(message)


def getLogger(name: str, level: Level | None = None) -> Logger:
    """Get a logger that shares a writer with the default path."""
    if level is None:
        level = _DEFAULT_LEVEL
    logger = Logger.__new__(Logger)
    logger._logger = _get_logger(name, level)
    return logger
