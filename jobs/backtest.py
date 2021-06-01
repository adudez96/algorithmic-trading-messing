from util import datetime_to_date_string
from fastquant import backtest, get_stock_data
import yfinance as yf

from datetime import datetime, timedelta
import logging


def run_backtest():
    logging.info("Getting stock data...")
    start_date = datetime.today() - timedelta(days=1000)
    end_date = datetime(2020, 1, 1)
    print(datetime_to_date_string(start_date))
    print(datetime_to_date_string(end_date))
    df_stock_data = get_stock_data("CBA.AX",
        start_date=datetime_to_date_string(start_date),
        end_date=datetime_to_date_string(end_date),
        # start_date="2021-03-15",
    )
    # df_stock_data = yf.Ticker("CBA.AX").history(
    #     start=datetime_to_date_string(start_date),
    #     end=datetime_to_date_string(end_date)
    # )
    print(df_stock_data.head())

    logging.info("Backtesting...")
    df_res = backtest(
        "smac", df_stock_data,
        init_cash=1000,
        # commission=10,
        fast_period=15, slow_period=35,
    )

    print(df_res)
