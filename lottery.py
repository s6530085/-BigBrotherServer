# coding=UTF-8
from flask import Flask
import random
import json

def geneRandomDistinctList(totalCount, minValue, maxValue):
    sourceList = []
    while (len(sourceList) < totalCount) :
        while (1):
            r = random.choice(range(minValue,maxValue))
            if not (r in sourceList):
                sourceList.append(r)
                break
    sourceList.sort()
    return sourceList


def geneDLT():
    reds = geneRandomDistinctList(5, 1, 35)
    blues = geneRandomDistinctList(2, 1, 12)
    return reds + blues

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Lottery'


@app.route('/lottery')
def lottery():
    ls = geneDLT()
    s = map(str, ls)
    return json.dumps({'status' : 'success', 'lottery_list' : [s]})

if __name__ == '__main__':
    app.run()
