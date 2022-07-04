# import packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import csv
import json
import os
from bs4 import BeautifulSoup
from multiprocessing import  Process

class Shopify(scrapy.Spider):
    name = 'shopify'

    base_url = 'https://www.shopistores.com/areas/11/'

    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    house = 0

    results = []

    file = 'shopify.csv'
    try:
       if (os.path.exists(file)) and (os.path.isfile(file)):
          os.remove(file)
       else:
          print('file not found')
    except OSError:
       pass
    # custom settings
    custom_settings = {
        #'FEED_FORMAT': 'csv',
        #'FEED_URI' : 'shopify.csv',
        'CONCURRENT_REQUEST_PER_DOMAIN': 6,
        'CONCURRENT_REQUESTS_PER_IP' : 6,
        'DOWNLOAD_DELAY': 1,
        'DOWNLOAD_TIMEOUT' : 10,
        'AUTO_THROTTLE' : False,


    }

    def start_requests(self):
      yield scrapy.Request(
             url = self.base_url,
             headers = self.headers,
             callback = self.parse_pagination
            )
    def parse_pagination(self, response):

        for page in range(0, 10):
            next_page = self.base_url + str(page)
            print('\nnext_page\n',next_page)

            yield response.follow(
                  url = next_page,
                  headers = self.headers,
                  callback = self.parse_listing
            )


    def parse_listing(self,response):

       content = ''

       with open('shopify.html', 'r') as f:
           for line in f.read():
               content += line

       response = Selector(text = content)


       for i in response.css('#content-container-tbl'):



           features = {
               'Name' :[j.get().strip() for j in i.css('td[data-title = "Store"]::text')]
,
               'Website' : i.css('table#content-container-tbl tbody tr td[data-title = "Store"] a::attr(href)').get().strip('https://nullrefer.com/?'),
               'Facebook' : '',
               'Twitter' : '',
               'Instagram' : '',
               'Pinterest' :'',
               'Snapchat' : '',
               'Youtube' : '',

           }

           try:
             facebook = response.css('.social_link:nth-child(1)::attr(href)').get()
             features['Facebook'] = facebook
           except:
             features['Facebook'] = 'None'

           try:
             twitter = response.css('.social_link:nth-child(2)::attr(href)').get()
             features['Twitter'] = twitter
           except:
             features['Twitter'] = 'None'

           try:
             instagram = response.css('.social_link:nth-child(3)::attr(href)').get()
             features['Instagram'] = instagram
           except:
             features['Instagram'] = 'None'

           try:
             pinterest = response.css('.social_link:nth-child(4)::attr(href)').get()
             features['Pinterest'] = pinterest
           except:
             features['Pinterest'] = 'None'

           try:
             snapchat = response.css('.social_link:nth-child(5)::attr(href)').get()
             features['Snapchat'] = snapchat
           except:
             features['Snapchat'] = 'None'

           try:
             youtube = response.css('.social_link:nth-child(6)::attr(href)').get()
             features['Snapchat'] = youtube
           except:
             features['Youtube'] = 'None'


           print(features)




#       #print(json.dumps(features, indent = 2))
#       self.results.append(features)
#       headers = features.keys()
#
#
#       with open('shopify.csv', 'w', newline='', encoding='utf-8') as csv_file:
#            writer = csv.DictWriter(csv_file, delimiter = ',',fieldnames = headers)
#            writer.writeheader()
#            writer.writerows(self.results)
#






# main driver
if __name__ == '__main__':
#  def crawl():
#       process = CrawlerProcess()
#       process.crawl(Shopify)
#       process.start()
        Shopify.parse_listing(Shopify, '')

#  process = Process(target=crawl)
#  process.start()
#  print(process)
