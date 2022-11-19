import requests
import pandas as pd

from binance.client import Client

api_key = "7Y76Gcu8fSXBfwYwYLRflQG4ifzDVim5G09SiMAxcxRQWtCPuO4XGOivuqB8BeQ7"
api_secret = "DaMfF3glGm2jc2OuMyi8azdi4el8krv2N2XohaAi1qqG2DISgPpSKiv3WEB2o6UH"

def convert_to_df(data):
    """Convert the result JSON in pandas dataframe"""

    df = pd.DataFrame.from_dict(data, orient='index')

    df = df.reset_index()

    #Rename columns

    df = df.rename(index=str, columns={"index": "date", "1. open": "open",
    "2. high": "high", "3. low": "low", "4. close": "close"})

    #Change to datetime

    df['date'] = pd.to_datetime(df['date'])

    #Sort data according to date

    df = df.sort_values(by=['date'])

    #Change the datatype

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)

    #Checks
    df.head()
    df.info()

    return df

def main():
    client = Client(api_key, api_secret)

    #res = client.get_exchange_info()
    res = client.get_symbol_info('BTCUSD')
    print(client.response.headers)

    res_from_json = res.json()

    print(res_from_json)

if __name__ == "__main__":
    main()