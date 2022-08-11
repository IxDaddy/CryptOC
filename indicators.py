import math


def movingAverage(data, length, firstValues=None):
    res = [firstValues] * length
    for i in range(len(data) - length):
        tmp = 0
        for j in range(length):
            tmp += data[i + j]
        res.append(tmp / length)
    return res


def minus(data, number):
    res = []
    for e in data:
        e -= number
        res.append(e)
    return res


def divide(data, number):
    res = []
    for e in data:
        e /= number
        res.append(e)
    return res


def log(data):
    res = []
    for e in data:
        e = math.log10(e)
        res.append(e)
    return res


def reduceLenght(data, start):
    res = []
    for i in range(start, len(data)):
        res.append(data[i])
    return res


def priceDelta(data):
    res = [0]
    for i in range(0, len(data) - 1):
        res.append(data[i] - data[i + 1])
    return res
