from django.shortcuts import render
from yahoo_fin import stock_info as si
import yfinance as yf

def get_heatmap(request):

    snp500 = si.tickers_sp500()

    tickers = []
    deltas = []
    sectors =[]
    market_caps = []

    for ticker in snp500:
        
        try:
            ## create Ticker object
            stock = yf.Ticker(ticker)
            tickers.append(ticker)

            ## download info
            info = stock.info

            ## download sector
            sectors.append(info['sector'])

            ## download daily stock prices for 2 days
            hist = stock.history('2d')

            ## calculate change in stock price (from a trading day ago)
            deltas.append((hist['Close'][1]-hist['Close'][0])/hist['Close'][0])

            ## calculate market cap
            market_caps.append(info['sharesOutstanding'] * info['previousClose'])

            ## add print statement to ensure code is running
            print(f'downloaded {ticker}')
        except Exception as e:
            print(e)

    return render(request, 'analysis/heatmap.html')
