import logging
import os
import sys

from ..config.config import settings


def get_logger(file, display=False):

    """Создание и настройка логгера."""

    logging.root.setLevel(logging.NOTSET)
    log_path = os.path.join(os.path.dirname(file), settings.LOG_REL_PATH)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_file = os.path.join(log_path, os.path.basename(file) + settings.LOG_EXTENSION)
    logger = logging.getLogger(os.path.basename(file))
    formatter = logging.Formatter(settings.LOG_FORMAT)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(settings.LOG_DEFAULT_LVL)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if display:
        console_handler = logging.StreamHandler(stream=sys.stdout)
        console_handler.setLevel(settings.LOG_DEFAULT_LVL)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger
