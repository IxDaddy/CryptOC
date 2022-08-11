# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


import json
import numpy as np
import matplotlib as plot
import matplotlib.pyplot as plt
import pandas as pd

import api
import time

import core
import indicators
import post

ASSET = 'BTC'
TIMEFRAME = '10m'
SINCE = '24h'


def chartGenerator(df1, name1, df2=None, name2=None, df3=None, name3=None, df4=None, df5=None):
    ax = df1.plot(y=name1)
    if df2:
        bx = df2.plot(ax=ax, y=name2)
        if df3:
            cx = df2.plot(ax=ax, y=name2)
            if df3:
                cx = df3.plot(ax=bx, y=name3)

    plt.show()


def main():
    primary = core.Data(api.getPrice(ASSET, TIMEFRAME, SINCE))
    if len(primary.dataFrame['Price']) == 0:
        raise Exception('Cant get price values on : ' + ASSET + '|' + TIMEFRAME + '|' + SINCE)
    timeframeUnix = api.timeToTimestamp(TIMEFRAME)
    primary.dataFrame.plot(y='Price')
    post.postTelegram("Bot is starting...")
    # plt.show()

    while True:
        if int(time.time()) % timeframeUnix == 0:
            current = None
            while True:
                current = core.Data(api.getPrice(ASSET, TIMEFRAME, SINCE))
                if not current.dataFrame['Time'][len(current.dataFrame['Time']) - 1] == primary.dataFrame['Time'][
                    len(primary.dataFrame['Time']) - 1]:
                    primary.dataFrame = current.dataFrame
                    break
                time.sleep(10)

            if current is None:
                raise Exception("Data can't be downloaded!")
            else:
                print("Data has been correctly downloaded.")

            signal = current.signalMA(5, 20)
            if signal == 1:
                post.postTelegram("BUY")
            elif signal == -1:
                post.postTelegram("LOOSE")
            else:
                post.postTelegram("NEUTRAL")

            """
            primaryDataframe = pd.concat([primaryDataframe, currentDataframe], ignore_index=True)

            primaryDataframe.plot(y='Price')
            print(len(primaryDataframe['Price']))

            dfMA1 = pd.DataFrame(indicators.movingAverage(primaryDataframe['Price'], 50), columns=['MA50'])
            dfMA2 = pd.DataFrame(indicators.movingAverage(primaryDataframe['Price'], 200), columns=['MA200'])
            

            ax = primaryDataframe.plot(y='Price', color='Blue')
            bx = dfMA1.plot(ax=ax, y='MA50', color='Orange')
            dfMA2.plot(ax=bx, color='Green')

            plt.show()
            """


        else:
            time.sleep(1)


if __name__ == '__main__':
    main()

# convert to pandas dataframe
"""
priceDelta = [0.]
for i in range(1, len(dfBtc['v'])):
    priceDelta.append((dfBtc['v'][i] - dfBtc['v'][i - 1]) / dfBtc['v'][i - 1])
df = pd.DataFrame(priceDelta, columns=['priceDelta'])

dfSOPR = pd.read_json(res.text, convert_dates=['t'])

bestMoney = []

for i in range(10, 200):

    SOPR = MA(dfSOPR['v'], i, 1)

    btc = dfBtc['v']

    money = 0
    boughtPrice = 0
    tradeNumber = 0
    tradeWin = 0
    tradeLoose = 0
    tradeType = 0  # BUY=1 ; SELL=-1 ; NULL=0
    tradeBuyID = 1
    tradeSellID = -1

    for i in range(1000, len(SOPR)):
        if SOPR[i] > 1 and SOPR[i - 1] <= 1:

            #print("Sell : " + str(btc[i]))

            if boughtPrice < btc[i] and tradeType == tradeBuyID:
                tradeLoose += 1
                tradeNumber += 1
                money -= (btc[i] - boughtPrice) / btc[i]
            else:
                tradeWin += 1
                tradeNumber += 1
                money -= (btc[i] - boughtPrice) / btc[i]

            if boughtPrice != 0:
                money += ((btc[i] - boughtPrice) / btc[i]) * tradeBuyID

            boughtPrice = btc[i]
            tradeType = tradeSellID

        elif SOPR[i] < 1 and SOPR[i - 1] >= 1:

            #print("Buy : " + str(btc[i]))

            if boughtPrice > btc[i] and tradeType == tradeSellID:
                tradeLoose += 1
                tradeNumber += 1
            else:
                tradeWin += 1
                tradeNumber += 1
            if boughtPrice != 0:
                money += ((btc[i] - boughtPrice) / btc[i]) * tradeSellID

            boughtPrice = btc[i]
            tradeType = tradeBuyID

    bestMoney.append((money, i))

print(bestMoney)

bx = dfSOPR.plot(y='v')
plt.axhline(y=1, color='r', linestyle='-')
plt.show()
"""
