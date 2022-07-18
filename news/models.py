# from papers.exeptions import ArticleException
from .configs import configs
from .helpers import get_all_url_sub_domain, get_domain_in_url, get_html, get_infomation, is_article, is_category, get_article_urls, is_feed

class Article:
    url: str
    html: str
    
    text: str
    top_image: str
    authors: list[str]
    title: str
    images: list[str]
    movies: list[str]
    
    def __init__(self, url) -> None:
        self.url = url
    
    def get_url(self):
        return self.url;
    
    def parse(self) -> None:
        text = " ".join(self.html.get_text().split())
        self.text = text

    def download(self) -> None:
        self.html = get_html(self.url, [])

class Category:
    url = '';
    
    def __init__(self, url) -> None:
        self.url = url
    
    def get_url(self):
        return self.url;

class Description:
    pass;

class Brand:
    pass;

class Feed:
    url = '';
    
    def __init__(self, url) -> None:
        self.url = url
    
    def get_url(self):
        return self.url;

class Config:
    def __init__(self, **args):
        for key, value in configs.items():
            if key not in args:
                self.__setattr__(key, value)
            else: self.__setattr__(key, args.key)

class Source:
    instance = None
    
    url_newspaper: str
    headers: list = []
    
    desctiption: str
    title: str
    
    config: Config
    articles: list[Article]
    categories: list[Category]
    feeds: list[Feed]
    
    def __init__(self, url_newspaper, **args):
        if Source.instance == None:
            Source.instance = self
        
        self.url_newspaper = url_newspaper;
        self.config = Config(args=args)
        
        urls, title, description = get_infomation(self.url_newspaper, self.headers)
        
        self.title = title
        self.desctiption = description
        
        self.categories = [Category(url) for url in urls if is_category(url)]
        self.feeds = [Feed(url) for url in urls if is_feed(url)]
        
        domain = get_domain_in_url(url_newspaper)
        sub_domains = get_all_url_sub_domain(domain, urls)
        article_urls = get_article_urls(sub_domains)
        
        self.articles = [Article(article_url) for article_url in article_urls if is_article(article_url)]
        
    @staticmethod
    def get_instance(self):
      if Source.instance == None:
             Source()
      return Source.instance

    def size(self) -> int:
        return len(self.articles)
    
    def article_urls(self) -> list:
        return [article.get_url() for article in self.articles]

    def category_urls(self) -> list:
        return [category.get_url() for category in self.categories]
    
    def feed_urls(self) -> list:
        return [feed.get_url() for feed in self.feeds]