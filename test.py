from papers import build
from papers.models import Article

cnn_article = Article('https://edition.cnn.com/2022/07/17/uk/uk-conservative-leadership-trans-intl-gbr/index.html')
cnn_article.download()
cnn_article.parse()
# print(cnn_article.text)
