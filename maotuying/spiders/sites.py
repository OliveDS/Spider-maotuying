# -*- coding: utf-8 -*-
import scrapy
from maotuying.items import MaotuyingItem

class SitesSpider(scrapy.Spider):
    name = 'sites'
    allowed_domains = ['www.tripadvisor.cn']
    # start_urls = ['http://www.tripadvisor.cn/']
    '''
    两层爬虫,先爬取所有目的地的URL,再在改URL下爬取所有景点
    parse先将目的地html解析出来,然后调用parse_sites
    parse_des 将目的地的中的所有景点URL爬取下来
    parse_sites 将每个景点的具体内容爬取并存储下来
    '''
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',# 允许爬取重复的页面 因为我的程序中对目的地首页先解析了pages页数,所以会重复一次!!否则爬第一页景点失败
        'ITEM_PIPELINES' : {'maotuying.pipelines.MaotuyingPipeline': 300,}
    }

    # 通常情况下给出 start_urls 即可开始爬虫,但此处需要构造,专门设置一个函数确定需要被爬取的URL,存到requests中,逐个被请求
    def start_requests(self):
        requests = []
        url = '''https://www.tripadvisor.cn/TourismChildrenAjax?geo=294211&offset={offset}&desktop=true'''
        for i in range(212):# 通过尝试,发现共0~211页 也可以while循环直到没有新的目的地
            request = scrapy.Request(url.format(offset=i), callback=self.parse_des)
            # print(request)
            # print("start_requests",i)
            requests.append(request)
        return requests

    def parse_des(self, response): # 解析目的地链接
        des_s = response.xpath('//a/@href').extract()# 页面中所有a的数组,即所有目的地
        print("this is parse_des")
        for des in des_s:
            des_parts = des.split('-') # e.g. /Tourism-g298559-Hangzhou_Zhejiang-Vacations.html
            print(des_parts[2])
            # https://www.tripadvisor.cn/Attractions-g298559-Activities-Hangzhou_Zhejiang.html
            url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-' + des_parts[2] + '.html'
            print("parse_des",url)
            yield scrapy.Request(url, self.parse_sites_firstpage)

    def parse_sites_firstpage(self, response):# 解析目的地的景点页数
        # url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-oa' + str(i*30) + '-' + des_parts[2] + '.html'
        desurl = response.xpath('//li[@data-element=".masthead-dropdown-attractions"]/a/@href').extract()# 页面中所有页码的数组
        # desurl = response.url
        # e.g. /Attractions-g294217-Activities-Hong_Kong.html
        print(desurl[0])
        des_parts = desurl[0].split('-')
        # https://www.tripadvisor.cn/Attractions-g294217-Activities-Hong_Kong.html
        # url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-' + des_parts[3] #+ '.html'
        # print("only parse page 1",url)
        try:
            page_s = response.xpath('//div[@class="pageNumbers"]/a/@data-page-number').extract()# 页面中所有页码的数组
            pages = int(page_s[-1])# 最后一个页码就是最大页码
        except:
            pages = 1;
        print("this is parse_sites_pages") #,pages
        for i in range(pages):
            # print("this is i in range(pages)",i)
            url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-oa' + str(i*30) + '-' + des_parts[3] #+ '.html'
            print("this is i in range(pages)",i,url)
            yield scrapy.Request(url, self.parse_sites_1page)

        '''site_s = response.xpath('//div[@class="listing_title "]/a/@href').extract()# 页面中所有a的数组
        sites_items = []
        print("this is parse_sites_1page",site_s)
        for site in site_s:
            # for example: /Attraction_Review-g298559-d386917-Reviews-West_Lake_Xi_Hu-Hangzhou_Zhejiang.html
            # /Attraction_Review-g297431-d501536-Reviews-Cangyan_Mountain-Shijiazhuang_Hebei.html
            site_parts = site.split('-')
            # if url is not None:
            url = 'https://www.tripadvisor.cn' + site
            print(site_parts[4],url)

            # 实现数据库pipeline读写
            item = MaotuyingItem()
            item['site_name'] = site_parts[4]
            item['site_url'] = url
            # TypeError: can only concatenate str (not "MaotuyingItem") to str
            # print("this is parse_sites's item" + item['site_url']) # 检查item是否成功生成
            sites_items.append(item)
            # yield scrapy.Request(url, self.parse_site)

        return sites_items# 必须return not pass 否则des_s中后续str不执行(for循环只执行一次)
        '''

    
    def parse_sites_1page(self, response):
        site_s = response.xpath('//div[@class="listing_title "]/a/@href').extract()# 页面中所有a的数组
        sites_items = []
        print("this is parse_sites_1page",site_s)
        for site in site_s:
            # for example: /Attraction_Review-g298559-d386917-Reviews-West_Lake_Xi_Hu-Hangzhou_Zhejiang.html
            # /Attraction_Review-g297431-d501536-Reviews-Cangyan_Mountain-Shijiazhuang_Hebei.html
            site_parts = site.split('-')
            # if url is not None:
            url = 'https://www.tripadvisor.cn' + site
            print(site_parts[4],url)

            # 实现数据库pipeline读写
            item = MaotuyingItem()
            item['site_name'] = site_parts[4]
            item['site_url'] = url
            # TypeError: can only concatenate str (not "MaotuyingItem") to str
            # print("this is parse_sites's item" + item['site_url']) # 检查item是否成功生成
            sites_items.append(item)
            # yield scrapy.Request(url, self.parse_site)
        return sites_items# 必须return not pass 否则des_s中后续str不执行(for循环只执行一次)

            