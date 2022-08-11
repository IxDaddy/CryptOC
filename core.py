import api
import matplotlib.pyplot as plt
import pandas as pd
import indicators

BUY = 1
SHORT = -1
NEUTRAL = 0


class Data:
    dataFrame = None

    def __init__(self, df):
        self.dataFrame = df

    def __int__(self, asset, timeframe, since):
        self.dataFrame = api.getPrice(asset, timeframe, since)

    def show(self, color='blue'):
        self.dataFrame.plot(y='Price')
        plt.show()

    def toList(self, name):
        return self[name].values.tolist()

    def signalMA(self, t1, t2):
        name1 = 'MA' + str(t1)
        name2 = 'MA' + str(t2)

        dfMA1 = pd.DataFrame(indicators.movingAverage(self.dataFrame['Price'], t1), columns=[name1])
        dfMA2 = pd.DataFrame(indicators.movingAverage(self.dataFrame['Price'], t2), columns=[name2])

        lenght1 = len(indicators.movingAverage(self.dataFrame['Price'], t1)) - 1
        lenght2 = len(indicators.movingAverage(self.dataFrame['Price'], t2)) - 1

        if dfMA1[name1][lenght1] > dfMA2[name2][lenght2] and dfMA1[name1][lenght1 - 1] <= dfMA2[name2][lenght2 - 1]:
            return BUY
        elif dfMA1[name1][lenght1] < dfMA2[name2][lenght2] and dfMA1[name1][lenght1 - 1] >= dfMA2[name2][lenght2 - 1]:
            return SHORT
        else:
            return NEUTRAL
