import requests
from bs4 import BeautifulSoup


class PinterestScraper:
    def load_images(self):
        '''
        html = ''

        with open('gety.html', 'r') as image:
            for line in image.read():
                html += line
        '''
        url = 'https://www.gettyimages.com.br/detail/foto/the-matterhorn-mountain-zermatt-switzerland-imagem-royalty-free/1174718425'

        headers = {
           "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
        }

        response = requests.get(url, headers = headers)
        return response

    def parse(self, html):
        content = BeautifulSoup(html.content, 'lxml')
        content =  content.find('div',attrs = {'class' : 'AssetCard-module__assetCardContainer___E0Uc9'}).find('img')
        content = content['src']

        return content
    def download(self, url):
        response = requests.get(url)
        filename = url.split('/')[-1]


        print('Downloading image %s from URL %s' % (filename, url))

        if response.status_code == 200:
            with open('./getty_images/' + filename, 'wb') as image:
                for chunk in response.iter_content(chunk_size=128):
                    image.write(chunk)

    def run(self):
        html = self.load_images()
        url = self.parse(html)


        self.download(url)

if __name__ == '__main__':
    scraper = PinterestScraper()
    scraper.run()
