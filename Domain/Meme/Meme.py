class Meme():
    def __init__(self, title, image):
        self.title = title
        self.image = image

    def __str__(self):
        return '{}: {}'.format(self.title, self.image_url)