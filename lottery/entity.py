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

class LOObject(object):

    @classmethod
    def all_keys(cls):
        return []

    @classmethod
    def all_desc_keys(cls):
        return []

    #短描述肯定自己写咯
    def short_desc(self):
        return ''

    def full_desc(self):
        format = u''
        for i, key in enumerate(self.all_keys()):
            v = getattr(self, key)
            if isinstance(v, float):
                v = str(v)
            elif isinstance(v, int):
                v = str(v)
            elif isinstance(v, list):
                v = ','.join(v)
            format += self.all_desc_keys()[i] + ' : ' + v + ' \n'
        return format

    def __str__(self):
        return self.full_desc()

# 做个基类吧
class Lottery(LOObject):

    def __init__(self):
        pass

    def award(self, draw):
        pass


    # 产生一个随机,没有任何算法的
    @classmethod
    def random(self, count=1):
        pass

    @classmethod
    def gene(self, policy):
        pass


# 红蓝双色的彩票基类,实际上就是双色球和大乐透啦
class ColoredLottery(Lottery):

    RED_BALLS_KEY = 'red_balls'
    RED_BALLS_CHINESE_KEY = u'红球'

    BLUE_BALLS_KEY = 'blue_balls'
    BLUE_BALLS_CHINESE_KEY = u'篮球'

    @classmethod
    def min_red(cls):
        return 1

    @classmethod
    def max_red(cls):
        pass

    @classmethod
    def red_count(cls):
        pass

    @classmethod
    def min_blue(cls):
        return 1

    @classmethod
    def max_blue(cls):
        pass

    @classmethod
    def blue_count(cls):
        pass

    @classmethod
    def all_keys(cls):
        return []

    @classmethod
    def all_desc_keys(cls):
        return []

    def __init__(self):
        super(Lottery, self).__init__()
        self.red_balls = []
        self.blue_balls = []


# 开奖信息
class LotteryDraw(LOObject):

    SERIAL_KEY = 'serial'
    SERIAL_CHINESE_KEY = u'期号'

    DATE_KEY = 'l_date'
    DATE_CHINESE_KEY = u'开奖日期'

    SALES_KEY = 'sales'
    SALES_CHINESE_KEY = u'销售额'

    # 奖池的钱不是这期总的奖金哦
    POND_KEY = 'pond'
    POND_CHINESE_KEY = u'奖池奖金'


    # 双色球大乐透的1-3等奖金都是不固定的,但是苦于数据不全,所以暂时不做记录了

    def __init__(self):
        super(LOObject, self).__init__()
        self.serial = ''
        self.l_date = ''
        self.sales = 0
        self.pond = 0

    def parse_sqlresult(self, sqlresult):
        pass


class ColoredLotteryDraw(LotteryDraw, ColoredLottery):

    def __init__(self):
        super(LotteryDraw, self).__init__()
        super(ColoredLottery, self).__init__()

    def level(self, lottery):
        return self.rule.level(lottery)

    def winnings(self, lottery):
        return self.rule.winnings(lottery)


