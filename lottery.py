# coding=UTF-8
from flask import Flask,request
import json
from types import *
import SuperLotto
import WelfareLottery

app = Flask(__name__)

def validateBalls(balls, type, isRed):
    validated = []
    minValue = 1
    if type == 'superlotto':
        if isRed:
            length
            maxValue = SuperLotto.SuperLottoRedBallMaxValue
        else:
            maxValue = SuperLotto.SuperLottoBlueBallMaxValue


    for (i in range(0, len(balls))):
        try:
            a = int(balls[i])
            if a >= minValue && a <= maxValue:
                if not validated.__contains__(a):
                    validated.append(a)
        except ValueError:
            None
    validated = validated[0:length]
    return validated.sort()


def lotteryAlgorithm(type, algorithm, count, blues = [], reds = []):
    if type == None:
        type = 'superlotto'
    else:
        type = type.lower()

    if algorithm == None:
        algorithm = 'random'
    else:
        algorithm = algorithm.lower()

    if count == None:
        count = 1
    else:
        try:
            count = int(count)
        except ValueError:
            count = 1
        #最多不超过一百个
        if count <= 0:
            count = 1
        elif count > 100 :
            count = 100


    if algorithm == 'random':
        #目前所谓篮球红球的偏好只是非选他们不可而已，以后再来复式的算法
        if blues == None:
            blues = []
        else:
            #所以目前只取前几个元素而已，校验一下是否是数字,以及数字范围和数量
            if type == 'walfarelottery'
                blues = validateBalls
            else:
                blues =

        if reds == None:
            reds = []
        else:
            reds = [1]


    #目前只支持随机嘻嘻,所谓recommend都是假的
    if type.lower() == 'walfarelottery':
        if algorithm.lower() == 'prefer':
            return WelfareLottery.recommend(blues, reds, count)
        else:
            return WelfareLottery.random(count)
    else:
        if algorithm.lower() == 'prefer':
            return SuperLotto.recommend(blues,reds,count)
        else:
            return SuperLotto.random(count)



@app.route('/')
def hello_world():
    return 'Hello Lottery'


@app.route('/lottery')
def lottery():

    # 参数优先看 类型(大乐透|福彩)，其次看玩法(随机|真算)，最后看注数，默认值是大乐透，随机，一注
    algorithm = request.args.get('algorithm')
    count = request.args.get('count')
    blues = request.args.get('preferblues')
    reds = request.args.get('preferreds')
    ls = lotteryAlgorithm(type, algorithm, count, blues, reds)

    return json.dumps({'status' : 'success', 'lottery_list' : ls})


if __name__ == '__main__':
    app.run()
