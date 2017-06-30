# coding=UTF-8
__author__ = 'study_sun'

from algorithm import BaseAlgorithm
from entity import *

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


def prefer(preferReds, preferBlues, excludeReds, excludeBlues, count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctListPreferAndExclude(preferReds, excludeReds, WelfareLotteryRedBallCount, WelfareLotteryRedBallMinValue, WelfareLotteryRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctListPreferAndExclude(preferBlues, excludeBlues, WelfareLotteryBlueBallCount, WelfareLotteryBlueBallMinValue, WelfareLotteryBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls



class WelfareLottery(ColoredLottery):

    @classmethod
    def red_count(cls):
        return WelfareLotteryRedBallCount

    @classmethod
    def max_red(cls):
        return WelfareLotteryRedBallMaxValue

    @classmethod
    def blue_count(cls):
        return WelfareLotteryBlueBallCount

    @classmethod
    def max_blue(cls):
        return WelfareLotteryBlueBallMaxValue

    @classmethod
    def random(cls, count=1):
        results = random(count)
        # 港真,不太可能出现相同的两注吧,比中大奖概率还低
        if count==1:
            return results[0]
        else:
            return results


class WelfareLotteryDraw(ColoredLotteryDraw):
    pass

