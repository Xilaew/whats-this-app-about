import os

FILE = os.path.dirname(__file__)
stopwords = dict()
stopwords['de'] = set(map(str.strip, open(os.path.join(FILE, 'stopwords_de')).readlines()))
print(stopwords['de'])
