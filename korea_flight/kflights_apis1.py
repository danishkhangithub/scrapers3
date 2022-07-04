# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import csv
import datetime

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    start_url = 'https://suvarnabhumi.airportthai.co.th/flight'
    base_url = 'https://apis.airportthai.co.th/'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    # payload
    payload = {
        "schedule_end": "2021-08-20 23:59:59",
        "schedule_start": "2021-08-20 10:51:00",
        "search": "",
        "site": "bkk",
        "type": "A"

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

    # general crawler
    def start_requests(self):

            # initial HTTP request
            yield scrapy.Request(
                url=self.start_url,
                #body = json.dumps(self.payload),
                headers=self.headers,
                #method = "POST",
                callback=self.parse
                      )
    def parse(self, res):
       print(res.status)

       yield res.follow(
             url = self.base_url,
             body = json.dumps(self.payload),
             method = "POST",
             headers = self.headers,
             callback = self.parse
       )
       '''
       with open('qsranks.csv', 'a') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=items.keys())
            writer.writerow(items)
       '''
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()

    #ResidentialSale.parse(ResidentialSale, '')
