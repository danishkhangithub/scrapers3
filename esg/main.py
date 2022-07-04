# built-ins
from time import sleep
import re
from sys import platform
import dateutil.parser
import datetime
import pytz
from sys import platform
from typing import Dict, List, Tuple
import csv
from pprint import pprint
# external
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.utils import requote_uri
from bs4 import BeautifulSoup, NavigableString
from fake_useragent import UserAgent
from langdetect import detect
import xlrd
import numpy as np
# selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# internal
from config import tzinfos, xls_file, chrome_options, zenscrape_api, DELAY, DEFAULT_TIMEOUT, chromedriver_path
from tools import requests_retries, decode_email


class ScrapingTargets:

    def __init__(self, pr_site: str, source: str, company: str, emails: str, title: str,
                 link: str, ticker: str, full_text: str, release_date: str):
        self.pr_site = pr_site
        self.source = source
        self.company = company
        self.emails = emails
        self.title = title
        self.link = link
        self.ticker = ticker
        self.full_text = full_text
        self.release_date = release_date

    def asdict(self):
        return {'pr_site': self.pr_site,
                'source': self.source,
                'company': self.company,
                'emails': self.emails,
                'title': self.title,
                'link': self.link,
                'ticker': self.ticker,
                'full_text': self.full_text,
                'release_date': self.release_date
                }


class MainScraper:

    def __init__(self):
        self.allprs = []

    def read_xls(self):
        wb = xlrd.open_workbook(xls_file)
        sheet = wb.sheet_by_index(0)
        self.companies_dicts = []
        for i in range(sheet.nrows)[3:]:
            if sheet.row_values(i)[2]:
                company_dict = {'name': sheet.row_values(i)[0], 'ticker': sheet.row_values(i)[
                    2], 'pr-agency':  sheet.row_values(i)[3].lower()}
                self.companies_dicts.append(company_dict)
        pprint(self.companies_dicts)

    def globenewswire_scraper(self) -> None:
        """Main scraper for GlobeNewsWire. Requires cookies from a requests session to traverse paginations"""

        base_url = "https://www.globenewswire.com"
        pr_site = base_url.split('.')[1]
        print(f"START {pr_site} scrape")
        driver = webdriver.Chrome(
            #chrome_options=chrome_options,
            executable_path=chromedriver_path
        )
        driver.maximize_window()

        # Accept JS cookies script - only necessary in Kiosk mode (?)
        try:
            driver.execute_script("arguments[0].click();", driver.find_element_by_class_name(
                'btn-primary jquery-accept-disclosure'))
            driver.execute_script("arguments[0].click();",
                                  driver.find_element_by_xpath('/html/body/div[6]/div/div/a'))
        except:
            pass

        for company in self.companies_dicts:
            if company['pr-agency'] == 'globenewswire':

                prs = []
#                url = f"{base_url}/Search/NewsSearch?organization={requote_uri(company['name'] + ' ' + company['ticker'].split(',')[0])}&lang=en"
                url = f"{base_url}/search/keyword/{requote_uri(company['name'])}&lang=en"

                print(url)
                driver.get(url)
                sleep(DELAY/2)
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/a'))

                sleep(DELAY/2)
                search_box = driver.find_element_by_id('quicksearch-textbox')
                driver.execute_script("arguments[0].click();", driver.find_element_by_id('quicksearch-textbox'))
                search_box.send_keys(
                    company['name'] + ' ' + company['ticker'].split(',')[0])
                driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="quicksearch-button"]/i'))
                sleep(1)

                # Main try block wrap to catch if any results were returned
                try:
                    # Handling to maintain session cookie of page position
                    for page in range(5):

                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        links = soup.select('#content-R3 > div > h1 > a')
                        hrefs = [base_url+pr['href'] for pr in links]
                        prs.extend(hrefs)
                        sleep(DELAY)
                        # Pagination is VERY unusual. First hit element 5, then 7, 8, 9 and remain on 9
                        if page == 0:
                            next = '5'
                        elif page == 1:
                            next = '7'
                        elif page == 2:
                            next = '8'
                        else:
                            next = '9'
                        pagination = driver.find_element_by_xpath(
                            f'/html/body/form/div/div[5]/div[12]/ul/li[{next}]/a')
                        driver.execute_script(
                            "arguments[0].click();", pagination)

                    prs = [pr for pr in prs if '/en/' in pr]
                    print(prs)
                    results = [self.globenewswire_subscraper(
                        i, company['name'], company['ticker']) for i in prs]
                    for i in results:
                        self.allprs.append(i)
                except Exception as e:
                    print(f"ERROR {e}")
        driver.close()
        driver.quit()

    def globenewswire_subscraper(self, url: str, company_name: str, ticker: str) -> dict:
        """Individual press release scraper for GlobeNewsWire."""


        headers = {"apikey": zenscrape_api}
        params = (("url", url), ("location", "na"))
        r = requests_retries().get('https://app.zenscrape.com/api/v1/get',
                                   headers=headers, params=params)
        soup = BeautifulSoup(r.content, 'html.parser')

        title = soup.find('meta', {'name': 'title'}).attrs['content']
        source = soup.find('span', {'itemprop': 'author copyrightHolder'}).text
        print(title)
        release_date = soup.select(
            '#post-content-metadata > span.post-metadata.dt-green > span > em > time')[0].text
        release_date = dateutil.parser.parse(
            release_date, tzinfos=tzinfos).astimezone(pytz.utc)
        raw_text = soup.find('span', {'class': 'article-body'}).text.strip()
        # Remove excessive whitespace
        full_text = re.sub(r'(\n\s*)+\n+', '\n\n', raw_text)

        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', full_text)

        # if detect(full_text) != 'en':
        #     print('other lang')
        #     return None

        scraped_data = ScrapingTargets('GlobeNewsWire', source, company_name, ', '.join(
            emails), title, url, ticker, full_text, str(release_date))
        return scraped_data.asdict()

    def businesswire_scraper(self) -> None:
        """Main scraper for BusinessWire. Requires a selenium driver to retrieve PR links"""

        base_url = "https://www.businesswire.com"
        pr_site = base_url.split('.')[1]
        print(f"START {pr_site} scrape")

        driver = webdriver.Chrome(
            executable_path=chromedriver_path
        )
        for company in self.companies_dicts:
            if company['pr-agency'] == 'businesswire':
                prs = []

                for i in range(4):

                    url = f"{base_url}/portal/site/home/template.PAGE/search/?searchType=ticker&searchTerm={company['ticker']}&searchPage={str(i+1)}"

                    # Get remaining links from AJAX pagination
                    driver.get(url)
                    sleep(DELAY)
                    soup = BeautifulSoup(driver.page_source, 'html.parser')
                    try:
                        ul = soup.find('ul', {'class': 'bw-news-list'})
                        href = [li.find('a')['href']
                                for li in ul.find_all('li')]
                        prs.extend([pr for pr in href if '/en/' in pr])
                    except:
                        print(
                            f"No PRs found for ticker {company['ticker']} on page {i}")

                results = [self.businesswire_subscraper(
                    i, company['name'], company['ticker']) for i in prs]
                for i in results:
                    self.allprs.append(i)

        driver.close()
        driver.quit()

    def businesswire_subscraper(self, url: str, company_name: str, ticker: str) -> dict:
        """Individual press release scraper for BusinessWire. Relies on a Zenscrapeo; ;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;p proxied request to avoid bot detection"""

        headers = {"apikey": zenscrape_api}
        params = (("url", url), ("location", "na"))

        try:

            r = requests_retries().get('https://app.zenscrape.com/api/v1/get',
                                       headers=headers, params=params)
            soup = BeautifulSoup(r.content, 'html.parser')

            try:
                raw_title = soup.find('h1', {'class': 'article-headline'})
                title = raw_title.text
            except:
                raw_title = soup.find('h1', {'class': 'epi-fontLg'})
                title = raw_title.text
            print(title)

            release_date = soup.find('time').text
            release_date = dateutil.parser.parse(
                release_date[:-21]+' ET', tzinfos=tzinfos).astimezone(pytz.utc)
            raw_text = soup.find(
                'div', {'class': 'bw-release-story'}).text.strip()
            # Remove excessive whitespace
            full_text = re.sub(r'(\n\s*)+\n+', '\n\n', raw_text)

            contacts = [i.text.strip() for i in soup.find(
                'div', {'class': 'bw-release-contact'}).find_all('p')]

            # Try all methods for email parsing
            try:
                # Emails can either be nested within a span singly or doubly
                try:
                    emails = [decode_email(i.findNext('span')['data-cfemail']) for i in
                              soup.find('div', {'class': 'bw-release-contact'}).find_all('a')]
                except:
                    emails = [decode_email(i.findNext('span').findNext('span')['data-cfemail']) for i in
                              soup.find('div', {'class': 'bw-release-contact'}).find_all('a')]
                try:
                    decoded_contacts = [contacts[i].replace(
                        '[email\xa0protected]', j) for i, j in enumerate(emails)]
                    for i in decoded_contacts:
                        full_text += i
                except:
                    for i in contacts:
                        full_text += i
            except:
                emails = []

            scraped_data = ScrapingTargets('BusinessWire', '', company_name, ', '.join(
                emails), title, url, ticker, full_text, str(release_date))
            return scraped_data.asdict()

        except Exception as e:
            print(f"ERROR {e}")

    def prnewswire_scraper(self) -> None:
        """Main scraper for PRNewsWire. Straightforward Requests."""

        base_url = "https://www.prnewswire.com"
        pr_site = base_url.split('.')[1]
        print(f"START {pr_site} scrape")

        for company in self.companies_dicts:
            if company['pr-agency'] == 'prnewswire':

                url = f"{base_url}/search/news/?keyword={requote_uri(company['name'])}&page=1&pagesize=25"
                print(url)
                r = requests_retries().get(
                    url, headers={'User-Agent': UserAgent().random})
                soup = BeautifulSoup(r.content, 'html.parser')
                links = soup.find_all('a', {'class': 'news-release'})
                prs = [base_url+pr['href'] for pr in links]
                print(prs)
                results = [self.prnewswire_subscraper(
                    i, company['name'], company['ticker']) for i in prs]
                for i in results:
                    self.allprs.append(i)

    def prnewswire_subscraper(self, url: str, company_name: str, ticker: str) -> dict:
        """Individual press release scraper for PRNewsWire. Uses Requests."""

        sleep(DELAY/3)

        r = requests_retries().get(url, timeout=5)
        print(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Try block to catch PRs that have been removed entirely but whose links are still visible
        try:
            title = soup.find('title').text
            print(title)

            source = ''
            for i in soup.find('section', {'class': 'release-body container'}).find_all('p'):
                if 'SOURCE' in i.text:
                    source += i.text[7:]

            release_date = soup.find('p', {'class': 'mb-no'}).text
            release_date = dateutil.parser.parse(
                release_date, tzinfos=tzinfos).astimezone(pytz.utc)
            raw_text = soup.find(
                'section', {'class': 'release-body container'}).text.strip()
            # Remove excessive whitespace
            full_text = re.sub(r'(\n\s*)+\n+', '\n\n', raw_text)

            # PRNewsWire's email decoding is a little more complicated, two possible methods
            # If table is present
            try:
                table = soup.find('div', {'class': 'table-responsive'})
                contacts = []
                for line in table.findAll('tr'):
                    row = []
                    for l in line.findAll('td'):
                        row.append(l.text)
                    contacts.append(row)

                contacts_formatted = [''.join(i)
                                      for i in np.array(contacts[1:]).T]
                emails = [decode_email(i.findNext('span')['data-cfemail']) for i in
                          table.find_all('a')]
                decoded_contacts = [contacts_formatted[i].replace(
                    '[email\xa0protected]', j) for i, j in enumerate(emails)]
                for i in decoded_contacts:
                    full_text += i

            # if in raw text
            except:
                emails = []
                for i in soup.find_all('a', {'rel': 'nofollow'}):
                    try:
                        if 'cdn-cgi' in i['href']:
                            email = decode_email(
                                i.findNext('span')['data-cfemail'])
                            emails.append(email)
                    except:
                        pass
                emails_dict = {i + 1: j for i, j in enumerate(emails)}
                full_text = full_text.replace('[email\xa0protected]', '{}', len(
                    emails_dict)).format(*emails_dict.values())

            if detect(full_text) != 'en':
                print('other lang')
                pass

            scraped_data = ScrapingTargets('PRNewsWire', source, company_name, ', '.join(
                emails), title, url, ticker, full_text, str(release_date))
            return scraped_data.asdict()

        except Exception as e:
            print(f"ERROR {e}")

    def to_csv(self, filename):
        allprs = [i for i in self.allprs if i]
        with open(filename, 'w', encoding='utf-8') as csv_file:
            fieldnames = sorted(
                list(set(k for d in allprs for k in d)))
            writer = csv.DictWriter(
                csv_file, fieldnames=fieldnames, dialect='excel')
            writer.writeheader()
            for row in allprs:
                writer.writerow(row)

    def run_all_scrapers(self):
        """Complete entry point - reads xls, runs all 3 scrapers and outputs CSV"""
        self.read_xls()
        self.globenewswire_scraper()
        self.businesswire_scraper()
        self.prnewswire_scraper()
        self.to_csv('releases.csv')

#if __name__ == '__main__':
#    a = MainScraper()
#    a.read_xls()
#    a.businesswire_scraper()

if __name__ == '__main__':
     a = MainScraper()
     #a.read_xls()
#     a.businesswire_scraper()
# Globenewswire bug to be fixed
#     a.globenewswire_scraper()
     a.prnewswire_scraper()
     a.to_csv('pressreleases raw.csv')




