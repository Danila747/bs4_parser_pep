import logging

from requests import Session, RequestException
from typing import Optional
from bs4 import BeautifulSoup as Bs

from constants import EXPECTED_STATUS
from exceptions import NoTagFound


def get_response(session: Session, url: str):
    try:
        response = session.get(url)
        response.encoding = "utf-8"
        response.raise_for_status()
        return response
    except RequestException as e:
        logging.exception(f"Failed to load page {url}: {e}")
        return None


def find_tag(soup: Bs, tag: Optional[str] = None,
             attrs: Optional[dict] = None,
             text: Optional[str] = None) -> Optional[Bs]:
    try:
        if text:
            searched_tag = soup.find(text=text)
        else:
            searched_tag = soup.find(tag, attrs=(attrs or {}))
        if searched_tag is None:
            raise Exception
    except Exception:
        if text:
            error_msg = f"Tag with text '{text}' not found"
        else:
            error_msg = f"Tag '{tag}' with attributes '{attrs}' not found"
        logging.error(error_msg, exc_info=True)
        raise NoTagFound(error_msg)
    else:
        return searched_tag


def check_key(key: str) -> bool:
    if key in EXPECTED_STATUS:
        return True
    else:
        raise KeyError("Status key not found in the dictionary")
