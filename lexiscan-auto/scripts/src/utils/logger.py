import logging
import sys
from pathlib import Path
from pythonjsonlogger import jsonlogger


def setup_logging(
        level: str = "INFO",
        log_file: str = None,
        json_format: bool = False
):
    """
    Configure application logging.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional file path for logs
        json_format: Use JSON format (better for production)
    """

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level.upper()))

    # Remove existing handlers
    logger.handlers = []

    # Console handler (prints to terminal)
    console_handler = logging.StreamHandler(sys.stdout)

    if json_format:
        # JSON format for production (easy to parse)
        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
    else:
        # Human-readable format for development
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        Path(log_file).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.info(f"Logging initialized at {level} level")
    return logger

#TEST
from src.utils.logger import setup_logging

logger = setup_logging(level="INFO")
logger.info("This is an info message")
logger.warning("This is a warning")
logger.error("This is an error")