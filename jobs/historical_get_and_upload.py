from config import config
from datasources.stock_data.ameritrade import AmeritradeDatasource
from google.cloud import bigquery
import logging
import os


historical_data_csv_filename = "{}/historical.csv".format(os.getcwd())


def historical_get_and_upload(exchange: str) -> None:
    logging.info("Getting symbols...")
    # eoddata_datasource = EODDataDatasource()
    # symbols = eoddata_datasource.get_stock_symbol_list(exchange=exchange)
    symbols = ["AAPL", "TSLA", "GOOG", "MCD", "BP", "WMT", "GS", "JPM", "BAC", "BNS"]  # for testing
    logging.debug(symbols)

    logging.info("Getting historical data from the internet...")
    ameritrade_datasource = AmeritradeDatasource()
    df_historical_data = ameritrade_datasource.getHistoricalData(symbols=symbols)
    df_historical_data = df_historical_data.sort_values(by=["date", "symbol"])
    df_historical_data["exchange"] = exchange

    logging.info("Outputting historical data to csv @ \"{}\"...".format(historical_data_csv_filename))
    df_historical_data.to_csv(historical_data_csv_filename)

    logging.info("Uploading data to BigQuery...")
    client = bigquery.Client()
    db_table_config = config["storage"]["bigquery"]["eod-price-data"]
    dataset_ref = client.dataset(db_table_config["dataset"])
    table_ref = dataset_ref.table(db_table_config["table"])

    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.autodetect = True
    job_config.ignore_unknown_values = True
    job = client.load_table_from_dataframe(
        df_historical_data,
        table_ref,
        job_config=job_config
    )

    job.result()
