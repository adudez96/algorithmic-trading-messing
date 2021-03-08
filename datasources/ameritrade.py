from typing import List
from config import config
from datasources import Datasource
from util import YEAR_IN_MILLIS, unix_time_millis

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd

from google.cloud import storage

from datetime import datetime
import logging
import requests
import string
import time


class AmeritradeDatasource(Datasource):
    def get_symbols() -> List[str]:
        symbols = []

        # Get a current list of all the stock symbols for the NYSE
        alpha = list(string.ascii_uppercase)
        for each in alpha:
            url = 'http://eoddata.com/stocklist/NYSE/{}.htm'.format(each)
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

    # Price History API Documentation
    # https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory
    @classmethod
    def getHistoricalData(cls) -> pd.DataFrame:

        # Get the historical dates you need.
        # Only doing one day here as an example
        date = datetime.strptime('2019-11-19', '%Y-%m-%d')

        # Convert to unix for the API
        date_ms = unix_time_millis(date)

        logging.info("Getting symbols...")
        symbols = cls.get_symbols()
        # symbols = ["AAPL"]  # for testing
        logging.debug(symbols)

        # Get the price history for each stock. This can take a while
        logging.info("Getting TDAmeritrade key...")
        consumer_key = get_ameritrade_key()

        data_list = []

        logging.info("Getting historical data...")
        for each in symbols:
            url = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(each)

            # You can do whatever period/frequency you want
            # This will grab the data for a single day
            params = {
                'apikey': consumer_key,
                'periodType': 'month',
                'frequencyType': 'daily',
                'frequency': '1',
                'startDate': date_ms - (2 * YEAR_IN_MILLIS),
                'endDate': date_ms,
                'needExtendedHoursData': 'true'
            }

            request = requests.get(
                url=url,
                params=params
                )

            data_list.append(request.json())
            time.sleep(.25)

        # Create a list for each data point and loop through the json, adding the data to the lists
        symbl_l, open_l, high_l, low_l, close_l, volume_l, date_l = [], [], [], [], [], [], []

        for data in data_list:
            try:
                symbl_name = data['symbol']
            except KeyError:
                symbl_name = np.nan
            try:
                for each in data['candles']:
                    symbl_l.append(symbl_name)
                    open_l.append(each['open'])
                    high_l.append(each['high'])
                    low_l.append(each['low'])
                    close_l.append(each['close'])
                    volume_l.append(each['volume'])
                    date_l.append(each['datetime'])
            except KeyError:
                pass

        # Create a df from the lists
        df = pd.DataFrame(
            {
                'symbol': symbl_l,
                'open': open_l,
                'high': high_l,
                'low': low_l,
                'close': close_l, 
                'volume': volume_l,
                'date': date_l
            }
        )

        # Format the dates
        df['date'] = pd.to_datetime(df['date'], unit='ms')
        df['date'] = df['date'].dt.strftime('%Y-%m-%d')

        print(df.head())

        return df


def get_ameritrade_key() -> str:
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(config["storage"]["tdameritrade-api-creds"]["bucket"])
    api_key = bucket.get_blob(config["storage"]["tdameritrade-api-creds"]["blob"]).download_as_string()

    return api_key
