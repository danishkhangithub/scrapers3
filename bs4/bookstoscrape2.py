# import packages
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

# main class
class Booktoscrape:

    url = 'https://books.toscrape.com/'

    results = []

    def fetch(self, url):
        response = requests.get(url)
        print('HTTP GET Reqest to url: %s' % response, end = '')
        print(' | Status Code', response.status_code)

        return response

    def parse(self, response):

        content = BeautifulSoup(response,'html.parser')

        # extract all features which you want
        title = [title.find('a')['title'].strip() for title in content.findAll('h3')]
        price = [price.find('p').text.strip('Â') for price in content.findAll('div',{'class' : 'product_price'})]
        Stock_availablity = [stock.text.strip() for stock in content.findAll('p',{'class' : 'instock availability'})]

        for index in range(0, len(title)):
            self.results.append({
              'Title' : title[index],
              'Price' : price[index],
              'Stock_availablity' : Stock_availablity[index]
            })
    def to_csv(self):
         with open('books.csv','w', newline = '') as csv_file:
              writer = csv.DictWriter(csv_file, delimiter = ',', fieldnames = self.results[0].keys())
              writer.writeheader()

              for row in self.results:
                  writer.writerow(row)

              print('Stored results to books.csv')


    def run(self):
        for page in range(1,2):
            url = self.url + 'catalogue/page-'  + str(page) + '.html'
            response = self.fetch(url)
            self.parse(response.text)
        self.to_csv()

# main driver  instance
if __name__ == '__main__':
    scraper = Booktoscrape()
    scraper.run()
