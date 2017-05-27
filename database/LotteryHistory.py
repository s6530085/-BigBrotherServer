# coding=UTF-8
__author__ = 'study_sun'
import sqlite3
from lottery.entity import Lottery



# 存储彩票信息,目前做三件事,存储大乐透基础中奖信息,存储双色球的,存储算出的号
class LotteryHistory(object):
    DATABASE_NAME = 'lottery.db'
    SUPER_LOTTO_TABLE = 'super_lotto'
    WELFARE_LOTTERY_TABLE = 'welfare_lottery'

    def __init__(self):
        self.db = sqlite3.connect(LotteryHistory.DATABASE_NAME)
        self._create_main_table()

    def __del__(self):
        if self.db != None:
            self.db.close()

    def _create_main_table(self):
        # 大乐透和双色球的历史记录应该是差不多的
        sql = '''
        CREATE TABLE IF NOT EXISTS {table_name} (
        {}
        '''.format(table_name=LotteryHistory.SUPER_LOTTO_TABLE
            )
        self.db.execute(sql)
        self.db.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table_name} ({key_name});
        '''.format(index_name='', table_name=LotteryHistory.SUPER_LOTTO_TABLE, key_name=''))

    # 不用管是增量还是全量,总之有多少数据就更新多少数据
    def update_super_lotto(self, lotteries):
        pass

    def update_welfare_lottery(self, lotteries):
        pass