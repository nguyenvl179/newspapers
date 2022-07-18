# import newspaper
# from newspaper import Article

# first_article = Article(url="https://www.lemonde.fr/en/international/article/2022/07/15/eu-commission-takes-hungary-to-court-over-lgbt-law_5990286_4.html", language='en')
# first_article.download()
# first_article.parse()
# print(first_article.text)
# cnn_paper = newspaper.build('https://cnn.com/', memoize_articles=False)
# for url in cnn_paper.article_urls():
#     print(url)

# print(len(cnn_paper.article_urls()))

# from papers import build
# from papers.models import Article

# cnn_article = Article('https://edition.cnn.com/2022/07/17/uk/uk-conservative-leadership-trans-intl-gbr/index.html')
# cnn_article.download()
# cnn_article.parse()
# print(cnn_article.text)

# print(len(article_urls))
# pd = parse_sitemap(
#     'https://edition.cnn.com/sitemaps/article-2022-06.xml', [], ["loc", "lastmod"])
# print(pd)
