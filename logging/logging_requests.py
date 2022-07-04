from datetime import date
from requests_html import HTMLSession
import logging


s = HTMLSession()

headers = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}

today = date.today()

date_save = today.strftime("%Y-%m-%d")

logging.basicConfig(filename = 'scraper.log' , level = logging.DEBUG,
                    format = '%(asctime)s - %(message)s', datefmt = '%d-%m-%y %H:%M:%S')

def Amazon(s, headers, date, asin):
   link = 'https://www.amazon.co.uk/dp/{asin}'

   r = s.get(link, headers = headers)
   print(r.status_code)
   product = (
     date,
     'Amazon',
     r.html.xpath('//*[@id="productTitle"]/text()', first = True),
     #r.html.find('span#priceblock_ourprice', first = True).text or 'N/A',
     link
   )

   print(product)

   return product

asins = ['B08XMPGL7Q', 'B00IE9XHE0','B07X78SMWP', 'B08J2K9VS7']

for  asin in asins:
     Amazon(s, headers, date_save, asin)
