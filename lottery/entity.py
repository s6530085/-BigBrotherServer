# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
from enum import Enum, unique

reload(sys)
sys.setdefaultencoding('utf-8')


@unique
class LotteryType(Enum):
    SuperLotto = 0
    Walfare = 1
    PowerBall = 2

# 做个基类吧,强力球不怎么用,所以基类还是以乐透双色为准好了
class Lottery(object):

    def __init__(self):
        self.red_balls = []
        self.blue_balls = []
        self.date = ''

    # 产生一个随机,没有任何算法的
    def random(self):
        pass


# 开奖信息,比基础彩票要多一些元素
class LotteryT(Lottery):

    def __init__(self):
        super(Lottery, self).__init__()
        self
