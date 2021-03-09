import pandas as pd 


class StockDataSource(object):
    def getHistoricalData(self) -> pd.DataFrame:
        raise NotImplementedError()
