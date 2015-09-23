# coding=UTF-8
from flask import Flask,request
import random
import json
import SuperLotto
import BaseAlgorithm
import string

app = Flask(__name__)

def lotteryAlgorithm(type, algorithm, count):
    if type == None:
        type = 'superlotto'
    if algorithm == None:
        algorithm = 'random'
    if count == None:
        count = 1
    count = int(count)
    #目前只支持随机嘻嘻

    if type.lower() == 'SuperLotto'.lower():
        if algorithm.lower() == 'random':
            return SuperLotto.random(count)
        else:
            return SuperLotto.random(count)
    else:
        return SuperLotto.random(count)



@app.route('/')
def hello_world():
    return 'Hello Lottery'


@app.route('/lottery')
def lottery():
    # 参数优先看 类型(大乐透|福彩)，其次看玩法(随机|真算)，最后看注数，默认值是大乐透，随机，一注
    type = request.args.get('type')
    algorithm = request.args.get('algorithm')
    count = request.args.get('count')
    ls = lotteryAlgorithm(type, algorithm, count)

    return json.dumps({'status' : 'success', 'lottery_list' : ls})


if __name__ == '__main__':
    app.run()
