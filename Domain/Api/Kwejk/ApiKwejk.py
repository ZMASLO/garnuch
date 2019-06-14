from bs4 import BeautifulSoup
from requests import get
from ...Meme.Meme import Meme

class ApiKwejk():
    def __init__(self):
        self.url = 'https://kwejk.pl/'
        self.page_number = ''

    def loadMemes(self):
        page = BeautifulSoup(get(self.url).text, 'html.parser')
        for meme in page.find_all('div', attrs={'class': 'media-element'}):
            self.title = meme.find('h2').text.strip()
            self.image_url = meme['data-image']
            self.image = get(self.image_url).content
            yield Meme(self.title, self.image)

    def nextPage(self):
        if self.page_number == '':
            page = get(self.url)
        else:
            page = get(self.url+'/strona/'+self.page_number)
        page = BeautifulSoup(page.text, 'html.parser')
        nextPageUrl = page.find('div', attrs={'class': 'pagination'}).find('a', attrs={'class': 'btn btn-next btn-gold'})['href']
        self.url = nextPageUrl
        print('Next page')