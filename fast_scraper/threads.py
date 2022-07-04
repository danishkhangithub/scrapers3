# import packages
import requests
from bs4 import BeautifulSoup
import urllib
import time
#from multiprocessing import cpu_count, Pool 
from concurrent.futures import ThreadPoolExecutor

def get_links():
  curr_list = 'https://en.wikipedia.org/wiki/List_of_circulating_currencies'
  all_links = []
  response = requests.get(curr_list)
  soup = BeautifulSoup(response.text,'lxml')
  all_link_el = soup.select('p+table td:nth-child(2) > a, p+table td:nth-child(1) > a')
  for link_el in all_link_el:
        link = link_el.get("href")
        link = urllib.parse.urljoin(curr_list, link)
        all_links.append(link)
        
  return all_links
  
def fetch(link):
   response = requests.get(link)
   # disk i/o
   filename = './output/'+ link.split('/')[-1] + 'html'
   with open(filename, 'wb') as f:
        f.write(response.content) 
   
   print('.',end = "", flush = True)
  
if __name__ == '__main__':
   links = get_links()  
   start_time = time.time()

  
#   print(f'Total pages: {len(links)}')
#   for link in links:
#       fetch(link)
   # multiprossesing 
   with ThreadPoolExecutor(max_workers = 100) as p:
       p.map(fetch, links)  
       
   duration = time.time() - start_time
   print('\n\t Total time taken:', duration)
   
   
   
   
