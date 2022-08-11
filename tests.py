import api
import time
import indicators
import pandas as pd
import matplotlib.pyplot as plt
import strategies
import core

btc = core.Data(api.getPrice('BTC', '1h', '1Y'))
eth = core.Data(api.getPrice('ETH', '1h', '1Y'))

print(btc.dataFrame.corrwith(eth.dataFrame))