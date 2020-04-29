import os

import google_play_scraper
import matplotlib.pyplot as plt
from wordcloud import WordCloud

FILE = os.path.dirname(__file__)
stopwords = dict()
stopwords['en'] = set(map(str.strip, open(os.path.join(FILE, 'stopwords_en'), mode='r', encoding='utf-8').readlines()))
stopwords['de'] = set(map(str.strip, open(os.path.join(FILE, 'stopwords_de'), mode='r', encoding='utf-8').readlines()))
stopwords['es'] = None


def create_appcloud( app_id: str, lang: str, country: str):
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
	return fig

if __name__ == '__main__':
	app_id = 'kajfosz.antimatterdimensions'
	#app_id = 'tech.jonas.travelbudget'
	for lang, country in [('de','de'),('en','us'),('es','es')]:
		create_appcloud(app_id, lang, country).show()
	plt.show()
