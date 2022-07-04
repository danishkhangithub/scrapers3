# Database path (when developing in sqlite)
from sys import platform
from selenium import webdriver
from dateutil.tz import gettz
import os

cwd = os.getcwd()
#chromedriver_path = 'C:\Windows\chromedriver.exe'
chromedriver_path = 'C:\Program Files\ChromeDriver\chromedriver.exe'

# ---------------
DEFAULT_TIMEOUT = 5
DELAY = 8.0
xls_file = 'ESGC Company universe 1.2.xlsx'
# Set timezones

zenscrape_api = '7bbc6400-ba6f-11ea-b2a1-837839d858fe'


tzs = ["ET", "EST", "Eastern Daylight Time"]
tzinfos = {i: gettz("US/Eastern") for i in tzs}

# ---------------
# Selenium parameters

if 'linux' in platform:
    chrome_options = webdriver.ChromeOptions()
    #chrome_options.add_argument('--headless')
    chrome_options.add_argument("--kiosk")
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-gpu')
    #chrome_options.add_argument('--window-size=1280x1696')
    # chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    # chrome_options.add_argument('--hide-scrollbars')
    # chrome_options.add_argument('--enable-logging')
    # chrome_options.add_argument('--log-level=0')
    # chrome_options.add_argument('--v=99')
    # chrome_options.add_argument('--single-process')
    # chrome_options.add_argument('--data-path=/tmp/data-path')
    # chrome_options.add_argument('--ignore-certificate-errors')
    # chrome_options.add_argument('--homedir=/tmp')
    # chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    #chrome_options.binary_location = "/root/pr-spiders/bin/headless-chromium"
elif 'win' in platform:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')