# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json
import codecs
import MySQLdb
import MySQLdb.cursors
import copy

from twisted.enterprise import adbapi


class OwMaxPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        '''        1 、@classmethod声明一个类方法，而对于平常我们见到的则叫做实例方法。
                   2、类方法的第一个参数cls（class的缩写，指这个类本身），而实例方法的第一个参数是self，表示该类的一个实例
                   3、可以通过类来调用，就像C.f()，相当于java中的静态方法'''
        dbparams = dict(
            host=settings['MYSQL_HOST'],  # 读取settings中的配置
            db=settings['MYSQL_NAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',  # 编码要加上，否则可能出现中文乱码问题
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=False,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbparams)       # **表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        return cls(dbpool)  # 相当于dbpool付给了这个类，self中可以得到

    def __init__(self, dbpool):
        self.dbpool = dbpool

    def process_item(self, item, spider):

        asynItem = copy.deepcopy(item)
        query = self.dbpool.runInteraction(self._insert_data, asynItem)
        query.addErrback(self._handle_error, item, spider)
        return item

    @staticmethod
    def _insert_data(tx, item):
        sql = "insert into data(userID,hero,gameTime,gameWinning,averageHitRate,averageCritRate,averageTime," \
              "averageDamage,averageKill,averageSingleKill,averageDefenseKill,averageLastKill,averageDead," \
              "averageTreatment,averageDamageDefense,bestHitRate,bestTime,bestDamage,bestKill,bestTreatment) " \
              "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
        params = (item['userID'], item["hero"], item["gameTime"], item["gameWinning"], item["averageHitRate"],
                  item["averageCritRate"], item["averageTime"], item["averageDamage"], item["averageKill"],
                  item["averageSingleKill"], item["averageDefenseKill"], item["averageLastKill"], item["averageDead"],
                  item["averageTreatment"], item["averageDamageDefense"], item["bestHitRate"],
                  item["bestTime"], item["bestDamage"], item["bestKill"], item["bestTreatment"])
        tx.execute(sql, params)

    # 错误处理方法
    @staticmethod
    def _handle_error(failue, item, spider):
        print failue

