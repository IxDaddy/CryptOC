import json
import numpy as np
import requests
import pandas as pd
import matplotlib as plot
import matplotlib.pyplot as plt
import time

API_KEY = '2CkVxSwnFFkotVH0EEoU9NuOzuN'
DOMAIN = 'https://api.glassnode.com/'


def checkResponse(response):
    if response.status_code == 400:
        raise Exception('Bad request : ' + response.text)
    if "forbidden" in response.text:
        raise Exception('Bad request : ' + response.text)


def checkTimeFrame(t):
    if not (t == '10m' or t == '1h' or t == '24h' or t == '1w' or t == '1month'):
        raise Exception("Wrong TimeFrame selected : " + t)


# translate 1h, 1d, 1week, 1month, 1Y, 5Y, 1OY, all-time
def timeToTimestamp(t):
    if t == '10m':
        return 60 * 10
    elif t == '1h':
        return 60 * 60
    elif t == '24h':
        return 60 * 60 * 24
    elif t == '1w':
        return 60 * 60 * 24 * 7
    elif t == '1month':
        return 60 * 60 * 24 * 31
    elif t == '1Y':
        return 60 * 60 * 24 * 365
    elif t == '5Y':
        return 60 * 60 * 24 * 365 * 5
    elif t == '10Y':
        return 60 * 60 * 24 * 365 * 10
    elif t == 'all-time':
        return int(time.time())
    else:
        raise Exception("Bad time format : " + t)


def getPrice(asset='BTC', t='10m', since='1Y'):
    checkTimeFrame(t)
    res = requests.get(DOMAIN + 'v1/metrics/market/price_usd_close',
                       params={'a': asset, 's': int(time.time()) - timeToTimestamp(since), 'i': t,
                               'api_key': API_KEY})
    checkResponse(res)
    df = pd.read_json(res.text, convert_dates=['t'])
    df.rename(columns={"t": "Time", "v": "Price"}, inplace=True)
    return df


def getIndicator(indicator, asset='BTC', t='10m', since='1Y'):
    checkTimeFrame(t)
    res = requests.get(DOMAIN + 'v1/metrics/indicators/' + indicator,
                       params={'a': asset, 's': int(time.time()) - timeToTimestamp(since), 'i': t,
                               'api_key': API_KEY})
    checkResponse(res)
    df = pd.read_json(res.text, convert_dates=['t'])
    df.rename(columns={"t": "Time", "v": "Value"}, inplace=True)
    return df


def getMiningHashRate(asset='BTC', t='10m'):
    pd.io.json._json.loads = lambda s, *a, **kw: json.loads(s)

    res = requests.get(DOMAIN + 'v1/metrics/mining/hash_rate_mean',
                       params={'a': asset, 'i': t, 'api_key': API_KEY})
    checkResponse(res)
    df = pd.read_json(res.text, convert_dates=['t'])
    df.rename(columns={"t": "Time", "v": "Value"}, inplace=True)
    return df


def getMiningDifficulty(asset='BTC', t='10m'):
    res = requests.get(DOMAIN + 'v1/metrics/mining/difficulty_latest',
                       params={'a': asset, 'i': t, 'api_key': API_KEY})
    checkResponse(res)
    df = pd.read_json(res.text, convert_dates=['t'])
    df.rename(columns={"t": "Time", "v": "Value"}, inplace=True)
    return df


def getMinerRevenueTotal(asset='BTC', t='10m'):
    res = requests.get(DOMAIN + 'v1/metrics/mining/revenue_sum',
                       params={'a': asset, 'i': t, 'api_key': API_KEY})
    checkResponse(res)
    df = pd.read_json(res.text, convert_dates=['t'])
    df.rename(columns={"t": "Time", "v": "Value"}, inplace=True)
    return df


def getLastPriceCurrency(asset='BTC', t='10m'):
    checkTimeFrame(t)
    res = requests.get(DOMAIN + 'v1/metrics/market/price_usd_close',
                       params={'a': asset, 's': int(time.time()) - timeToTimestamp(t), 'i': t, 'api_key': API_KEY})
    checkResponse(res)
    df = pd.read_json(res.text, convert_dates=['t'])
    df.rename(columns={"t": "Time", "v": "Price"}, inplace=True)
    return df
