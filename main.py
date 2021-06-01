from jobs.backtest import run_backtest
from jobs.historical_get_and_upload import historical_get_and_upload
from logger import setup_logging

from google.cloud import bigquery, storage

import logging


def main() -> None:
    logging.info("Setting up...")
    setup_logging()
    logging.info("Running!")

    # historical_get_and_upload("NYSE")
    run_backtest()

    logging.info("Done!")


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
