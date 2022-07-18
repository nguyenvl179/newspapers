class ArticleException(Exception):
    message: str = ''
    
    def __init__(self, message="You must parse an article before you try to"):
        self.message = message
        super().__init__(self.message)