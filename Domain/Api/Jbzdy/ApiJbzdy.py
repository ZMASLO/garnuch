from bs4 import BeautifulSoup
from requests import get
from ..ApiAbstract import ApiAbstract
from ...Meme.Meme import Meme

class ApiJbzdy(ApiAbstract):
    def __init__(self):
        self.url = 'https://jbzd.com.pl'
        self.page_number = ''

    def loadMemes(self):
        page = BeautifulSoup(get(self.url).text, 'html.parser')
        for meme in page.find_all('div', attrs={'class': 'article-content'}):
            self.title = meme.find('h3', attrs={'class': 'article-title'}).text.strip()
            try:
                self.image_url = meme.find('img', attrs={'class': 'article-image'})['src']
                self.image = get(self.image_url).content
                yield Meme(self.title, self.image)
            except:
                print('video - skipping it')

    def nextPage(self):
        page = get(self.url+'/str/'+self.page_number)
        page = BeautifulSoup(page.text, 'html.parser')
        nextPageUrl = page.find('div', attrs={'class': 'pagination-buttons'}).find('a', attrs={'class': 'pagination-next'})['href']
        self.url = nextPageUrl
        print('Next page')
