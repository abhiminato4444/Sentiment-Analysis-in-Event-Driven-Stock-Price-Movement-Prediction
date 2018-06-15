#!/usr/bin/env python3
import os
import sys

import json
from datetime import datetime  
from datetime import timedelta


from yahoo_finance import repeat_download

# collect the tickers to crawl their corresponding price information
def get_tickers(date):
    f = open('./input/news/' + date[:4] + '/news_' + date + '.csv')
    tickers = set()
    for l in f:
        l = l.strip().split(',')
        ticker = l[0]
        tickers.add(ticker)
    return(tickers)

def save_daily_price(end_date, tickers):
    print(tickers)
    datetime_object = datetime.strptime(end_date, '%Y%m%d')
    start_date = (datetime_object - timedelta(days=28)).date().strftime('%Y%m%d')
    output = './input/prices/' + end_date[:4] + '/price_' + end_date
    end_date = '29991231' # up to the most recent news
    price_set = {}
    price_set['^GSPC'] = repeat_download('^GSPC', start_date, end_date) # download S&P 500
    for num, ticker in enumerate(tickers):
        price_set[ticker] = repeat_download(ticker, start_date, end_date)
        with open(output, 'w') as outfile:
            json.dump(price_set, outfile, indent=4)
        print(num, ticker)


def main():
    cur_date = sys.argv[1]
    tlist = get_tickers(cur_date)
    save_daily_price(cur_date, tlist)

if __name__ == "__main__":
    main()

