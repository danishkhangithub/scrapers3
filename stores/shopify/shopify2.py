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

    base_url = 'https://www.sainsburys.co.uk/webapp/wcs/stores/servlet/gb/groceries?storeId=10151&langId=44&krypto=WXcJrfvVDvc646jmpQQ0tsEARbbeRyYsuH84a3kf2ElMC8A0W1yhSKNyqGF6Jgq4JMyaVNAO2arPsIHca2ptAX7NuqZPc7cj9RnTTpiqVtvnEDlhCiH5iV8jm%2B0vqo1I&ddkey=https%3Agb%2Fgroceries'

    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    results = []

    file = 'stores.csv'
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
        'DOWNLOAD_DELAY': 3,
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

        for page in range(0, 161):
            next_page = self.base_url + str(page)
            print('\nnext_page\n',next_page)

            self.page +=1

            yield response.follow(
                  url = next_page,
                  headers = self.headers,
                  meta = {'page': self.page},
                  callback = self.parse_listing
            )


    def parse_listing(self,response):

       page_no = response.meta.get('page')
       '''
       content = ''

       with open('shopify.html', 'r') as f:
           for line in f.read():
               content += line

       response = Selector(text = content)
       '''

       for i in response.css('.text-muted+ .col-md-12 table#content-container-tbl tbody tr'):



           features = {
               'Rank' : i.css('td[data-title = "Rank"]::text').get(),
               'Name' :i.css('td[data-title = "Store"]::text').get().strip(),
               'Country' : i.css('td[data-title = "Area"] a::attr(title)').get(),
               'Website' : '',
               'Facebook' : '',
               'Twitter' : '',
               'Instagram' : '',
               'Pinterest' :'',
               'Snapchat' : '',
               'Youtube' : '',
               'Alexa' : i.css('td[data-title = "Alexa Rank"]::text').get().strip(),
               'Growing' : i.css('td[data-title = "Growing"] span::text').get().strip(),

           }

           try:
             website = i.css('td[data-title = "Store"] a::attr(href)').get()
             website = website.split('?')[1]
             features['Website'] = website
           except:
             features['website'] = 'N/a'

           try:
             facebook = i.css('td[data-title = "Social"] .social_link:nth-child(1)::attr(href)').get()
             features['Facebook'] = facebook
           except:
             features['Facebook'] = 'None'


           try:
             twitter = i.css('td[data-title = "Social"] .social_link:nth-child(2)::attr(href)').get()
             features['Twitter'] = twitter
           except:
             features['Twitter'] = 'None'


           try:
             instagram = i.css('td[data-title = "Social"] .social_link:nth-child(3)::attr(href)').get()
             features['Instagram'] = instagram
           except:
             features['Instagram'] = 'None'


           try:
             pinterest = i.css('td[data-title = "Social"] .social_link:nth-child(4)::attr(href)').get()
             features['Pinterest'] = pinterest
           except:
             features['Pinterest'] = 'None'

           try:
             snapchat = i.css('td[data-title = "Social"] .social_link:nth-child(5)::attr(href)').get()
             features['Snapchat'] = snapchat
           except:
             features['Snapchat'] = 'None'

           try:
             youtube = i.css('td[data-title = "Social"] .social_link:nth-child(6)::attr(href)').get()
             features['Youtube'] = youtube
           except:
             features['Youtube'] = 'None'


           self.results.append(features)
           headers = features.keys()

       with open('shopify.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, delimiter = ',',fieldnames = headers)
            writer.writeheader()
            writer.writerows(self.results)

       print('\n Page No %s is scraped' % page_no)







# main driver
if __name__ == '__main__':
       process = CrawlerProcess()
       process.crawl(Shopify)
       process.start()
       #Shopify.parse_listing(Shopify, '')
