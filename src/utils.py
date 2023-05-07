import logging
from typing import Optional

from bs4 import BeautifulSoup as Bs
from requests import RequestException, Session

from constants import EXPECTED_STATUS
from exceptions import ParserFindTagException


def get_response(session: Session, url: str):
    try:
        response = session.get(url)
        response.encoding = "utf-8"
        response.raise_for_status()
        return response
    except RequestException as e:
        logging.exception(f"Failed to load page {url}: {e}")
        return None


def find_tag(soup, tag, attrs=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag
