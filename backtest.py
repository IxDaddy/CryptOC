import api
import time
import indicators
import pandas as pd
import matplotlib.pyplot as plt
import strategies

BUY = 1
SHORT = -1
SIZE = 1


class trade:
    entryPrice = None
    exitPrice = None
    tradeType = None
    tradeResult = None
    size = None
    pnl = None
    index = None

    def __init__(self, entryPrice, tradeType, size):
        self.entryPrice = entryPrice
        self.tradeType = tradeType
        self.size = size
        # print("New trade created at " + str(self.entryPrice) + '$')

    def __str__(self):
        if not self.tradeResult:
            return str(int(self.entryPrice)) + '$|' + ('Buy ' if self.tradeType == 1 else 'Short') + '|' + str(self.size)
        else:
            return str(int(self.entryPrice)) + '$|' + str(
                int(self.exitPrice)) + '$|' + ('Buy ' if self.tradeType == 1 else 'Short') + '|' + (
                       'Won ' if self.tradeResult == 1 else 'Lost') + '|' + str(
                self.size) + '|' + str(float("{0:.3f}".format(self.pnl)))


class backtestResult:
    money = 0
    tradeNumber = 0
    tradeWin = 0
    tradeLoose = 0

    currentTrade = None

    tradeBuyID = 1
    tradeSellID = -1

    tradeList = []

    def __str__(self):
        return str(float("{0:.3f}".format(self.money))) + '$|' + str(self.tradeWin) + 'win|' + str(
            self.tradeLoose) + 'lost\n'

    def tradeHistory(self):
        for e in self.tradeList:
            print(e)
        print("Current trade : " + str(self.currentTrade))


ASSET = 'BTC'
TIMEFRAME = '1h'
SINCE = '1Y'
INDICATOR = 'RIBBONS'
STRATEGIES = 'MA50-200'


def backtest():
    datas = api.getPrice(ASSET, TIMEFRAME, SINCE)

    dfMA1 = pd.DataFrame(indicators.movingAverage(datas['Price'], 50), columns=['MA50'])
    dfMA2 = pd.DataFrame(indicators.movingAverage(datas['Price'], 200), columns=['MA200'])

    ax = datas.plot(y='Price', color='Blue')
    bx = dfMA1.plot(ax=ax, y='MA50', color='Orange')
    dfMA2.plot(ax=bx, color='Green')

    plt.show()

    backtest = backtestResult()

    for i in range(200, len(dfMA1)):

        price = datas['Price'][i]

        # BUY
        if dfMA1['MA50'][i] > dfMA2['MA200'][i] and dfMA1['MA50'][i - 1] <= dfMA2['MA200'][i - 1]:
            # Close last trade
            if backtest.currentTrade is not None:
                backtest.currentTrade.exitPrice = price
                backtest.currentTrade.pnl = ((
                                                         price - backtest.currentTrade.entryPrice) / price) * backtest.currentTrade.tradeType
                backtest.currentTrade.tradeResult = 1 if backtest.currentTrade.pnl > 0 else -1
                if backtest.currentTrade.tradeResult == 1:
                    backtest.tradeWin += 1
                else:
                    backtest.tradeLoose += 1
                backtest.tradeNumber += 1
                backtest.money += backtest.currentTrade.pnl
                backtest.tradeList.append(backtest.currentTrade)

            # Create new trade
            backtest.currentTrade = trade(price, BUY, SIZE)

        # SHORT
        elif dfMA1['MA50'][i] < dfMA2['MA200'][i] and dfMA1['MA50'][i - 1] >= dfMA2['MA200'][i - 1]:
            # Close last trade
            if backtest.currentTrade is not None:
                backtest.currentTrade.exitPrice = price
                backtest.currentTrade.pnl = ((
                                                         price - backtest.currentTrade.entryPrice) / price) * backtest.currentTrade.tradeType
                backtest.currentTrade.tradeResult = 1 if backtest.currentTrade.pnl > 0 else -1
                if backtest.currentTrade.tradeResult == 1:
                    backtest.tradeWin += 1
                else:
                    backtest.tradeLoose += 1
                backtest.tradeNumber += 1
                backtest.money += backtest.currentTrade.pnl
                backtest.tradeList.append(backtest.currentTrade)

            # Create new trade
            backtest.currentTrade = trade(price, SHORT, SIZE)

    backtest.tradeHistory()
    print(backtest)

    print(indicators.reduceLenght(dfMA1['MA50'], 0))

    priceList = indicators.movingAverage(datas['Price'].values.tolist(), 50)
    mm = datas['Price'].values.tolist()

    df1 = pd.DataFrame(priceList, columns='data')
    df2 = pd.DataFrame(mm, columns='data')

    print(df1)
    print(df2)

    print(df1.corrwith(df2))


if __name__ == '__main__':
    backtest()
