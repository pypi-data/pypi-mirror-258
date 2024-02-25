import logging
from logging.handlers import TimedRotatingFileHandler

""" Simple logger for logging info to a file"""

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler = TimedRotatingFileHandler(
    "info.log", when="D", interval=1, backupCount=100, encoding="utf-8", delay=False
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def log_info(func):
    def wrapper(*args, **kwargs):
        logger.info(f"{func.__name__} Run with {args} and {kwargs}")
        return func(*args, **kwargs)

    return wrapper
