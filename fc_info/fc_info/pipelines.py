# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql


class FcInfoPipeline(object):
    def __init__(self):
        try:
            self.db = pymysql.Connection(host="localhost", user="root", port=3310,
                                         passwd="d123456",
                                         db="crawler", charset="utf8")
            self.cursor = self.db.cursor()
            print "=============Connect to db successfully!==================="
        except:
            print "=============Fail to connect to db!==================="

    def process_item(self, item, spider):
        if item:
            sql = 'update albaba_enterprise set name="%s",location="%s",founding_time="%s",inquiry_sheet="%s",bidding="%s",recruit_suppliers="%s",purchase_amount="%s",purchase_frequency="%s",introduce="%s" where source_url="%s"' % (item['name'],item['location'],item['founding_time'],item['inquiry_sheet'],item['bidding'],item['recruit_suppliers'],item['purchase_amount'],item['purchase_frequency'],item['introduce'],item['source_url'])
            self.cursor.execute(sql)
            self.db.commit()
            return item

    def close_spider(self, spider):
        self.db.commit()
        self.db.close()