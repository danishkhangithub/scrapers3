# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import urllib
import os
import json
import datetime

# property scraper class
class ResidentialSale(scrapy.Spider):
    # scraper name
    name = 'therapists'
    base_url = 'https://www.globenewswire.com/NewsRoom'
    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }
    '''
    try:
       os.remove('abx.csv')
    except OSError:
       pass 
    '''
    file = 'data.csv'
    try:
      if(os.path.exists(file) and os.path.isfile(file)):
         os.remove(file)
         print('file deleted')
      else:      
         print('file not found')
    except OSError:
       pass 
    
         
    
    # general crawler
    def start_requests(self):
       
            # initial HTTP request
            yield scrapy.Request(
                url=self.base_url,
                headers=self.headers,
               
                callback=self.parse
                      )
    def parse(self, response):
       links = response.css('div[class="pagging-list-item-text-container"] a::attr(href)').getall()
       for link in links:
         if '?page=' not in link:
             link = 'https://www.globenewswire.com/' + link

       
             yield response.follow(
                 url = link ,
                 headers = self.headers,
                 callback = self.parse_cards
             )
             
    def parse_cards(self,response):
               
             
         '''
         with open('data.csv', 'a') as csv_file:
             writer = csv.DictWriter(csv_file, fieldnames=items.keys())
             writer.writerow(items)
         '''
 
 
if __name__ == '__main__':
    # run scraper
    process = CrawlerProcess()
    process.crawl(ResidentialSale)
    process.start()
    
    #ResidentialSale.parse(ResidentialSale, '')
    
