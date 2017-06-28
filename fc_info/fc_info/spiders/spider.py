# encoding=utf8
from fc_info.items import FcInfoItem
from selenium import webdriver
from lxml import html
import scrapy
import re
import redis
import pymysql
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class spider(scrapy.Spider):
    name = 'fc_info'
    start_urls = ['https://www.1688.com/?spm=a261j.8198142.0.0.uCYBJI']
    header = {
        # 'referer': 'https://page.1688.com/html/go/info2016.html?spm=b26110225.7247409.2001419.116.n48wVh',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Mobile Safari/537.36'
    }
    cookie = \
        {
            '_tmp_ck_0': '"8vvkE%2B29JoTz3tymhdO8vVZrqregbDIktyV%2B9VdutBP3RGEYqJmd8Tu%2BLkTvKjQcKAOQ3BjN2mDe%2BXhKsvbcEst1uZc8gv6lbGhOj6VEcYFYbrekHkFfFInVHSFhdjF7oNmj3GYpLS7q4Av86mIe2%2BALphqO66M52GrQVLbeIUU%2BuUFT5ZuRKxGiodeB0hM1dCK2HExbcABD9wU2UJj3zj53iNnrmW6GsD73W1oj8uoGDCSElz%2BbwlBRRFZ1hiMmhM2mZI33VsNDTCt%2Be0hkCL66cyydaJPt8vHKHcGcWCGHhH7%2FxBhS2Ro%2BSdoPt%2B6jhUwnabcqDbmlYDwrO%2FYPgG5ZsBKNwPG8"',
            'last_mid': 'b2b-317934331449c07', 'JSESSIONID': '8L789vtu1-IYaXJXesAZuSz2HON5-7qaRBJQ-dBAJ',
            'alicnweb': 'lastlogonid%3D%25E6%2598%2593%25E8%25AE%25AD%25E5%2590%2588%25E5%25BE%25B7%25E7%25A7%2591%25E6%258A%2580%7Ctouch_tb_at%3D1494480055513%7Ccmsboxflag%3D1%7Ccmsbox%3Dcmsbox',
            'ali_ab': '114.242.2.96.1493271431414.0',
            '__last_loginid__': '"%E6%98%93%E8%AE%AD%E5%90%88%E5%BE%B7%E7%A7%91%E6%8A%80"',
            'ali_apache_track': '"c_ms=2|c_mt=3|c_mid=b2b-317934331449c07|c_lid=%E6%98%93%E8%AE%AD%E5%90%88%E5%BE%B7%E7%A7%91%E6%8A%80"',
            '_csrf_token': '1494471344842', 'cna': 'UB5+ESZKRAICAXLyAmDgoR4B',
            'UM_distinctid': '15bade9c52444c-0fa833b717b14b-39687804-13c680-15bade9c525bf0',
            'isg': 'AtracVDIV8b5X9t4l0oVvJfdK4YkyV7lpcY5rORThm04V3qRzJuu9aClUZ22', '_cn_slid_': 'jthciuejve',
            'l': 'AvT0IpVzv83ixaki1WDp/EtJRLlmzRi3'}

    def __init__(self):
        try:
            self.db = pymysql.Connection(host="localhost", user="root", port=3310,
                                         passwd="d123456",
                                         db="crawler", charset="utf8")
            self.cursor = self.db.cursor()
            print "=============Connect to db successfully!==================="
        except:
            print "=============Fail to connect to db!==================="

    def parse(self, response):
        self.driver.get('http://ghepc.go.1688.com/page/index.htm')
        self.driver.add_cookie({
            'name': 'cookie',
            'value': self.cookie,
            'domain': '.1688.com',
            'path': '/'
        })
        self.driver.refresh()
        data = self.driver.page_source
        data = html.fromstring(data)
        item = FcInfoItem()
        name = data.xpath('//div[@class="info"]/div/p/text()')
        if name:
            item['name'] = name[0]
        else:
            item['name'] = ''
        medal = data.xpath('//li[@class="fx-tab-pane"]/img/@src')
        if medal:
            item['medal'] = medal[0]
        else:
            item['medal'] = ''
        is_authentication = data.xpath('//div[@class="name fd-clr"]/img/@title')
        if is_authentication:
            item['is_authentication'] = is_authentication[0]
        else:
            item['is_authentication'] = ''
        location = data.xpath('//ul[@class="fd-clr"]/li[2]/@title')
        if location:
            item['location'] = location[0]
        else:
            item['location'] = ''
        founding_time = data.xpath('//ul[@class="fd-clr"]/li[4]/text()')
        if founding_time:
            founding_time = founding_time[0]
            item['founding_time'] = re.findall(u'公司成立时间：(.*)', founding_time)[0]
        else:
            item['founding_time'] = ''
        inquiry_sheet = data.xpath('//ul[@class="list fd-clr"]/li[1]/span/text()')
        if inquiry_sheet:
            item['inquiry_sheet'] = inquiry_sheet[0] + u'条'
        else:
            item['inquiry_sheet'] = ''
        bidding = data.xpath('//ul[@class="list fd-clr"]/li[2]/span/text()')
        if bidding:
            item['bidding'] = bidding[0] + u'次'
        else:
            item['bidding'] = ''

        recruit_suppliers = data.xpath('//ul[@class="list fd-clr"]/li[3]/span/text()')
        if recruit_suppliers:
            item['recruit_suppliers'] = recruit_suppliers[0] + u'次'
        else:
            item['recruit_suppliers'] = ''

        purchase_amount = data.xpath('//ul[@class="list fd-clr"]/li[4]/span/text()')
        if purchase_amount:
            item['purchase_amount'] = purchase_amount[0] + u'万元'
        else:
            item['purchase_amount'] = ''

        purchase_frequency = data.xpath('//ul[@class="list fd-clr"]/li[5]/span/text()')
        if purchase_frequency:
            item['purchase_frequency'] = purchase_frequency[0] + u'次'
        else:
            item['purchase_frequency'] = ''
        introduce = data.xpath('//dl[@class="desc  desc-l last "]/dd/div/text()')
        if introduce:
            item['introduce'] = introduce[0]
        else:
            item['introduce'] = ''
        source_url = data.xpath('//div[@class="masthead-nav"]/ul/li[1]/a/@href')
        if source_url:
            item['source_url'] = source_url[0]
        else:
            item['source_url'] = ''
        purchase_url = data.xpath('//div[@class="masthead-nav"]/ul/li[2]/a/@href')
        if purchase_url:
            item['purchase_url'] = purchase_url[0]
        else:
            item['purchase_url'] = ''
        recruit_url = data.xpath('//div[@class="masthead-nav"]/ul/li[3]/a/@href')
        if recruit_url:
            item['recruit_url'] = recruit_url[0]
        else:
            item['recruit_url'] = ''
        company_info_url = data.xpath('//div[@class="masthead-nav"]/ul/li[4]/a/@href')
        if company_info_url:
            item['company_info_url'] = company_info_url[0]
        else:
            item['company_info_url'] = ''
        notice_url = data.xpath('//div[@class="masthead-nav"]/ul/li[4]/a/@href')
        if notice_url:
            item['notice_url'] = notice_url[0]
        else:
            item['notice_url'] = ''
        print item
        yield item









