# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
import requests
import sqlite3
import re
from database.LotteryHistory import LotteryHistory
from lxml import etree
from lottery.entity import LotteryDraw, ColoredLotteryDraw
from lottery.SuperLotto import SuperLotto, SuperLottoDraw
from lottery.WelfareLottery import WelfareLotteryDraw, WelfareLottery

reload(sys)
sys.setdefaultencoding('utf-8')

#http://chart.lottery.gov.cn/chart_tc2/chart.shtml?LotID=23529&ChartID=15&_StatType=3&MinIssue=2007001&MaxIssue=2007200&IssueTop=100&ChartType=0&param=0&tab=15
# https://datachart.500.com/ssq/history/newinc/history.php?start=03000&end=17063
# 本项目核心不在爬虫,就懒得做一整套爬虫体系了啊嘻嘻
class Spider(object):
    def __init__(self):
        self.downloader = Downloader()
        self.collector = Collector()
        self.parser = Parser()
        self.url_manager = URLManager()

    def crawl(self, incremental=True):
        super_lotto_content = self.downloader.download(self.url_manager.super_lotto_url(incremental))
        if super_lotto_content != None and len(super_lotto_content) > 0:
            lotteries = self.parser.parse_superlotto(super_lotto_content)
            self.collector.update_super_lotto(lotteries)
        else:
            print 'download super lotto fail'
        welfare_lottery_content = self.downloader.download(self.url_manager.welfare_lottery_url(incremental))
        if welfare_lottery_content != None and len(welfare_lottery_content) > 0:
            lotteries = self.parser.parse_welfarelottery(welfare_lottery_content)
            self.collector.update_welfare_lottery(lotteries)
        else:
            print 'download welfare lottery fail'


class Parser(object):

    # 不比在意是全量还是增量,网页有多少就解析多少
    def parse_superlotto(self, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        items = html.xpath('//div[@class="result"]/table/tbody/tr')
        draws = []
        for item in items:
            tds = item.xpath('./td')
            # 这些td没标签,只能用顺序了
            draw = SuperLottoDraw()
            for (index, td) in enumerate(tds):
                if index == 0:
                    draw.serial = td.text
                elif index in range(1, SuperLotto.red_count()+1):
                    draw.red_balls.append(int(td.text))
                elif index in range(SuperLotto.red_count()+1, SuperLotto.red_count()+SuperLotto.blue_count()+1):
                    draw.blue_balls.append(int(td.text))
                elif index == len(tds)-3:
                    # 注意数字是以123,233,111的形式出现的
                    t = td.text
                    if t == '- -':
                        draw.sales = 0
                    else:
                        draw.sales = int(t.replace(',',''))
                elif index == len(tds)-2:
                    t = td.text
                    if t == '- -':
                        draw.pond = 0
                    else:
                        # 在谈几千万的生意呢,几毛钱滚草
                        draw.pond = int(float(t.replace(',', '')))
                elif index == len(tds)-1:
                    draw.l_date = td.text
            draws.append(draw)
        return draws

    def parse_welfarelottery(self, content):
        html = etree.HTML(content, parser=etree.HTMLParser(encoding='utf-8'))
        items = html.xpath('//tr[@class="t_tr1"]')
        draws = []
        for item in items:
            tds = item.xpath('./td')
            draw = WelfareLotteryDraw()
            for (index, td) in enumerate(tds):
                if index == 0:
                    draw.serial = td.text
                elif index in range(1, WelfareLottery.red_count()+1):
                    draw.red_balls.append(int(td.text))
                elif index in range(WelfareLottery.red_count()+1, WelfareLottery.red_count()+1+WelfareLottery.blue_count()):
                    draw.blue_balls.append(int(td.text))
                elif index == len(tds) - 7:
                    draw.pond = int(td.text.replace(',', ''))
                elif index == len(tds) - 2:
                    draw.sales = int(td.text.replace(',', ''))
                elif index == len(tds) - 1:
                    draw.l_date = td.text
            draws.append(draw)
        return draws



# collector只应该做数据的存储和记录,不做逻辑操作

class Collector(object):

    def __init__(self):
        self.db = sqlite3.connect(LotteryHistory.DATABASE_NAME)
        self._create_main_table()

    def __del__(self):
        if self.db != None:
            self.db.close()


    def _create_colored_table(self, table_name):
        # 大乐透和双色球的库其实差不多,也就是表名不同
        sql = '''
        CREATE TABLE IF NOT EXISTS {table_name} (
        {serial_no} TEXT PRIMARY KEY NOT NULL,
        {date} DATE NOT NULL,
        {sales} TEXT NOT NULL,
        {pond} NUMERIC NOT NULL,
        {reds} TEXT NOT NULL,
        {blues} TEXT NOT NULL
        );
        '''.format(table_name=table_name,\
                   serial_no=LotteryDraw.SERIAL_KEY,\
                   date=LotteryDraw.DATE_KEY,\
                   sales=LotteryDraw.SALES_KEY,\
                   pond=LotteryDraw.POND_KEY,\
                   reds=ColoredLotteryDraw.RED_BALLS_KEY, \
                   blues=ColoredLotteryDraw.BLUE_BALLS_KEY \
                   )
        self.db.execute(sql)
        self.db.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS {index_name} ON {table_name} ({key_name});
        '''.format(index_name='serial_key', table_name=table_name, key_name=LotteryDraw.SERIAL_KEY))


    def _create_main_table(self):
        self._create_colored_table(LotteryHistory.SUPER_LOTTO_TABLE)
        self._create_colored_table(LotteryHistory.WELFARE_LOTTERY_TABLE)


    # 不用管是增量还是全量,总之有多少数据就更新多少数据,反正有序号区分
    def update_super_lotto(self, lotteries):
        self._update_colored_lottery(LotteryHistory.SUPER_LOTTO_TABLE, lotteries)

    def update_welfare_lottery(self, lotteries):
        self._update_colored_lottery(LotteryHistory.WELFARE_LOTTERY_TABLE, lotteries)


    def _update_colored_lottery(self, table_name, lotteries):
        params = []
        for draw in lotteries:
            params.append((draw.serial, draw.l_date, draw.sales, draw.pond, ','.join(str(b) for b in draw.red_balls), ','.join(str(b) for b in draw.blue_balls)))
        self.db.executemany('INSERT OR REPLACE INTO {table_name} VALUES (?, ?, ?, ?, ?, ?)'.format(table_name=table_name), params)
        self.db.commit()


class Analysis(object):
    def __init__(self, db_name=''):
        def regexp(expr, item):
            reg = re.compile(expr)
            return reg.search(item) is not None

        self.db = sqlite3.connect(db_name)
        #关于正则函数是看这里的 http://stackoverflow.com/questions/5365451/problem-with-regexp-python-and-sqlite
        self.db.create_function("REGEXP", 2, regexp)

    def __del__( self ):
        if self.db != None:
            self.db.close()

    def raw_query(self, sql):
        return self.db.cursor().execute(sql)


class Downloader(object):

    def download(self, url, session=None, headers=None):
        if url is None:
            return None
        if session == None:
            response = requests.get(url, headers=headers)
            if response.status_code != requests.codes.ok:
                return None
            return response.text
        else:
            response = session.get(url, headers=headers)
            if response.status_code == requests.codes.ok or response.status_code == requests.codes.bad:
                return response.text
            else:
                return None


class URLManager(object):
    # 有些固定url就直接写死了,灵活的url用堆栈控制
    # 全量更新的时候虽然基础url是一个,但是和增量更新时间差距很大,还是区分一下
    # 就把增量更新获取最近的20条好了
    def super_lotto_url(self, incremental=True):
        url = 'http://www.lottery.gov.cn/historykj/history_2.jspx?page=false&_ltype=dlt'
        if not incremental:
            url += '&termNum=10000'
        return url

    def welfare_lottery_url(self, incremental=True):
        url = 'https://datachart.500.com/ssq/history/newinc/history.php'
        if not incremental:
            url += '?limit=10000'
        return url


    def __init__(self):
        self.finished_urls = set()
        self.feed_urls = set()
        self.failed_urls = set()

    #吃进来的是code
    def add_url(self, url):
        if url not in self.finished_urls and url not in self.feed_urls:
            self.feed_urls.add(url)

    def add_urls(self, urls):
        for url in urls:
            self.add_url(url)

    # 加可以批量加,但移除肯定是一个个移除的
    def finish_url(self, url):
        self.feed_urls.discard(url)
        self.finished_urls.add(url)

    def fail_url(self, url):
        self.failed_urls.add(url)

    def is_empyt(self):
        return len(self.feed_urls) == 0

    def is_overflow(self):
        return False

    def pop_url(self):
        return self.feed_urls.pop()

    def output_faileds(self):
        for url in self.failed_urls:
            print url

    def transfer_url(self):
        self.feed_urls = self.feed_urls.union(self.failed_urls)
        self.failed_urls.clear()


if __name__ == '__main__':
    s = Spider()
    # 开发阶段先全量吧
    s.crawl(False)
