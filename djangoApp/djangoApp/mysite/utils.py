import requests
import pandas as pd
import json
import datetime

from binance.client import Client

api_key = "7Y76Gcu8fSXBfwYwYLRflQG4ifzDVim5G09SiMAxcxRQWtCPuO4XGOivuqB8BeQ7"
api_secret = "DaMfF3glGm2jc2OuMyi8azdi4el8krv2N2XohaAi1qqG2DISgPpSKiv3WEB2o6UH"

def convert_to_df(data):
    """Convert the result JSON in pandas dataframe"""

    # Only need the first 6 data inputs [date, open, high, low, close, volume] (12 are given)
    data = [item[:6] for item in data]

    '''df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    # Set index to date
    df = df.set_index('date')

    #Sort data according to date

    df = df.sort_values(by=['date'])'''

    df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close', 'volume'])

    df.reset_index()

    #change to datetime

    #df['date_formatted'] = pd.to_datetime(df['date'], origin='2009-01-09')
    df['date_formatted'] = [datetime.datetime.fromtimestamp(int(i)/1000) for i in df['date']]

    #sort data according to date

    df = df.sort_values(by=['date_formatted'])

    #print(df.head())

    #Change the datatype

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)

    print(df.head())

    #Checks
    df.head()
    df.info()

    return df

def get_data(from_symbol='BTC', to_symbol='USDT', rate='30m'):
    client = Client(api_key, api_secret)

    #res = client.get_exchange_info()
    #res = client.get_symbol_info('BTCUSD')
    #print(client.response.headers)

    #res_from_json = json.dumps(res, indent=2)

    #print(res_from_json)

    # Format symbol
    symbol = from_symbol + to_symbol

    # get timestamp of earliest date data is available
    #timestamp = client._get_earliest_valid_timestamp(symbol, rate)

    #print(timestamp)

    # get current time
    currTime = datetime.datetime.now()

    # request historical candle (or klines) data
    bars = client.get_historical_klines('BTCUSDT', rate, str(currTime - datetime.timedelta(1)), str(currTime), limit=1000)

    # Return the json data
    return bars

'''if __name__ == "__main__":
    data = get_data()
    dataDF = convert_to_df(data)'''