import os

import play_scraper
import google_play_scraper
import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pprint

from google_play_scraper.constants.url import Formats
from google_play_scraper.utils.request import post

import matplotlib.pyplot as plt

app_id = 'com.taptaptales.fortyfourcats'
app_id = 'tech.jonas.travelbudget'

FILE = os.path.dirname(__file__)
stopwords = dict()
stopwords['en'] = set(map(str.strip, open(os.path.join(FILE, 'stopwords_en'), mode='r', encoding='utf-8').readlines()))
stopwords['de'] = set(map(str.strip, open(os.path.join(FILE, 'stopwords_de'), mode='r', encoding='utf-8').readlines()))
stopwords['es'] = None

for lang,country in [('de','de'),('en','us'),('es','es')]:
	app = google_play_scraper.app(app_id, lang=lang, country=country)
	try:
		reviews, cont = google_play_scraper.reviews(app_id, count=500, lang=lang, country=country)
	except IndexError:
		print('no reviews found')
		reviews = []
	review_string = ' '.join([x.get('content') for x in reviews]) + 'test'

	fig, ax = plt.subplots(2,1)
	try:
		desc_cloud = WordCloud(stopwords=stopwords[lang]).generate(app.get('description'))
		desc_im = ax[0].imshow(desc_cloud, interpolation='bilinear')
		ax[0].axis("off")
		ax[0].set_title('App Description')
	except ValueError:
		print('no content')

	try:
		review_cloud = WordCloud(stopwords=stopwords[lang]).generate(review_string)
		review_img = ax[1].imshow(review_cloud, interpolation='bilinear')
		ax[1].axis("off")
		ax[1].set_title('Comments')
	except ValueError:
		print('no content')
	fig.show()

plt.show()
