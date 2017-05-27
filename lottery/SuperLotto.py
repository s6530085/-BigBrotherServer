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

class SuperLotto(Lottery):

    def __init__(self, raw=None):
        super(Lottery, self).__init__()
        if raw == None:
            self.redBalls = []
            self.blueBalls = []


