import csv

from binance.client import Client

def calculateHeiken(pair):
    client = Client()
    csvData = [['time', 'open', 'high', 'low', 'close', 'volume','closetime','quotevol','numtrades','takerbuybasevol','takerbuyquotevol','ignore']] + client.get_historical_klines(pair, Client.KLINE_INTERVAL_15MINUTE, "1 day ago UTC")

    with open('bitcoinCandlePrices.csv', 'w') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerows(csvData)
    csvFile.close()

    from astropy.io import ascii
    data = ascii.read("bitcoinCandlePrices.csv")

    data.remove_column('volume')


    data.write('bitcoinCandlePricesRevised.csv', format='csv',overwrite=True)

    import datetime as dt
    import matplotlib.dates as mdates 
    import matplotlib.pyplot as plt
    import pandas_datareader as web
    from mpl_finance import candlestick2_ochl

    from astropy.table import Table
    #from astropy.io import ascii

    fig= plt.figure(figsize=(20,10))

    t = Table.read("bitcoinCandlePricesRevised.csv")

    ax = plt.subplot()
    candlestick2_ochl(ax, t['open'], t['close'], t['high'], t['low'], width=2, colorup='g', colordown='r', alpha=1.0)

    ax.grid(True)

    fig.suptitle('USD-BTC Candlestick Chart', fontsize=20)
    plt.xlabel('Time', fontsize=16)
    plt.ylabel('Price USD', fontsize=16)

    fig.savefig('bitcoinCandleChart.jpg')

    # Modify table to be HA values
    from astropy.table import Table

    t = Table.read("bitcoinCandlePricesRevised.csv")

    def haLow(row):
        ha_low = min(t[row]['low'], t[row]['open'], t[row]['close'])
        return ha_low

    def haHigh(row): 
        ha_high = max(t[row]['high'], t[row]['open'], t[row]['close'])
        return ha_high 

    def haOp(row): 
        row-=1
        data = t[row]['open'] + t[row]['close']
        ha_op = data/2
        return ha_op

    def haClose(row):
        data = t[row]['open'] + t[row]['high'] + t[row]['low'] + t[row]['close']
        ha_close = data/4
        return ha_close

    for x in range(len(t)): 
        t[x]['low'] = haLow(x)
        t[x]['high'] = haHigh(x)
        t[x]['open'] = haOp(x)
        t[x]['close'] = haClose(x)

    #t.write('bitcoinHA', format='csv')
    t.write('heikenAshi.csv', format='csv',overwrite=True)
