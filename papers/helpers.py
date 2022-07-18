from operator import itemgetter
from bs4 import BeautifulSoup
from requests import Response, Session, Request
from urllib.parse import urljoin, urlparse
import re

PATTERN_CATEGORY = "^(http\:\/\/|https\:\/\/)([a-zA-Z0-9]{2,}\.)*[a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+(?:\/)*([a-zA-Z0-9]*)$"
PATTERN_ARTICLE = "^(http\:\/\/|https\:\/\/)([a-zA-Z0-9]{2,}\.)*[a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+(?:\/[a-zA-Z0-9\-\_\*\&\%\$\#\@\!\+\?]*){2,}$"
PATTERN_FEED = '^(http\:\/\/|https\:\/\/)([a-zA-Z0-9]{2,}\.)*[a-zA-Z0-9-]{1,61}[a-zA-Z0-9](?:\.[a-zA-Z]{2,})+(?:\/[a-zA-Z0-9\-\_\*\&\%\$\#\@\!\+\?]*)*\.rss$'

def get_answer():
    """Get an answer."""
    return True

def make_request(url: str, options: object) -> Response:
    method, data, headers = itemgetter('method', 'data', 'headers')(options)
    
    s = Session()
    req = Request(method, url, data, headers)
    prepped = s.prepare_request(req)
    res = s.send(prepped)

    return res

def parse_url(base_url: str, path: str) -> str:
    return urljoin(base_url, path)

def get_domain_in_url(url: str)-> str :
    return urlparse(url).netloc

def is_domain_in_url(domain: str, url: str) -> bool:
    if domain in url:
        return True
    
    return False

def is_sub_domain(domain: str, sub_domain: str) -> bool:
    if not is_domain_in_url(domain, sub_domain): return False
    return domain.split('.')[0] != sub_domain.split('.')[0] and sub_domain.split('.')[0] != 'www'

def is_element_in_list(element: any, list: list) -> bool:
    return element in list

def get_all_url_sub_domain(domain: str, list_url: list) -> list:
    list_url_sub_domain = list()
    
    for url in list_url:
        url = urlparse(url).scheme + '://' + urlparse(url).netloc
        if url in list_url_sub_domain: 
            continue
        
        domain_in_url = get_domain_in_url(url)
        
        if is_sub_domain(domain, domain_in_url):
            list_url_sub_domain.append(url)
            
    return list_url_sub_domain;

def is_category(url: str) -> bool:
    match_obj = re.match(PATTERN_CATEGORY, url)
    if match_obj: return True
    return False

def is_article(url: str) -> bool:
    match_obj = re.match(PATTERN_ARTICLE, url)
    if match_obj: return True
    return False

def is_feed(url: str) -> bool:
    match_obj = re.match(PATTERN_FEED, url)
    if match_obj: return True
    return False

def get_infomation(
    base_url : str,
    headers : list,
    method : str='GET',
    data : object={}
) -> list: 
    urls = list()
    title, description = '', ''
    
    res = make_request(base_url, options={
            "method": method, 
            'data': data, 
            'headers': headers  
        }
    )

    if res.status_code != 200:
        return False

    soup = BeautifulSoup(res.content, "html.parser")

    for url in soup.find_all('a', href=True):
        if hasattr(url, 'href'):
            urls.append(parse_url(base_url, url['href']))
    
    title = soup.find('title').get_text()
    description = soup.find('meta', attrs={"name": "description"})
    if description: description = description['content']
            
    return urls, title, description;

def get_html(
    base_url : str,
    headers : list,
    method : str='GET',
    data : object={}
):
    res = make_request(base_url, options={
                'method': method, 
                'data': data, 
                'headers': headers 
            }
        )
        
    if res.status_code != 200:
        return False

    return BeautifulSoup(res.content, "html.parser")

def get_urls(
    base_url: str,
    headers: list,
    method: str='GET',
    data: object={}
) -> list:
    domain = get_domain_in_url(base_url)
    out = list()
    
    res = make_request(base_url, options={
            "method": method, 
            'data': data, 
            'headers': headers  
        }
    )

    if res.status_code != 200:
        return False

    soup = BeautifulSoup(res.content, "html.parser")

    for url in soup.find_all('a', href=True):
        if not hasattr(url, 'href'):
            continue;

        parsed_url = parse_url(base_url, url['href'])        
        if parsed_url not in out and is_domain_in_url(domain, parsed_url):
            out.append(parse_url(base_url, url['href']))
            
    return out;
    
def get_category_urls(urls: list) -> list:
    return [url for url in urls if is_category(url)]

def get_article_urls(urls: list) -> list:
    out = list()
    for url in urls:
        urls = get_urls(url, [])
        out = out + [url for url in urls if is_article(url)]
    
    return out

def get_feed_urls(urls: list) -> list:
    return [url for url in urls if is_feed(url)]