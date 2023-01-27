import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import mplfinance
import matplotlib.dates as mpl_dates
from polygon import RESTClient
from dotenv import load_dotenv
load_dotenv()

import os
import datetime

POLYGON_API_KEY = os.getenv('POLYGON_KEY')
client = RESTClient(POLYGON_API_KEY)

matplotlib.use('Agg')

def getStockData(ticker):
    plt.style.use('dark_background')

    # start_date and end_date are strings in the format 'YYYY-MM-DD'. Dates must be within the last 2 years.
    end_date = datetime.datetime.now()
    start_date = (end_date - datetime.timedelta(days=30)).strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')
    past = client.get_aggs(ticker, 1, 'day', start_date, end_date, adjusted=True)
    stock_prices = pd.DataFrame({'date': np.array([datetime.datetime.fromtimestamp(i.timestamp/1000).strftime('%Y-%m-%d')
                                               for i in past]),
                             'open': [i.open for i in past],
                             'close': [i.close for i in past],
                             'high': [i.high for i in past],
                             'low': [i.low for i in past],
                             'volume': [i.volume for i in past],
                             'vwap': [i.vwap for i in past]})
    ohlc = stock_prices.loc[:, ['open', 'high', 'low', 'close', 'volume', 'vwap']]
    stock_prices['date'] = pd.to_datetime(stock_prices['date'])
    ohlc.set_index(stock_prices['date'], inplace=True)

    # Plot
    mc = mplfinance.make_marketcolors(up='#1EB854',down='#ff0000', edge='inherit', wick={'up':'#1EB854','down':'#ff0000'}, volume='#1EB854')
    customstyle = mplfinance.make_mpf_style(base_mpf_style='nightclouds',
                                 facecolor='#171212', marketcolors=mc)
    mplfinance.plot(ohlc, type='candle', style=customstyle,
            title=f'{ticker}, {start_date} - {end_date}',
            ylabel='Price ($)',
            ylabel_lower='Shares \nTraded',
            volume=True)
    plt.savefig('static/candle-bars.png', facecolor='#171212')
    dates = stock_prices['date'].dt.strftime('%Y-%m-%d').tolist()
    return (start_date, end_date), dates, ohlc

if __name__ == '__main__':
    data = getStockData('AAPL')
    print(data)
    print(data[2]['close'][0])