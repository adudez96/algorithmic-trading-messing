from config import config
from datasources.ameritrade import AmeritradeDatasource, get_ameritrade_key
from logger import setup_logging

from google.cloud import bigquery, storage

import logging
import os


historical_data_csv_filename = "{}/historical.csv".format(os.getcwd())

def main() -> None:
    setup_logging()
    logging.info("Running!")
    # run_bigquery_client_test()
    # run_storage_client_test()
    logging.info("Getting historical data...")
    df_historical_data = AmeritradeDatasource.getHistoricalData()
    logging.info("Outputting historical data to csv @ \"{}\"".format(historical_data_csv_filename))
    df_historical_data.to_csv(historical_data_csv_filename)


def run_bigquery_client_test() -> None:
    client = bigquery.Client()

    # Perform a query.
    QUERY = (
        'SELECT * FROM `bigquery-public-data.usa_names.usa_1910_2013` '
        'WHERE state = "TX" '
        'LIMIT 100')
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        logging.debug(row)


def run_storage_client_test() -> None:
    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    logging.debug(buckets)


if __name__ == "__main__":
    main()
