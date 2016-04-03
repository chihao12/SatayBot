import flickrapi
import tweepy
import time
from bs4 import BeautifulSoup
from random import choice, randint, shuffle, random
import xml.etree.ElementTree as ET
import urllib

from secret import FLICKR_KEY, FLICKR_SECRET, TWITTER_KEY, TWITTER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
from config import USER_ID, TAGS, MIN_HEIGHT, MIN_WIDTH

photo_list = []
random_page = randint(1, 100)

def flickr():
	flickr = flickrapi.FlickrAPI(FLICKR_KEY, FLICKR_SECRET, format='etree')

	photos = flickr.photos_search(
		per_page = 100, 
		page = 5, 
		text = TAGS,
		tag_mode = 'any',
		extras = 'url_c', 
		sort = 'relevance'
	)

	soup = BeautifulSoup(ET.tostring(photos, encoding='utf8', method='xml'), "html.parser")
	possibilities = soup.find_all('photo')
	
	for p in possibilities:
		tag = p.has_attr('url_c')
		if tag:
			photo_list.append(p)
		

	#print photo_list
	p_shuffle = shuffle(photo_list)
	p_choice = choice(photo_list)
	p_url = p_choice['url_c']
	p_id = p_choice['id']
	p_owner = p_choice['owner']

	p_weburl = "https://www.flickr.com/photos/" + p_owner + "/" + p_id
	#print p_weburl 


	urllib.urlretrieve(p_url, "image.jpg")
	
	return p_weburl
	    

def twitter():
	auth = tweepy.OAuthHandler(TWITTER_KEY, TWITTER_SECRET)
	auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

	api = tweepy.API(auth)
	status = flickr()
	media = 'image.jpg'
	api.update_with_media(media, status=status)

def main():
	while 1:
		print('Looking for pictures on Flickr')
		#flickr()
		print('Picked a cool satay image')
		twitter()
		print('Posted the image to Twitter')
		time.sleep(900)

if __name__ == "__main__":
	main()
