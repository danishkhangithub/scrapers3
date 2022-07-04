import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerProcess
from scrapy.http import FormRequest
import csv
import json

# init class
class Mysql(scrapy.Spider):
    # scraper name
    name = "mysql_scraper"
    start_urls = ['https://www.mysqltutorial.org/tryit/']
    api_url = 'https://www.mysqltutorial.org/tryit/json.php'

    payloads = {
        'command' : 'SELECT * FROM customers;'
    }

    headers = {
       'user-agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
       'x-requested-with' : 'XMLHttpRequest'
       }

    custom_settings = {'HTTPERROR_ALLOW_ALL': True}

    # general crawler
    def parse(self,response):

            # initial HTTP request
            yield scrapy.FormRequest(
                url=self.api_url,
                method = "POST",
                formdata = self.payloads,
                headers=self.headers,
                callback=self.parse2
                      )
    def parse2(self, res):

       data = json.loads(res.text)
       #print(json.dumps(data, indent = 2))

       for i in data:
           print(i['columns'])
       '''
       content = ''

       with open('mysql_live_customers.html', 'r') as html:
            for line in html.read():
                content += line

       response = Selector(text = content)
       print(response)

       '''
       '''
       yield response.follow(
             url = ,
             headers = self.headers,
             callback =
       )

       with open('qsranks.csv', 'a') as csv_file:
             writer = csv.DictWriter(csv_file, fieldnames=items.keys())
             writer.writerow(items)
       '''





if __name__ == '__main__':
   process = CrawlerProcess()
   process.crawl(Mysql)
   process.start()
   #Mysql.parse(Mysql, '')