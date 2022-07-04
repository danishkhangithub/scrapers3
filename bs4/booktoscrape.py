# import libraries
import requests
from bs4 import BeautifulSoup
import csv

# main class
class Booktoscrape:
   url = 'https://books.toscrape.com/'

   results = []

   def fetch(self, url):
       response = requests.get(url)
       print('HTTP Request to Url %s' % url)
       print('Status Code : %s' % response.status_code)

       return response

   def parse(self, response):

       content = BeautifulSoup(response, 'lxml')

       title = [title.find('a')['title'] for title in content.findAll('h3')]
       price = [price.find('p').text.strip('Â') for price in content.findAll('div', {'class': 'product_price'})]
       stock_availability = [stock.text.strip() for stock in content.findAll('p',{'class' : 'instock availability'})]

       for index in range(0, len(title)):
           self.results.append({
             'Title' : title[index],
             'Price' : price[index],
             'Stock_availablity' : stock_availability[index]
           })


   def to_csv(self):
     with open('books.csv', 'w+', newline = '') as csv_file:
         writer  = csv.DictWriter(csv_file, fieldnames = self.results[0].keys())

         for row in self.results:
             writer.writerow(row)
     print('Stores Data To Csv File')
   def run(self):
       for page in range(1, 10):
           url = self.url + 'catalogue/page-' + str(page)+ '.html'
           response = self.fetch(url)
           self.parse(response.text)

       self.to_csv()


# initialized the main driver
if __name__ == '__main__':
   scraper = Booktoscrape()
   scraper.run()