import argparse
import logging
import re
from urllib.parse import urljoin

import requests
import requests_cache
from bs4 import BeautifulSoup as Bs
from tqdm import tqdm

from constants import BASE_DIR, EXPECTED_STATUS, MAIN_DOC_URL, PATTERN, PEP
from outputs import control_output
from utils import check_key, find_tag, get_response

def main(session):
    response = get_response(session, MAIN_PEP_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'section', {'id': 'numerical-index'})
    peps_row = main_tag.find_all('tr')
    count_status_in_card = defaultdict(int)
    result = [('Статус', 'Количество')]
    for i in range(1, len(peps_row)):
        pep_href_tag = peps_row[i].a['href']
        pep_link = urljoin(MAIN_PEP_URL, pep_href_tag)
        response = get_response(session, pep_link)
        soup = BeautifulSoup(response.text, 'lxml')
        main_card_tag = find_tag(soup, 'section', {'id': 'pep-content'})
        main_card_dl_tag = find_tag(main_card_tag, 'dl',
                                    {'class': 'rfc2822 field-list simple'})
        for tag in main_card_dl_tag:
            if tag.name == 'dt' and tag.text == 'Status:':
                card_status = tag.next_sibling.next_sibling.string
                count_status_in_card[card_status] = count_status_in_card.get(
                    card_status, 0) + 1
                if len(peps_row[i].td.text) != 1:
                    table_status = peps_row[i].td.text[1:]
                    if card_status[0] != table_status:
                        logging.info(
                            '\n'
                            'Несовпадающие статусы:\n'
                            f'{pep_link}\n'
                            f'Статус в карточке: {card_status}\n'
                            f'Ожидаемые статусы: '
                            f'{EXPECTED_STATUS[table_status]}\n'
                                )
    for key in count_status_in_card:
        result.append((key, str(count_status_in_card[key])))
    result.append(('Total', len(peps_row)-1))
    return result

if __name__ == "__main__":
    main()
