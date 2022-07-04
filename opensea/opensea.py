# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import csv
import datetime
from scrapy.shell import inspect_response

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://opensea.io/rankings?sortBy=one_day_volume'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    file = 'amazon_list.csv'
    try:
       if (os.path.exists(file)) and (os.path.isfile(file)):
          os.remove(file)
       else:
          print('file not found')
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
                url=self.base_url,
                headers=self.headers,

                callback=self.parse
                      )
    def parse(self, res):
       print(response), self
       inspect_response(response)

#       yield response.follow(
#             url = ,
#             headers = self.headers,
#             callback =
#       )

        '''
        self.results.append(features)
        headers = features.keys()

        with open('amazon_list.csv', 'w+', newline = '') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter = ',', fieldnames = headers)
            writer.writeheader()
            writer.writerows(self.results)
        '''

if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()

    #ResidentialSale.parse(ResidentialSale, '')
