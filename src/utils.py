import logging

from requests import RequestException, Session

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
