# import packages
from multiprocessing import connection
import requests
from bs4 import BeautifulSoup
from scrapy.selector import Selector
import json
import sqlite3
import re
import json
import random
import datetime


class GetNewsLink:

    def __init__(self):
       self.url = 'https://www.bbc.com/news'
       self.links = []

    def GetSourceCode(self):
        response = requests.get(self.url)
        if response.status_code == 200:
           self.BeautifulSoupProcess(response.content)
        return self.links

    def BeautifulSoupProcess(self, context):
        soup = BeautifulSoup(context, 'lxml')
        self.LastestNewsLinks(soup)
        self.GetOtherLinks(soup)

    def LastestNewsLinks(self, soup):
        html_content = ''
        with open('bbc.html','r') as html:
             for line in html.read():
                 html_content+=line

        soup = BeautifulSoup(html_content, 'lxml')

        top_news = soup.find('div', {'id': 'news-top-stories-container'})
        top_news_links = top_news.select('[data-entityid= "container-top-stories#1"] a')
        top_news_links = [link['href'] for link in top_news_links]
        for  i in top_news_links:
            if list(map(int, re.findall(r'\d+', i))) != []:
               self.links.append(i)

        for cat in range(1,15):
            top_news_links2 = top_news.select('[data-entityid= "container-top-stories#%s"] a' % cat ) #%cat
            top_news_links2 = [link['href'] for link in top_news_links2]
            #print(top_news_links2)
            for  i in top_news_links2:
                if list(map(int, re.findall(r'\d+', i))) != []:
                   self.links.append(i)


#        print(set(self.links))
        self.links = set(self.links)
        return self.links

    def GetOtherLinks(self, soup):
        pass


class NewsDetail:

      def __init__(self,url):
          self.url = url
          self.connection = sqlite3.connect('/home/danish-khan/scrapers/freelancing3/newspaper/db.sqlite3')
          self.cursor = self.connection.cursor()
          self.details = {}

      def GetSourceCode(self):
          r=requests.get(url)
          if(r.status_code==200):
              self.BeautifulSoupProcess(r.content,url)
              self.ConvertToJson(self.details)

      def BeautifulSoupProcess(self,content,url):
          soup = BeautifulSoup(content,'lxml')
          self.GetDetails(soup,url)

      def ConvertToJson(self,dictironaryData):
          convertedData=json.dumps(dictironaryData)
          print(convertedData)


          self.SaveToDatabase(convertedData)



      def SaveToDatabase(self, convertedData):
          randomNumber = random.randint(1,1000)
          id = int(datetime.datetime.now().microsecond)+randomNumber
          self.connection.execute('insert into bbc_news values(?,?)',[id,convertedData])
          self.connection.commit()


      def GetDetails(self,soup,url):
          try:
             title = soup.find('h1',attrs={"id":"main-heading"}).text
          except:
             try:
                title = soup.select_one("#lx-event-title").text
             except Exception as e:
                print('\nError\t',e,url)
                title = None
                pass
          else:
             pass

          try:
             image = soup.select_one('div[data-component="image-block"] img')['src']
          except Exception as e:
             print('\terror\t',e)
             image = None

          text_tags = ['b','h1','p']
          texts = []
          try:
             for i in text_tags:
                 text = [g.text for g in soup.select('div[data-component="text-block"] %s' %i)]
                 texts.append(text)
          except Exception as e:
             print('\terror\t',e)
             text = None


          self.details = {
              'Title' : title,
              'Image' : image,
              'Text' : texts,
          }


          try:
             name = soup.select_one('p strong').text

          except Exception as e:
             print('\terror\t',e)
             name = None

          try:
             time = soup.select_one('[data-testid="timestamp"]')['datetime']

          except Exception as e:
             print('\terror\t',e)
             time = None

          self.details['Author'] = name
          self.details['Time'] = time


          #print(self.details)





#
links = GetNewsLink().GetSourceCode()
#links = GetNewsLink().LastestNewsLinks()
for url in links:
    NewsDetail(url).GetSourceCode()
    break
