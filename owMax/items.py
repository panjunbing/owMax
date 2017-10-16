# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class OwMaxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    userName = scrapy.Field()                                   #用户名
    userID = scrapy.Field()                                     #用户ID
    hero = scrapy.Field()                                       #英雄

    averageKill = scrapy.Field()                                #平均击杀数
    averageTime = scrapy.Field()                                #平均攻防时间
    averageDamage = scrapy.Field()                              #平均伤害数
    averageSingleKill = scrapy.Field()                          #平均单杀数
    averageDefenseKill = scrapy.Field()                         #平均攻防击杀
    averageLastKill = scrapy.Field()                            #平均最后一击数
    averageDead = scrapy.Field()                                #平均死亡数
    averageDeadAfterKill = scrapy.Field()                       #平均死前击杀数
    averageCritRate = scrapy.Field()                            #平均暴击率
    averageHitRate = scrapy.Field()                             #平均命中率
    averageDamageDefense = scrapy.Field()                       #平均伤害吸收量
    averageTreatment = scrapy.Field()                           #平均治疗量

    gameTime = scrapy.Field()                                   #游戏场次
    gameWinning = scrapy.Field()                                #胜场

    bestKill = scrapy.Field()                                   #最佳击杀数
    bestDamage = scrapy.Field()                                 #最佳伤害数
    bestTime = scrapy.Field()                                   #最佳攻防时间
    bestHitRate = scrapy.Field()                                #最佳命中率
    bestTreatment = scrapy.Field()                              #最佳治疗量

    pass
