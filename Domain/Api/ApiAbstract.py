class ApiAbstract:
    
    def loadMemes(self):
        raise NotImplementedError('subclasses must override this method!')

    def nextPage(self):
        raise NotImplementedError('subclasses must override this method!')