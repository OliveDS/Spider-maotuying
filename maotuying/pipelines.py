# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''
class MaotuyingPipeline(object):
    def process_item(self, item, spider):
        with open("sites.txt",'a') as fp:
        	fp.write( item['site_url'] + '\n') # item['site_name'].encode("utf8") + ' ' +
        	# return item
'''
import pymysql

class MaotuyingPipeline(object):
    
    siteInsert = '''insert into sites_all_url_copy4(site_name,site_url) values ('{site_name}','{site_url}')'''

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        sqlinsert = self.siteInsert.format(
        	site_name = pymysql.escape_string(item['site_name']),
        	site_url = pymysql.escape_string(item['site_url'])
        	)

        self.cursor.execute(sqlinsert)
        return item
        # print("this is item in pipeline process_item")
        # session = self.Session()
        # sitesdb = SitesDB()
        # print("this is sitesdb in pipeline process_item")
        # sitesdb.site_name = item["site_name"]
        # sitesdb.site_url = item["site_url"]

        # try:
        #     session.add(sitesdb)
        #     session.commit()
        # except:
        #     session.rollback()
        #     raise
        # finally:
        #     session.close()

        # return item


    def open_spider(self, spider):
        self.connect = pymysql.connect(
        	host = '47.93.238.102',
	        port = 3306,
	        user = 'dsjk',
	        password = 'dsjk',
	        database = 'scrapy_sies',  
	        charset='utf8',
	        use_unicode=True)
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()

class MaotuyingReviewPipeline(object):
    
    reviewInsert = '''insert into sites_all_review_copy2(review_site,review_url,review_quote,review_detail,review_user,review_time) values ('{review_site}','{review_url}','{review_quote}','{review_detail}','{review_user}','{review_time}')'''

    def process_item(self, item, spider):
        """Save deals in the database.

        This method is called for every item pipeline component.
        """
        sqlinsert = self.reviewInsert.format(
            # site_name = pymysql.escape_string(item['site_name']),
            # site_url = pymysql.escape_string(item['site_url'])
            review_site = pymysql.escape_string(item['review_site']),
            review_url = pymysql.escape_string(item['review_url']),
            review_quote = pymysql.escape_string(item['review_quote']),
            review_detail = pymysql.escape_string(item['review_detail']),
            review_user = pymysql.escape_string(item['review_user']),
            review_time = pymysql.escape_string(item['review_time']),
            )

        self.cursor.execute(sqlinsert)
        return item
      


    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host = '47.93.238.102',
            port = 3306,
            user = 'dsjk',
            password = 'dsjk',
            database = 'scrapy_sies',  
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()