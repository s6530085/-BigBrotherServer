# -*- coding: utf-8 -*-
__author__ = 'study_sun'

import sys
import requests
import sqlite3
import re
from database.LotteryHistory import *
from lxml import etree
from lottery.SuperLotto import SuperLotto

reload(sys)
sys.setdefaultencoding('utf-8')

SuperLottoInitYear = '2007'
WelfareLotteryInitYear = '2003'

#http://www.3dcp.cn/zs/gonggao.php?type=dlt&year=2007
#http://www.3dcp.cn/zs/gonggao.php?type=ssq&year=2009


#http://chart.lottery.gov.cn/chart_tc2/chart.shtml?LotID=23529&ChartID=15&_StatType=3&MinIssue=2007001&MaxIssue=2007200&IssueTop=100&ChartType=0&param=0&tab=15

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
        welfare_lottery_content = self.downloader.download(self.url_manager.welfare_lottery_url())
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
        lotteries = []
        for item in items:
            tds = item.xpath('./td')
            # 这些td没标签,只能用顺序了
            for (index, td) in enumerate(tds):
                lottery = SuperLotto()
                if index == 0:
                    pass
        return lotteries

    def parse_welfarelottery(self, content):
        pass

class Collector(LotteryHistory):
    pass

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
                #从雪球下载的时候,会有非200,但是并非下载失败的情况,这里特例一下
                return response.text
            else:
                return None

class URLManager(object):
    # 有些固定url就直接写死了,灵活的url用堆栈控制
    # 全量更新的时候虽然基础url是一个,但是和增量更新时间差距很大,还是区分一下
    def super_lotto_url(self, incremental=True):
        return ""

    def welfare_lottery_url(self, incremental=True):
        return ""


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
    s.crawl(True)
