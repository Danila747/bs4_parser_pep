import argparse
import logging
from logging.handlers import RotatingFileHandler
import sys

from constants import DT_FORMAT, LOG_FORMAT, LOG_DIR


def configure_argument_parser(available_modes):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--clear-cache',
        action='store_true',
        help='Очистить кэш'
    )
    parser.add_argument(
        '--output',
        choices=('pretty'),
        help='Способ вывода'
    )
    return parser


def configure_logging():
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / 'parser.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6, backupCount=5
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler(sys.stdout))
    )
