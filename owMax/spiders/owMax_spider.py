# coding=utf-8
import json

import MySQLdb
import scrapy
from scrapy import Request
from owMax.items import OwMaxItem

class DmozSpider(scrapy.Spider):
    name = "owMax"
    # allowed_domains = ["dmoz.org"]
    userName = " "
    userID = 0
    custom_settings = {
        "DEFAULT_REQUEST_HEADERS": {
            'authority': 'ow.ali213.net',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'origin': 'http://ow.ali213.net/',
            'referer': 'http://ow.ali213.net/gamer/'+userName,
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest'
            # 'cookie': 'cna=/oN/DGwUYmYCATFN+mKOnP/h; tracknick=adimtxg; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; thw=cn; v=0; cookie2=1b2b42f305311a91800c25231d60f65b; t=1d8c593caba8306c5833e5c8c2815f29; _tb_token_=7e6377338dee7; CNZZDATA30064598=cnzz_eid%3D1220334357-1464871305-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464871305; CNZZDATA30063600=cnzz_eid%3D1139262023-1464874171-https%253A%252F%252Fmm.taobao.com%252F%26ntime%3D1464874171; JSESSIONID=8D5A3266F7A73C643C652F9F2DE1CED8; uc1=cookie14=UoWxNejwFlzlcw%3D%3D; l=Ahoatr-5ycJM6M9x2/4hzZdp6so-pZzm; mt=ci%3D-1_0'
        },
        "ITEM_PIPELINES": {
            'owMax.pipelines.OwMaxPipeline': 300
        }
    }

    def start_requests(self):

        conn = MySQLdb.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='123456',
            db='owmax',
            charset='utf8',           #编码要加上，否则可能出现中文乱码问题
        )
        cursor = conn.cursor()
        cursor.execute("select * from user where state = 0")
        user = cursor.fetchall()[0]
        print("userID: "+str(user[0]))
        print("userName: "+user[1])
        self.userID = user[0]
        self.userName = user[1]
        cursor.close()
        conn.close()

        url = "http://ow.ali213.net/getdata.php?playerName="+self.userName
        requests = []
        request = Request(url=url, callback=self.parse_model)
        requests.append(request)
        return requests

    def parse_model(self, response):
        jsonBody = json.loads(response.body.decode("gbk").encode("utf-8"))
        models = jsonBody['statsSectionMap']
        for i in models:
            modelItem = OwMaxItem()
            modelItem['userID'] = int(self.userID)
            modelItem['hero'] = models[i]['selectName']

            # 用于判断英雄有没有数据项
            if u'战斗' in models[i]['statsSectionMap'] and u'平均' in models[i]['statsSectionMap'] and  u'游戏' \
                    in models[i]['statsSectionMap'] and u'最佳' in models[i]['statsSectionMap']:
                # 战斗
                if u'命中率' in models[i]['statsSectionMap'][u"战斗"]:
                    modelItem['averageHitRate'] = models[i]['statsSectionMap'][u"战斗"][u'命中率']
                else:
                    modelItem['averageHitRate'] = 'NULL'
                if u'爆击精准度' in models[i]['statsSectionMap'][u"战斗"]:
                    modelItem['averageCritRate'] = models[i]['statsSectionMap'][u"战斗"][u'爆击精准度']
                else:
                    modelItem['averageCritRate'] = 'NULL'
                # modelItem['averageDeadAfterKill'] = models[i]['statsSectionMap'][u"战斗"][u'死前平均击杀数']

                # 平均
                modelItem['averageDamage'] = models[i]['statsSectionMap'][u'平均'][u'平均伤害量']
                modelItem['averageKill'] = models[i]['statsSectionMap'][u'平均'][u'平均击杀数']
                modelItem['averageSingleKill'] = models[i]['statsSectionMap'][u'平均'][u'平均单人击杀数']
                modelItem['averageDefenseKill'] = models[i]['statsSectionMap'][u'平均'][u'平均攻防击杀']
                modelItem['averageLastKill'] = models[i]['statsSectionMap'][u'平均'][u'平均最后一击数']
                modelItem['averageDead'] = models[i]['statsSectionMap'][u'平均'][u'平均死亡数']
                modelItem['averageTime'] = models[i]['statsSectionMap'][u"平均"][u'平均目标攻防时间']
                if u'平均治疗量' in models[i]['statsSectionMap'][u"平均"]:
                    modelItem['averageTreatment'] = models[i]['statsSectionMap'][u"平均"][u'平均治疗量']
                else:
                    modelItem['averageTreatment'] = 'NULL'

                # 游戏
                modelItem['gameTime'] = models[i]['statsSectionMap'][u'游戏'][u'对战次数']
                modelItem['gameWinning'] = models[i]['statsSectionMap'][u'游戏'][u'胜场']

                # 英雄特定
                if modelItem['hero'] != "所有英雄":
                    if u'平均伤害吸收量' in models[i]['statsSectionMap'][u"英雄特定"]:
                        modelItem['averageDamageDefense'] = models[i]['statsSectionMap'][u"英雄特定"][u'平均伤害吸收量']
                    else:
                        modelItem['averageDamageDefense'] = 'NULL'
                else:
                    modelItem['averageDamageDefense'] = 'NULL'

                # 最佳
                if u'单场最佳命中率' in models[i]['statsSectionMap'][u"最佳"]:
                    modelItem['bestHitRate'] = models[i]['statsSectionMap'][u"最佳"][u'单场最佳命中率']
                else:
                    modelItem['bestHitRate'] = 'NULL'
                modelItem['bestTime'] = models[i]['statsSectionMap'][u'最佳'][u'单场最长目标攻防时间']
                modelItem['bestDamage'] = models[i]['statsSectionMap'][u'最佳'][u'单场最高伤害量']
                modelItem['bestKill'] = models[i]['statsSectionMap'][u'最佳'][u'单场最高击杀数']
                if u'单场最高治疗量' in models[i]['statsSectionMap'][u"最佳"]:
                    modelItem['bestTreatment'] = models[i]['statsSectionMap'][u"最佳"][u'单场最高治疗量']
                else:
                    modelItem['bestTreatment'] = 'NULL'
                yield modelItem
            else:
                print modelItem['hero']+'没有找到数据'