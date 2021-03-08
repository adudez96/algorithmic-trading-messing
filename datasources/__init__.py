import pandas as pd 


class Datasource(object):
    def getHistoricalData(self) -> pd.DataFrame:
        raise NotImplementedError()
