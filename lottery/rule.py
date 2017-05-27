# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
from enum import Enum, unique
from entity import LotteryType
from SuperLotto import *
from WelfareLottery import *

reload(sys)
sys.setdefaultencoding('utf-8')

# 大乐透是八等奖,双色球是六等,有点不太想用枚举,因为意义不大啊
# @unique
# class

# 其实不需要传type啊,如果参数就已经是类型了的话,当然我们也支持直接传数组,不过因为双色球和大乐透都是7个数字,所以得传([5],[2])这样区分
def lottery_level(lotteries, target, type=LotteryType.SuperLotto):
    levels = []
    for lottery in lotteries:
        if isinstance(lottery, SuperLotto):
            i = 100
        elif isinstance(lottery, WelfareLottery):
            i = 100
        elif isinstance(lottery, tuple):
            # 要区分红蓝球数量哦
            i = 300
        else:
            # 纯list我是分不出到底是双色球还是大乐透的,只能看参数了
            i = 400


    return levels

# 此时的参数都已经保证类型化了
# 一等奖：选中5个前区号码及2个后区号码；
# 二等奖：选中5个前区号码及2个后区号码中的任意1个；
# 三等奖：选中5个前区号码；
# 四等奖：选中4个前区号码及2个后区号码；
# 五等奖：选中4个前区号码及2个后区号码中的任意1个；
# 六等奖：选中3个前区号码及2个后区号码或选中4个前区号码；
# 七等奖：选中3个前区号码及2个后区号码中的任意1个或选中2个前区号码及2个后区号码；
# 八等奖：选中3个前区号码或选中1个前区号码及2个后区号码或2个前区号码及2个后区号码中的任意1个或只选中2个后区号码。
def _superlotto_level(lottery, target):
    same_red = len([i for i in lottery.redBalls if i in target.redBalls])
    same_blue = len([i for i in lottery.blueBalls if i in target.blueBalls])
    if same_red == 5 and same_blue == 2:
        return 1
    elif same_red == 5 and same_blue == 1:
        return 2
    elif same_red == 5:
        return 3
    elif same_red == 4 and same_blue == 2:
        return 4
    elif same_red == 4 and same_blue == 1:
        return 5
    elif (same_red == 3 and same_blue == 2) or same_red == 4:
        return 6
    elif (same_red == 3 and same_blue == 1) or (same_red == 2 and same_blue == 2):
        return 7
    elif same_red == 3 or (same_red == 1 and same_blue == 2) or (same_red == 2 and same_blue == 1) or same_blue == 2:
        return 8
    else:
        return -1

def _welfarelottery_level(lottery, target):
    same_red = len([i for i in lottery.redBalls if i in target.redBalls])
    same_blue = len([i for i in lottery.blueBalls if i in target.blueBalls])
    if same_red == 6 and same_blue == 1:
        return 1
    elif same_red == 6:
        return 2
    elif same_red == 5 and same_blue == 1:
        return 3
    elif same_red == 5 or (same_red == 4 and same_blue == 1):
        return 4
    elif same_red == 4 or (same_red == 3 and same_blue == 1):
        return 5
    elif same_blue == 1:
        return 6
    else:
        return -1

# 低等的奖金是固定的,高等的奖金要结合奖池和中奖人数,暂时不做吧
def _superlotto_winnings(lottery, target):
    level = _superlotto_level(lottery, target)
    if level > 0:
        if level == 8:
            return 5
        elif level == 7:
            return 10
        elif level == 6:
            return 200
        elif level == 5:
            return 500
        elif level == 4:
            return 3000
        # 下面开始都是不固定的了
    else:
        return 0

def _welfarelottery_winnings(lottery, target):
    level = _welfarelottery_level(lottery, target)
    if level > 0:
        if level == 6:
            return 5
        elif level == 5:
            return 10
        elif level == 4:
            return 200
        elif level == 3:
            return 3000
        # 下面就是不定了
    else:
        return 0


class LotteryRule(object):
    # 传递对应的类型和球色,调用方不检查是否对应哦
    @classmethod
    def level(cls, type, lotteries):
        results = []
        for lottery in lotteries:
            if type == LotteryType.SuperLotto:
                i = 10
            else:
                i = 100
        return results


class LotteryWinnings(object):
    # 一般低等彩票是固定奖金的,但是头奖二奖则不然,不过我这里暂时没有数据,先占个位吧
    @classmethod
    def price(cls, type, level):
        pass