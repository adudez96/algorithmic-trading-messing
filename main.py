from config import config

from google.cloud import bigquery, storage

import logging
import sys


def main() -> None:
    setup_logging()
    logging.info("Running!")
    # run_bigquery_client_test()
    # run_storage_client_test()
    logging.debug(get_ameritrade_creds())


def get_ameritrade_creds() -> str:
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(config["storage"]["tdameritrade-api-creds"]["bucket"])
    api_key = bucket.get_blob(config["storage"]["tdameritrade-api-creds"]["blob"]).download_as_string()

    return api_key


def setup_logging() -> None:
    # Clear all logging handlers to make way for custom
    logging.getLogger().handlers = []

    log_format = '[%(asctime)s] [%(levelname)s] {%(filename)s:%(lineno)d} %(message)s'
    formatter = logging.Formatter(log_format)

    file_handler = logging.FileHandler(filename='tmp.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.getLevelName(config["logging"]["file-level"]))
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.getLevelName(config["logging"]["stdout-level"]))

    logging.getLogger().setLevel(logging.NOTSET)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(stdout_handler)


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
