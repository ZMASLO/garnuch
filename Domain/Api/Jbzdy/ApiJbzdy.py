from bs4 import BeautifulSoup
from requests import get
from ...Meme.Meme import Meme

class ApiJbzdy():
    def __init__(self):
        self.url = 'https://jbzdy.com.pl'
        self.page_number = ''

    def loadMemes(self):
        page = BeautifulSoup(get(self.url).text, 'html.parser')
        for meme in page.find_all('div', attrs={'class': 'content-info'}):
            self.title = meme.find('div', attrs={'class': 'title'}).text.strip()
            self.image_url = meme.find('img', attrs={'class': 'resource-image'})['src']
            self.image = get(self.image_url).content
            yield Meme(self.title, self.image)

    def nextPage(self):
        page = get(self.url+'/str/'+self.page_number)
        page = BeautifulSoup(page.text, 'html.parser')
        nextPageUrl = page.find('div', attrs={'class': 'content pagg'}).find('a', attrs={'class': 'btn-next-page'})['href']
        self.url = nextPageUrl
        print('Next page')
