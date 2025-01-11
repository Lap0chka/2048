import logging
from logging.handlers import RotatingFileHandler


class Logger:
    """
    A utility class for setting up and managing logging with rotating files.
    """

    def __init__(
        self,
        name: str,
        log_file: str,
        level: int = logging.DEBUG,
        max_bytes: int = 10000,
        backup_count: int = 3,
    ):
        """
        Initialize the Logger instance.

        Args:
            name (str): The name of the logger.
            log_file (str): The file where logs will be written.
            level (int): The logging level (default is logging.DEBUG).
            max_bytes (int): The maximum file size in bytes before rotation (default is 10,000).
            backup_count (int): The number of backup files to keep (default is 3).
        """
        self.logger: logging.Logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create a rotating file handler
        file_handler = RotatingFileHandler(log_file, maxBytes=max_bytes, backupCount=backup_count)
        file_handler.setLevel(level)

        # Create a formatter and set it for the handler
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(lineno)d - %(levelname)s: %(message)s"
        )
        file_handler.setFormatter(formatter)

        # Add the handler to the logger
        self.logger.addHandler(file_handler)

    def get_logger(self) -> logging.Logger:
        """
        Get the logger instance.

        Returns:
            logging.Logger: The configured logger.
        """
        return self.logger
