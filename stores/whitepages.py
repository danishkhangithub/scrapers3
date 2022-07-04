# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
from scrapy.http import FormRequest
import urllib
import os
import json
import csv
import datetime

# property scraper class
class Hotels(scrapy.Spider):
    # scraper name
    name = 'therapists'
    #start_url = 'https://www.priceline.com/relax/at/478502/from/20220523/to/20220527/rooms/1/adults/2?vrid=2af9fb11ff31fc1a4170ac6a891116da'
    base_url = 'https://www.whitepages.com.au/residential'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    custom_settings = {
       'CONCURRENT_REQUEST_PER_DOMAIN': 6,
       'CONCURRENT_REQUESTS_PER_IP' : 6,
       'DOWNLOAD_DELAY': 10,
       'DOWNLOAD_TIMEOUT' : 10,
       'AUTO_THROTTLE' : False,
        # enable the middleware
       'DOWNLOADER_MIDDLEWARES': {'scrapy_crawlera.CrawleraMiddleware': 610},

        # enable crawlera
        'CRAWLERA_ENABLED': True,

        # the APIkey you get with your subscription
        'CRAWLERA_APIKEY': '89d13c9b2dd6414aafd11e7952b0769b',

        'CRAWLERA_URL'      : 'http://123compareme.crawlera.com:8010',
        'ROBOTSTXT_OBEY' : 'False'

    }


    try:
       os.remove('abx.csv')
    except OSError:
       pass
    # custom settings
    custom_settings = {
        'CONCURRENT_REQUEST_PER_DOMAIN': 2,
        'DOWNLOAD_DELAY': 1
    }

    urls = []

    results = []

    urls_id = []

    # general crawler
    def start_requests(self):

                  yield scrapy.Request(
                      url = self.base_url,
                      headers = self.headers,
                      callback = self.parse,
                      dont_filter = True
                      )

    def parse(self, response):
       print(response.status)


#       # store all the scraped data into csv file
#       with open('hotels.csv', 'w+', newline = '') as csv_file:
#            writer = csv.DictWriter(csv_file, fieldnames = header)
#            writer.writeheader()
#            writer.writerows(self.results)



if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(Hotels)
    process.start()

    #Hotels.parse(Hotels.parse, '')
