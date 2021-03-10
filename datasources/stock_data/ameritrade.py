from typing import List

from config import config
from datasources.stock_data import StockDataSource
from util import ROUND_DECIMAL_PLACES_DEFAULT, YEAR_IN_MILLIS, current_unix_time_millis

import numpy as np
import pandas as pd
from tqdm import tqdm

from google.cloud import storage

import logging
import requests
import time


class AmeritradeDatasource(StockDataSource):
    # Price History API Documentation
    # https://developer.tdameritrade.com/price-history/apis/get/marketdata/%7Bsymbol%7D/pricehistory
    def getHistoricalData(self, symbols: List[str]) -> pd.DataFrame:

        # Convert to unix for the API
        date_ms = current_unix_time_millis()

        # Get the price history for each stock. This can take a while
        logging.info("Getting TDAmeritrade key...")
        consumer_key = get_ameritrade_key()

        data_list = []

        logging.info("Getting historical data...")
        for stock_sym in tqdm(symbols, disable=not config["logging"]["print-progress-bars"]):
            url = r"https://api.tdameritrade.com/v1/marketdata/{}/pricehistory".format(stock_sym)

            # You can do whatever period/frequency you want
            # This will grab the data for a single day
            params = {
                'apikey': consumer_key,
                'periodType': 'month',
                'frequencyType': 'daily',
                'frequency': '1',
                'startDate': date_ms - (3 * YEAR_IN_MILLIS),
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

        logging.info("Processing historical data...")
        for data in tqdm(data_list, disable=not config["logging"]["print-progress-bars"]):
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

        return df


def get_ameritrade_key() -> str:
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(config["storage"]["tdameritrade-api-creds"]["bucket"])
    api_key = bucket.get_blob(config["storage"]["tdameritrade-api-creds"]["blob"]).download_as_string()

    return api_key
