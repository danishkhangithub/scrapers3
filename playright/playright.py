# import libraries
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
         browser = p.chromium.launch(headless = False)
         page = browser.new_page()
         page.goto('https://www.pagesjaunes.fr/annuaire/chercherlespros?quoiqui=bureau+de+tabac&ou=Bretagne&univers=pagesjaunes&idOu=R53')
         page.wait_for_timeout(4000)

         login = page.query_selector('button[id = "didomi-notice-agree-button"]')
         #login = page.query_selector('')
         login.click()
         page.wait_for_timeout(4000)

         browser.close()


if __name__ == '__main__':
   main()