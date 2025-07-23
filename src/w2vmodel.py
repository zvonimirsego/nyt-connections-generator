import gensim.downloader as api
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

model = api.load("word2vec-google-news-300")