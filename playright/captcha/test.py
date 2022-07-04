from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import re


class Captcha:
    def __init__(self):
        self.url = 'https://www.google.com/recaptcha/api2/demo'

        chrome_driver_path = '/home/danish-khan/scrapers/researchgate/chromedriver'

        chrome_options = Options()
        #chrome_options.add_argument('--headless')

        self.driver = webdriver.Chrome(
          executable_path=chrome_driver_path, options=chrome_options
        )

    def run(self):
        # retrive url in headless browser
        self.driver.get(self.url)

        # find iframe box
        try:
           frames = self.driver.find_elements_by_tag_name("iframe")
           recaptcha_control_frame = None
           recaptcha_challenge_frame = None
           for index, frame in enumerate(frames):
               if re.search('reCAPTCHA', frame.get_attribute("title")):
                   recaptcha_control_frame = frame

               if re.search('recaptcha challenge', frame.get_attribute("title")):

                   recaptcha_challenge_frame = frame
           if not (recaptcha_control_frame and recaptcha_challenge_frame):
                print("[ERR] Unable to find recaptcha. Abort solver.")
                sys.exit()
           time.sleep(2)
           frames = self.driver.find_elements_by_tag_name("iframe")
           self.driver.switch_to.frame(recaptcha_control_frame)
           # click on checkbox to activate recaptcha
           self.driver.find_element_by_class_name("recaptcha-checkbox-border").click()

           # switch to recaptcha audio control frame
           time.sleep(2)

           self.driver.switch_to.default_content()
           frames = self.driver.find_elements_by_tag_name("iframe")
           self.driver.switch_to.frame(recaptcha_challenge_frame)
           time.sleep(5)

           src = self.driver.find_element_by_css_selector('button[id= "recaptcha-audio-button"]').get_attribute('src')
           print(f"[INFO] Audio src: {src}")

        except Exception as e:
           print('Not Found', e)



        # must close the driver after task finished
        #self.driver.close()

if __name__ == '__main__':
    scraper = Captcha()
    scraper.run()
