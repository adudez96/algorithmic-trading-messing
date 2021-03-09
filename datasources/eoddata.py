from typing import List

from bs4 import BeautifulSoup

import requests
import string

class EODDataDatasource(object):
    @staticmethod
    def get_stock_symbol_list(exchange: str = "NYSE") -> List[str]:
        symbols = []

        # Get a current list of all the stock symbols for the NYSE
        alpha = list(string.ascii_uppercase)
        for each in alpha:
            url = 'http://eoddata.com/stocklist/{}/{}.htm'.format(exchange, each)
            resp = requests.get(url)
            site = resp.content
            soup = BeautifulSoup(site, 'html.parser')
            table = soup.find('table', {'class': 'quotes'})
            for row in table.findAll('tr')[1:]:
                symbols.append(row.findAll('td')[0].text.rstrip())
                
        # Remove the extra letters on the end
        symbols_clean = []

        for each in symbols:
            each = each.replace('.', '-')
            symbols_clean.append((each.split('-')[0]))
        
        return symbols_clean
