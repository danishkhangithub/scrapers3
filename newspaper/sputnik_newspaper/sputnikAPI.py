from multiprocessing import connection
import requests
from bs4 import BeautifulSoup
import json
import sqlite3
import random
from datetime import datetime

class GetNewsLink:

    def __init__(self):
        self.url = "https://sputniknews.com/"
        self.links = []

    def GetSourceCode(self):
        r = requests.get(self.url)
        if(r.status_code == 200):
            self.BeautifulSoupProcess(r.content)
        return self.links

    def BeautifulSoupProcess(self,context):
        soup = BeautifulSoup(context,"lxml")
        self.LastestNewsLinks(soup)
        self.GetOtherLinks(soup)
        

    def LastestNewsLinks(self,soup):
        links = soup.find_all('a',attrs={"class":"cell-main-photo__image"})
        for link in links:
            if (link.find_parent('div',attrs={"data-floor":1})):
                href = self.url+link.get('href')
                self.links.append((href,"lastest_news"))


    def GetOtherLinks(self,soup):
        otherLinks = soup.find_all('a',attrs={"class":"cell-list__item"})
        for link in otherLinks:
            category = (link.find_parent('div',attrs={"class":"cell-list__list"}).previous_sibling).text
            href = self.url + link.get('href')
            self.links.append((href,category))










class NewsDetail:
    def __init__(self,url):
        self.url = url
        self.connection = sqlite3.connect('/home/harun/Desktop/SputnikApi/Django/sputnik_news/db.sqlite3')
        self.cursor = self.connection.cursor()
        self.detail={}

    def GetSourceCode(self):
        r=requests.get(url)
        if(r.status_code==200):
            self.BeautifulSoupProcess(r.content)
            self.ConvertToJson(self.detail)

    
    def BeautifulSoupProcess(self,content):
        soup = BeautifulSoup(content,'lxml')
        self.GetDetails(soup)

    
    def GettingTwitterLink(self,url):
        r = requests.get(url)
        newUrl = (r.url)
        index1=newUrl.find('status/')+7
        index2=newUrl.find('/',index1)
        iframelink = f"https://platform.twitter.com/embed/Tweet.html?&id={newUrl[index1:index2]}"
        return iframelink


    def ConvertToJson(self,dictironaryData):
        convertedData=json.dumps(dictironaryData)

        self.SaveToDatabase(convertedData)
        

    def SaveToDatabase(self,convertedData):
        randomNumber = random.randint(1,1000)
        id = int(datetime.now().microsecond)+randomNumber
        self.connection.execute('insert into news_newsdetail values(?,?)',[id,convertedData])
        self.connection.commit()
        



    def GetDetails(self,soup):
        try:
            title = soup.find('h1',attrs={"class":"article__title"}).text
        except:
            pass
        try:
            news_image = soup.find('div',attrs={"class":"media__size"}).find('img').get('src')
        except:
            pass
        try:

            announce_text = soup.find('div',attrs={"class":"article__announce-text"}).text
        except:
            pass

        try:

            self.detail={"title":title,"news_image":news_image,"announce_text":announce_text,"content":[]}
        except:
            pass


        
        article_body=soup.find('div',attrs={"class":"article__body"})

        for detail in article_body:
            try:
                by_journalist=(detail.find('div',attrs={"class":"article__text"}).text)
                self.detail['content'].append({"by_journalist":by_journalist})


            except:
                pass

            try:
                quote = (detail.find('div',attrs={"class":"article__quote-text"}).text)
                self.detail['content'].append({"quote":quote})


            except:
                pass

            try:
                related_link = detail.find('div',attrs={"class":"article__article"}).find('a')
                related_link_href = related_link.get('href')
                related_link_title = related_link.get('title')
                related_link_image = related_link.find('img').get('src')
                self.detail['content'].append({"related_link":[{"related_link_href":related_link_href,"related_link_title":related_link_title,"related_link_image":related_link_image}]})


            except:
                pass


            try:
                twitterlink =(detail.find('div',attrs={"class":"ria-tweet"}).find('a').get('href'))
                self.detail['content'].append({"iframelinktwitter":(self.GettingTwitterLink(twitterlink))})
            except:
                pass

            try:
                medias = (detail.find('div',attrs={"class":"media__size"}).find('img').get('src'))
                self.detail['content'].append({"medias":medias})
            except:
                pass

            try:
                article_h2_titles=(detail.find('h2',attrs={"class":"article__h2"}).text)
                self.detail['content'].append({"article_h2_titles":article_h2_titles})
            except:
                pass
            





            




links = GetNewsLink().GetSourceCode()

for url,category in links:
    NewsDetail(url).GetSourceCode()



