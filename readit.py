import json
import urllib, json, urllib
import random
import re, time
from config_utils import get_configs


reddit_url = 'https://www.reddit.com/r/aww/hot.json'
old_time = int(time.time())
def check_time():
	global old_time
	if not old_time:
		old_time = int(time.time())
		return True
	configs = get_configs()
	time_conf = int(configs['redditrefreshrate'])
	
	current_time = int(time.time())
	diff = current_time - old_time
	old_time = current_time
	if diff > time_conf:
		print("REFRESHING")
		return True
	return False

def get_image_url(url, regex='http(s)*://(i\.)*imgur\.com/.+\..+', ending='.jpg', cache=True):
	current_time = (int)(time.time())
	configs = get_configs()
	if check_time():
		cache = False
	cache = True
	if cache:
		with open('cache.txt') as f:
			data = f.read()
		data = json.loads(data)

	else:
		response = urllib.urlopen(url)
		data = json.loads(response.read())
		if data['data']['children']:
			with open('cache.txt', 'w') as f:
				f.write(data)


	data = data['data']['children']
	print(len(data))
	r = random.randint(0, len(data))-1

	imageurl = data[r]['data']['url']
	imageurl = re.sub('/gallery', '', imageurl)
	imageurl = re.sub('.gifv', '.jpg', imageurl)
	if re.match(regex, imageurl):
		return imageurl
	else:
		imageurl = imageurl + '.jpg'
		if re.match(regex, imageurl):
			return imageurl
		else:
			print(imageurl)
			return get_image_url(url)

print(get_image_url(reddit_url))
