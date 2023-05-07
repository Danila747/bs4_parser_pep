import argparse
import logging
import re
from collections import defaultdict
from urllib.parse import urljoin

import requests
import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm

from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PATTERN, PEP, MAIN_PEP_URL
from utils import check_key, find_tag, get_response

def main():
    session = requests.Session()
    response = get_response(session, MAIN_PEP_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = soup.find('section', {'id': 'numerical-index'})
    peps_row = main_tag.find_all('tr')
    count_status_in_card = defaultdict(int)
    result = [('Статус', 'Количество')]

    for i, row in enumerate(tqdm(peps_row[1:], desc="Scrapping PEPs Status")):
        pep_href_tag = row.a['href']
        pep_link = urljoin(MAIN_PEP_URL, pep_href_tag)
        response = get_response(session, pep_link)
        soup = BeautifulSoup(response.text, 'lxml')
        main_card_tag = soup.find('section', {'id': 'pep-content'})
        main_card_dl_tag = main_card_tag.find('dl', {'class': 'field-list'})
        
        for tag in main_card_dl_tag:
            if tag.name == 'dt' and tag.text == 'Status:':
                card_status = tag.next_sibling.next_sibling.string
                count_status_in_card[card_status] += 1

                if len(row.td.text) > 1 and card_status[0] != row.td.text[1:]:
                    logging.info(
                        '\n'
                        'Несовпадающие статусы:\n'
                        f'{pep_link}\n'
                        f'Статус в карточке: {card_status}\n'
                        f'Ожидаемые статусы: '
                        f'{EXPECTED_STATUS[row.td.text[1:]]}\n'
                            )

    for key in count_status_in_card:
        result.append((key, count_status_in_card[key]))

    result.append(('Total', len(peps_row)-1))
    return result

if __name__ == "__main__":
    main()
