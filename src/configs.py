import argparse
import logging
import os

from logging.handlers import RotatingFileHandler

from constants import (
    BASE_DIR,
    DT_FORMAT,
    LOG_FORMAT
)


def configure_argument_parser(available_modes):
    """
    Создает аргумент-парсер.
    """
    parser = argparse.ArgumentParser(description='Парсер документации Python')
    parser.add_argument(
        'mode',
        choices=available_modes,
        help='Режимы работы парсера'
    )
    parser.add_argument(
        "-c",
        "--clear-cache",
        action="store_true",
        help="Очистка кеша"
    )
    parser.add_argument(
        "-o",
        "--output",
        choices=("pretty", "file"),
        help="Дополнительные способы вывода данных"
    )
    return parser


def setup_logging(log_level=logging.INFO,
                  log_format='%(asctime)s %(levelname)s %(name)s %(message)s',
                  log_filename='parser.log'):
    """
    Настраивает логирование.
    """
    log_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)


def configure_logging():
    log_dir = BASE_DIR / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "parser.log"
    max_log_size = 10 * 1024 * 1024
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=max_log_size, backupCount=5
    )

    console_handler = logging.StreamHandler()
    handlers = [rotating_handler, console_handler]

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DT_FORMAT,
        handlers=handlers
    )
