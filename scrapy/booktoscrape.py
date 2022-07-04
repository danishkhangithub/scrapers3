# import libraries
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector
import csv

class Booktoscrape(scrapy.Spider):
    name = "booktoscrape"

# initialized the main driver
if __name__ == '__mian__':
   scraper = CrawlerProcess()
   scraper.craw(Booktoscrape)
   scraper.start()