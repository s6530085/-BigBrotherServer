# coding=UTF-8
from algorithm import BaseAlgorithm
from entity import *
# const
SuperLottoRedBallCount = 5
SuperLottoBlueBallCount = 2
SuperLottoTotalBallCount = SuperLottoRedBallCount + SuperLottoBlueBallCount
SuperLottoRedBallMinValue = 1
SuperLottoRedBallMaxValue = 35
SuperLottoBlueBallMinValue = 1
SuperLottoBlueBallMaxValue = 12

def random(count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctList(SuperLottoRedBallCount, SuperLottoRedBallMinValue, SuperLottoRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctList(SuperLottoBlueBallCount, SuperLottoBlueBallMinValue, SuperLottoBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls

#这里的blues等已经校验过，无需再次校验
def prefer(preferReds, preferBlues, excludeReds, excludeBlues, count = 1):
    ls = []
    for i in range(0, count):
        redBalls = BaseAlgorithm.geneRandomDistinctListPreferAndExclude(preferReds, excludeReds, SuperLottoRedBallCount, SuperLottoRedBallMinValue, SuperLottoRedBallMaxValue)
        blueBalls = BaseAlgorithm.geneRandomDistinctListPreferAndExclude(preferBlues, excludeBlues, SuperLottoBlueBallCount, SuperLottoBlueBallMinValue, SuperLottoBlueBallMaxValue)
        ls.append(redBalls + blueBalls)
    return ls


class SuperLotto(ColoredLottery):

    @classmethod
    def red_count(cls):
        return SuperLottoRedBallCount

    @classmethod
    def max_red(cls):
        return SuperLottoRedBallMaxValue

    @classmethod
    def blue_count(cls):
        return SuperLottoBlueBallCount

    @classmethod
    def max_blue(cls):
        return SuperLottoBlueBallMaxValue

    @classmethod
    def random(cls, count=1):
        results = random(count)
        # 港真,不太可能出现相同的两注吧,比中大奖概率还低
        if count==1:
            return results[0]
        else:
            return results


class SuperLottoDraw(ColoredLotteryDraw):
    pass
