# packages
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import json

# hummart spider class
class Darazspider(scrapy.Spider):
    # scraper / spider name
    name = 'daraz_spider'

    base_url =  'https://www.daraz.pk/smartphones/?spm=a2a0e.home.cate_1.1.6a2749373U3osu'

    headers = {
      'USER-AGENT' :  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
                    }

    results = []

    # custom settings
    custom_settings = {
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'DOWNLOAD_DELAY': 2
       }

    def __init__(self):
       self.resuts = []


    # crawler's entry point
    def start_requests(self):
        # make HTTP request to base URL
        yield scrapy.Request(
            url=self.base_url,
            headers=self.headers,
            callback=self.parse
        )

    def parse(self,response):
        '''
        content = ''

        with open('daraz.html', 'r') as html:
             for line in html.read():
                 content += line
        response = Selector(text = content)
        '''

        products = ''.join([script for script in response.css('script::text').getall() if 'window.pageData={"mods":' in script])
        products = json.loads(products.split('window.pageData=')[-1].replace(' ',''))
        products = products['mods']['listItems']

        producturls = [prod['productUrl'] for prod in products]

        for url in producturls:
            yield response.follow(
                 url = url,
                 headers = self.headers,
                 callback = self.parse_cards
            )
            break
    def parse_cards(self, response):

        content = ''

        with open('daraz3.html', 'r') as html:
             for line in html.read():
                 content += line
        response = Selector(text = content)

        data = response.css('script[type = "text"]').getall()
        print(data)



#        features = {
#            #'Product Url' : response.url,
#            'Name' : response.css('div[class= "pdp-product-title"] span::text').get(),
#            'Price' : response.css('div[class= "pdp-product-price"] span::text').get(),
#            'Rating' : response.css('div[class= "score"] span::text').get(),
#            #'Reviews' : response.css('div[class= "pdp-review-summary"] a::text').get().strip(' Ratings')
#
#        }
#        print(features)
#        self.results.append(features)
#        print(self.results)

#        with open('smartphones.csv','w') as csv_file:
#             writer  = csv.
#



if __name__ == '__main__':
    # run scraper
#    process = CrawlerProcess()
#    process.crawl(Darazspider)
#    process.start()
    Darazspider.parse_cards(Darazspider,'')
