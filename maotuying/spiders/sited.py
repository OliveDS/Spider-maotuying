# -*- coding: utf-8 -*-
import scrapy
import pymysql
from maotuying.items import MaotuyingReviewItem

class SitedSpider(scrapy.Spider):
    name = 'sited'
    allowed_domains = ['www.tripadvisor.cn']
    # start_urls = ['http://www.tripadvisor.cn/']

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',# 允许爬取重复的页面 因为我的程序中对目的地首页先解析了pages页数,所以会重复一次!!否则爬第一页景点失败
        'ITEM_PIPELINES' : {'maotuying.pipelines.MaotuyingReviewPipeline': 300,}
    }

    def start_requests(self):
        # 从数据库中找到所有景点的URL
        self.connect = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'dsjk',
            password = 'dsjk',
            database = 'scrapy_sies',  
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)
        sql = "select site_url from sites_all_url_copy4"# table: sites_all_url_copy4
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        print(len(results)," sites total.")
        requests = []
        i = 0
        for url in results:
            # i += 1
            # print(url[0])
            request = scrapy.Request(url[0], callback=self.parse_sites_firstpage)#Request(url, callback=self.parse_review, meta={'movieId': movieId}, dont_filter=True)
            requests.append(request)
            # if i > 100:
            #     break
        return requests

    def parse_sites_firstpage(self, response):# 解析目的地的景点页数
        desurl = response.url
        # print(desurl) #https://www.tripadvisor.cn/Attraction_Review-g298557-d1801584-Reviews---Xiangzi_Temple-Xi_an_Shaanxi.html
        des_parts = desurl.split('-')
        try:
            pages = response.xpath('//div[@class="pageNumbers"]/a/@data-page-number').extract()# 页面中所有页码的数组
            # print("pages is",pages)
            page = int(pages[-1])
            # print("transfer pages to int",pages)
        except:
            page = 1;
        for i in range(page):
            url = des_parts[0] + '-' + des_parts[1] + '-' + des_parts[2] + '-' + des_parts[3] + '-or' + str(i*10) + '-' + des_parts[4] + '-' + des_parts[5]#+ '.html'
            ##print("this is i in range(pages)",i,url)
#             yield scrapy.Request(
#                 url,
#                 formname = language,
#                 formdata = {
#                     'language': 'ALL', # or any other year value
#                 }
#                 callback=self.parse_site_reviews
# )
            yield scrapy.Request(url, self.parse_site_reviews)


    def parse_site_reviews(self, response): # 解析目的地详情
        desurl = response.url
        # print(desurl) #https://www.tripadvisor.cn/Attraction_Review-g298557-d1801584-Reviews---Xiangzi_Temple-Xi_an_Shaanxi.html
        des_parts = desurl.split('-')

        review_quote = response.xpath('//span[@class="noQuotes"]').xpath('string(.)').extract()
        review_detail = response.xpath('//p[@class="partial_entry"]').xpath('string(.)').extract()
        review_user = response.xpath('//div[@class="info_text"]/div[1]').xpath('string(.)').extract()# div[1]表示提取其中的第一个div
        review_time = response.xpath('//span[@class="ratingDate"]/@title').extract()
        review_url = response.xpath('//div[@class="quote"]/a/@href').extract()    
        review_items = []
        # print("this is parse_site_reviews",desurl)
        for i in range(len(review_quote)):
            item = MaotuyingReviewItem()
            item['review_site'] = des_parts[-2]# 倒数第二为景点名称
            try:
                url_r = review_url[i]
            except:
                url_r = ""
            item['review_url'] = url_r
            item['review_quote'] = review_quote[i]
            item['review_detail'] = review_detail[i]
            item['review_user'] = review_user[i]
            item['review_time'] = review_time[i]
            review_items.append(item)
        return review_items# 必须return not pass 否则des_s中后续str不执行(for循环只执行一次)

