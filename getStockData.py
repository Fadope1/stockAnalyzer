from tradingview_ta import TA_Handler, Interval
from currency_converter import CurrencyConverter
from talib.abstract import *
import talib
import yfinance as yf
import numpy as np

class stock_data:
    def get_history(self, stock, timestamp, interest="Close") -> "float array":
        # check if data is 0 -> return False
        # this will download a given stock
        c = CurrencyConverter()
        try:
            stockTicker = yf.Ticker(stock)
            stockHistory = stockTicker.history(period=timestamp)[ interest ].apply(lambda x: c.convert(x, "USD", "EUR"))
            if len(stockHistory) <= 1:
                return False
        except:
            print(f"{stock} is currently not available. Returning False")
            return False

        return stockHistory

    def get_analytics(self, stock_name) -> "str array":
        # this will return all the information retrieved from the internet
        stockExchanges = ["FWB", "SWB", "XETR"]
        data = []

        # get information from tradingview.com
        stock_data = TA_Handler()
        stock_data.set_symbol_as(stock_name)
        stock_data.set_screener_as_stock("germany")
        stock_data.set_interval_as(Interval.INTERVAL_1_MONTH)

        for stockExchange in stockExchanges:
            try:
                stock_data.set_exchange_as_crypto_or_stock(stockExchange)
                data.append(stock_data.get_analysis().summary)
                # print(f"Got it from {stockExchange}")
                break
            except Exception:
                print(f"{stock_name} not in {stockExchange}." \
                "Trying other Exchanges in Germany.")
                continue

        # get information from yahoo finances
        stockTicker = yf.Ticker(stock_name)
        print(stockTicker.info, stockTicker.actions, stockTicker.financials, \
        stockTicker.balance_sheet, stockTicker.cashflow, stockTicker.earnings, \
        stockTicker.nextEvent)

        return data

    def get_news(self, stock_name):
        # from stocknews import StockNews
        # sn = StockNews(stock_name, wt_key="7997ace6c0420600c74fb29944c258bb", news_file=f'{stock_name}news.csv', summary_file='data.csv', save_news=True)
        # df = sn.summarize()
        # print(df)
        pass

    def get_indicator(self, stock_data, indicator):
        # this will return the indicator for the stock
        return getattr(talib, indicator)(np.array(stock_data, dtype="double"))
