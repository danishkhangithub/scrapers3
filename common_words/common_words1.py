###########################################
#
#     Script to extract most common words
#           from a given website
#
#                   by
#
#                Danish Khan
#
###########################################

# packages 
from urllib.request import urlopen
from html.parser import HTMLParser
import json
import collections

# words parser class
class WordsParser(HTMLParser):
     # tags to search within text html
     search_tags = ['p','div','span','a','h1','h2','h3','h4']
    
     # common_words list
     common_words = {}
    
     # current tag
     current_tag = ''

     # handles starting tag
     def handle_starttag(self, tag, attr):
        # store current tag
        self.current_tag = tag   
              
     # handles tag's data
     def handle_data(self, data):
        if self.current_tag in self.search_tags:
            # loop over word list within current tag list
            for word in data.strip().split():
                # convet words to lowercase
                common_word = word.lower()
                
                # filter words
                if (len(common_word) > 2 
                   and common_word not in ['the','at','and','with','are']
                   ):
                   
                   try:             
                      # store common words
                      self.common_words[common_word] += 1
                      
                   except:
                      # try to update common_word 
                      self.common_words.update({common_word:1})
                   
                                            
# main driver
if __name__ == '__main__':
    # target URL to scrape
    url = 'https://las.uic.edu/advising/'
    
    # make HTTP GET request to the target URL
    response = urlopen(url)
    
    # extract HTML document form response
    html = response.read().decode('utf-8', errors = 'ignore')
    
    # create words parser instance
    words_counter = WordsParser() 
    
    # feed html to words parser
    words_counter.feed(html)          
    
    words_countts = collections.Counter(WordsParser.common_words)
    
    # extract most common words
    most_common = words_countts.most_common(25)
    
    # loop over most common words
    for word, count in most_common:
        print(word, str(count) + ' times', sep = ": ")
