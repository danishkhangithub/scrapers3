# import packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import csv
import json
import os
from bs4 import BeautifulSoup
import requests
from multiprocessing import  Process

class Shopify(scrapy.Spider):
    name = 'shopify'

    base_url = 'https://www.sainsburys.co.uk/shop/gb/groceries/dietary-and-lifestyle/all-vegan-products#langId=44&storeId=10151&catalogId=10241&categoryId=462852&parent_category_rn=453878&top_category=453878&pageSize=60&orderBy=SEQUENCING%7CFAVOURITES_ONLY%7CTOP_SELLERS&searchTerm=&beginIndex=0&hideFilters=true'

    # headers
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
    }

    results = []

    file = 'vegan.csv'
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
             callback = self.parse_listing
             )

    def parse_listing(self,response):

       products = response.css('div[class = "productInfo"] a::attr(href)').getall()

       for link in products[:15]:
           yield response.follow(
                url = link,
                headers = self.headers,
                callback = self.parse_products
           )

    def parse_products(self, response):
        link = response.url.split('/product/')[1]
        #link = link.strip('/')
        print(link)

        url = "https://www.sainsburys.co.uk/groceries-api/gol-services/product/v1/product?filter[product_seo_url]=gb%2Fgroceries%2F"+ link  +"&include[ASSOCIATIONS]=true&include[PRODUCT_AD]=citrus"

        r = requests.get( url)

        data = r.json()

        data = data['products'][0]


        features = {
           'Name' : data['name'],
           'Retail_price' : data['retail_price']['price'],
           'Description' : data['description'],
           'Image' : data['image'],
           'Reviews' : data['reviews']['average_rating']
        }

        print('\n\nfeatures\n', features)


        self.results.append(features)
        headers = self.results[0].keys()

        with open('vegan.csv', 'w', newline='', encoding='utf-8') as csv_file:
             writer = csv.DictWriter(csv_file, delimiter = ',',fieldnames = headers)
             writer.writeheader()
             writer.writerows(self.results)









# main driver
if __name__ == '__main__':
       process = CrawlerProcess()
       process.crawl(Shopify)
       process.start()
       # Shopify.parse_products(Shopify, '')
