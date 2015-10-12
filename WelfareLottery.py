# coding=UTF-8
__author__ = 'study_sun'

import BaseAlgorithm
# const
WelfareLotteryRedBallCount = 6
WelfareLotteryBlueBallCount = 1
WelfareLotteryTotalBallCount = WelfareLotteryRedBallCount + WelfareLotteryBlueBallCount
WelfareLotteryRedBallMinValue = 1
WelfareLotteryRedBallMaxValue = 33
WelfareLotteryBlueBallMinValue = 1
WelfareLotteryBlueBallMaxValue = 16

#虽然其实可以复用，但理论上随机应该用随机的算法，而推荐应该用推荐的算法就不复用了
def random(count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctList(WelfareLotteryRedBallCount, WelfareLotteryRedBallMinValue, WelfareLotteryRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctList(WelfareLotteryBlueBallCount, WelfareLotteryBlueBallMinValue, WelfareLotteryBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls


def prefer(preferReds, preferBlues, count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctListExclude(preferReds, WelfareLotteryRedBallCount, WelfareLotteryRedBallMinValue, WelfareLotteryRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctListExclude(preferBlues ,WelfareLotteryBlueBallCount, WelfareLotteryBlueBallMinValue, WelfareLotteryBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls
