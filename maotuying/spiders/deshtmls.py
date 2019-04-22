# -*- coding: utf-8 -*-
import scrapy


class DeshtmlsSpider(scrapy.Spider):
    name = 'deshtmls'
    allowed_domains = ['www.tripadvisor.cn']
    start_urls = ['https://www.tripadvisor.cn/Tourism-g294211-China-Vacations.html']

    custom_settings = {
        "ITEM_PIPELINES": {
            'maotuying.pipelines.MoviePipeline': 300
        },
        "DEFAULT_REQUEST_HEADERS": {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate',
            'accept-language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'referer': 'https://mm.taobao.com/search_tstar_model.htm?spm=719.1001036.1998606017.2.KDdsmP',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        },
        "ROBOTSTXT_OBEY": False  # 需要忽略ROBOTS.TXT文件 #也可以在setting.py中直接设置
    }

    def start_requests(self):
        url = '''https://www.tripadvisor.cn/TourismChildrenAjax?geo=294211&offset={offset}&desktop=true'''
        requests = []
        for i in range(2):
            request = Request(url.format(offset=i), callback=self.parse_htmls)
            requests.append(request)
        #return requests

    def parse_des_htmls(self, response):
        des_s = response.xpath('//div[@class="popularCities"]/a')
        for des in des_s:
            print(des.xpath('@href').extract()[0])

    def parse_sites(self, response):
        des_s = response.xpath('//div[@class="popularCities"]/a')
        for des in des_s:
            print(des.xpath('@href').extract()[0])
        #print(response.body.decode())
        jsonBody = json.loads(response.body.decode())
        subjects = jsonBody['data']
        movieItems = []
        for subject in subjects:
            item = MovieItem()
            item['id'] = int(subject['id'])
            item['title'] = subject['title']
            item['rating'] = float(subject['rate'])
            item['alt'] = subject['url']
            item['image'] = subject['cover']
            movieItems.append(item)
        return movieItems


    def parse_sites_pages(self, response):# 解析目的地的景点页数
        # url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-oa' + str(i*30) + '-' + des_parts[2] + '.html'
        desurl = response.xpath('//li[@data-element=".masthead-dropdown-attractions"]/a/@href').extract()# 页面中所有页码的数组
        # e.g. /Attractions-g294217-Activities-Hong_Kong.html
        print(desurl[0])
        des_parts = desurl[0].split('-')
        # https://www.tripadvisor.cn/Attractions-g294217-Activities-Hong_Kong.html
        # url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-' + des_parts[3] #+ '.html'
        # print("only parse page 1",url)
        # yield scrapy.Request(url, self.parse_sites_1page)

        try:
            page_s = response.xpath('//div[@class="pageNumbers"]/a/@data-page-number').extract()# 页面中所有页码的数组
            pages = int(page_s[-1])# 最后一个页码就是最大页码
        except:
            pages = 1;
        # if pages < 1:
        #     pages = 1;
        print("this is parse_sites_pages",pages)
        # i = 0
        for i in range(pages):
            # print("this is i in range(pages)",i)
            if i ==0 :
                url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-' + des_parts[3] #+ '#FILTERED_LIST'
                print("this is i in range(pages)",i,url)
                yield scrapy.Request(url, self.parse_sites_1page)
            else:
                url = 'https://www.tripadvisor.cn/Attractions-' + des_parts[1] + '-Activities-oa' + str(i*30) + '-' + des_parts[3] #+ '.html'
                print("this is i in range(pages)",i,url)
                # i += 1
                yield scrapy.Request(url, self.parse_sites_1page)

