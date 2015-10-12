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
            length = SuperLotto.SuperLottoRedBallCount
            maxValue = SuperLotto.SuperLottoRedBallMaxValue
        else:
            length = SuperLotto.SuperLottoBlueBallCount
            maxValue = SuperLotto.SuperLottoBlueBallMaxValue
    else:
        if isRed:
            length = WelfareLottery.WelfareLotteryRedBallCount
            maxValue = WelfareLottery.WelfareLotteryRedBallMaxValue
        else:
            length = WelfareLottery.WelfareLotteryBlueBallCount
            maxValue = WelfareLottery.WelfareLotteryBlueBallMaxValue

    for i in range(0, len(balls)):
        try:
            a = int(balls[i])
            if a >= minValue and a <= maxValue:
                if not validated.__contains__(a):
                    validated.append(a)
        except ValueError:
            None

    validated = validated[0:length]
    validated.sort()
    return validated


def lotteryAlgorithm(type, algorithm, count, reds = [], blues = []):
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
        elif count > 100:
            count = 100

    if blues == None:
        blues = []
    else:
        blues = blues.split(',')
    if reds == None:
        reds = []
    else:
        reds = reds.split(',')

    if algorithm == 'prefer':
        #目前所谓篮球红球的偏好只是非选他们不可而已，以后再来复式的算法
        #所以目前只取前几个元素而已，校验一下是否是数字,以及数字范围和数量
        blues = validateBalls(blues, type, False)
        reds = validateBalls(reds, type, True)
    #目前只支持随机嘻嘻,所谓recommend都是假的
    if type.lower() == 'welfarelottery':
        if algorithm.lower() == 'prefer':
            return WelfareLottery.prefer(reds, blues, count)
        else:
            return WelfareLottery.random(count)
    else:
        if algorithm.lower() == 'prefer':
            return SuperLotto.prefer(reds, blues, count)
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
    reds = request.args.get('preferreds')
    blues = request.args.get('preferblues')
    ls = lotteryAlgorithm(type, algorithm, count, reds, blues)

    return json.dumps({'status' : 'success', 'lottery_list' : ls})


if __name__ == '__main__':
    app.run()
