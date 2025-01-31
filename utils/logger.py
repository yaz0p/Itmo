import sys

from aiologger import Logger
from aiologger.formatters.base import Formatter
from aiologger.handlers.files import AsyncFileHandler
from aiologger.handlers.streams import AsyncStreamHandler
from aiologger.levels import LogLevel
import functools
import time


async def setup_logger():
    # Create logger instance
    logger = Logger(name="api_logger")

    # Create formatter
    formatter = Formatter(
        fmt="{asctime} | {levelname} | {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    file_handler = AsyncFileHandler(
        filename="logs/api.log",
        mode="a",
        encoding="utf-8",
    )
    stream_handler = AsyncStreamHandler(stream=sys.stdout)
    file_handler.formatter = formatter
    stream_handler.formatter = formatter
    logger.add_handler(file_handler)
    logger.add_handler(stream_handler)

    logger.level = LogLevel.INFO

    return logger


async def retryer(count_of_retryes = 3, delay = 1):
    async def retry_decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            for i in range(count_of_retryes):
                try:
                    result = await func(*args, **kwargs)
                except Exception as e:
                    if i < count_of_retryes - 1:
                        time.sleep(delay)
                    else:
                        raise e
            return result
        return wrapper
    
