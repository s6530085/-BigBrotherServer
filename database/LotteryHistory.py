# coding=UTF-8
__author__ = 'study_sun'
import sqlite3
from lottery.entity import Lottery, LotteryDraw, ColoredLotteryDraw


# 存储彩票信息,目前做三件事,存储大乐透基础中奖信息,存储双色球的,存储算出的号
class LotteryHistory(object):

    DATABASE_NAME = 'lottery.db'
    SUPER_LOTTO_TABLE = 'super_lotto'
    WELFARE_LOTTERY_TABLE = 'welfare_lottery'

    def __init__(self):
        pass
