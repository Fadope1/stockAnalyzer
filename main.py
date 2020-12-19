# this version only works on linux.
from matplotlib import pyplot as plt
from getStockData import stock_data
from PDFcreater import createPDF
import pandas as pd
import numpy as np
import argparse
import os

os.system("mkdir .tempPictures") # only works on linux

parser = argparse.ArgumentParser(description='Create PDF with stock information - Created by Fabian (fadop3).')

parser.add_argument("-s", "--stocks", type=str, nargs='+', help='Stock name like TSLA')
parser.add_argument("-i", "--intervals", type=str, nargs='+', help='Intervals interesting to you. E.g. 5y 1m 1w 1d')
parser.add_argument("-ind", "--indicators", type=str, default=[], nargs='+', help='Indicators to use available in talib. E.g. MACD EMA')

# use argparser to parse input_stocks, intervals, indicators
stocks = parser.parse_args().stocks # [ "MSFT", "TSLA" ]
intervals = parser.parse_args().intervals # [ "5y", "1y", "1m", "1w", "1d" ]
indicators = parser.parse_args().indicators #["MACD"]
stockData = stock_data()

for stock in stocks:
    for interval in intervals:
        rawStockData = stockData.get_history(stock=stock, timestamp=interval)

        if rawStockData is False:
            print("The data you are trying to receive couldnt be obtained...")
            break

        rawStockData.plot(figsize=(16, 9))
        plt.ylabel("Price in €")
        plt.xlabel("Dates")
        plt.savefig(f'./.tempPictures/{stock}{interval}.png')
        # plt.show()
        plt.close()

        if len(indicators) != 0:
            rawStockData = rawStockData.to_frame()
            for indicator in indicators: # x, y labels are wrong -> dates missing price range missing
                print(f"Downloading {stock} with {interval} and indicator {indicator}.")
                indicatorData = pd.DataFrame(stockData.get_indicator(rawStockData[ "Close" ], indicator)) # cant u just read it in the right way -> no transpose???
                if len(indicatorData) <= 10:
                    indicatorData = indicatorData.transpose()

                rawStockData.reset_index(drop=True, inplace=True)
                indicatorData.reset_index(drop=True, inplace=True)
                indicatorData = pd.concat([rawStockData, indicatorData], axis=1)

                indicatorData.plot(figsize=(16, 9)) # date missing ??? -> ADD PLEASE BUT HOW??? HOW DOES PANDAS WORK LOL
                plt.ylabel("Price in €")
                plt.xlabel("Dates")
                plt.savefig(f'./.tempPictures/{stock}{interval}{indicator}.png')
                # plt.show()
                plt.close()

for stock in stocks:
    createPDF(stock, intervals, indicators)

os.system("rm ./.tempPictures/*.png") # only works on linux
os.system("rmdir ./.tempPictures")
