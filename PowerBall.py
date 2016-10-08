# coding=UTF-8
__author__ = 'study_sun'

import BaseAlgorithm

# 其实是5个白球+1个篮球,懒得改了
# const
PowerBallRedBallCount = 5
PowerBallBlueBallCount = 1
PowerBallTotalBallCount = PowerBallRedBallCount + PowerBallBlueBallCount
PowerBallRedBallMinValue = 1
PowerBallRedBallMaxValue = 69
PowerBallBlueBallMinValue = 1
PowerBallBlueBallMaxValue = 26

def random(count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctList(PowerBallRedBallCount, PowerBallRedBallMinValue, PowerBallRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctList(PowerBallBlueBallCount, PowerBallBlueBallMinValue, PowerBallBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls

#这里的blues等已经校验过，无需再次校验
def prefer(preferReds, preferBlues, excludeReds, excludeBlues, count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctListPreferAndExclude(preferReds, excludeReds, PowerBallRedBallCount, PowerBallRedBallMinValue, PowerBallRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctListPreferAndExclude(preferBlues, excludeBlues, PowerBallBlueBallCount, PowerBallBlueBallMinValue, PowerBallBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls
