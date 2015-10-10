# coding=UTF-8
__author__ = 'study_sun'

import BaseAlgorithm
# const
WalfareLotteryRedBallCount = 6
WalfareLotteryBlueBallCount = 1
WalfareLotteryTotalBallCount = WalfareLotteryRedBallCount + WalfareLotteryBlueBallCount
WalfareLotteryRedBallMinValue = 1
WalfareLotteryRedBallMaxValue = 33
WalfareLotteryBlueBallMinValue = 1
WalfareLotteryBlueBallMaxValue = 16

def random(count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctList(WalfareLotteryRedBallCount, WalfareLotteryRedBallMinValue, WalfareLotteryRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctList(WalfareLotteryBlueBallCount, WalfareLotteryBlueBallMinValue, WalfareLotteryBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls


def recommend(preferBlues, preferReds, count = 1):
    return random(count)

