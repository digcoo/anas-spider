# encoding=utf8  

import time
import urllib2
import traceback
import jsonpickle
import json
from bs4 import BeautifulSoup
import Geohash
from MysqlClient import *

from HttpUtils import *

def get_item_category():
    try:
	base_url = 'https://pages.tmall.com/wow/chaoshi/act/category?wh_logica=HD&wh_callback=__chaoshi_category'
	content = HttpUtils.get(base_url, {}, 'utf-8')
	target_content = content[content.find('__chaoshi_category(') + len('__chaoshi_category(') : content.find(')')]
	json_array = jsonpickle.decode(target_content).get('data')
	categorys = []
	for json_obj in json_array:
	    categorys.append({'name' : json_obj.get('name'), 'link' : json_obj.get('link')})
	return categorys

    except Exception, e:
	traceback.print_exc()

    return None

def get_page_item_photos(url):
    try:
	print url
	headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"

	content = HttpUtils.get(url, headers, 'utf-8')
	print content
	soup = BeautifulSoup(content, "lxml")
	lis = soup.find(id="J_ProductList").find_all("li", "product")
	if lis is not None and len(lis) > 0:
	    item_photos = []
	    for li in lis:
		small_photo = li.find_all("div", "product-img")[0].find_all("img")[0]["src"]
		big_photo = small_photo.replace("160x160", "400x400")
		title = li.find_all("h3", "product-title")[0].get_text()
		item_photos.append({"title":title, "small_photo":small_photo, "big_photo":big_photo})
	    return item_photos
    except Exception, e:
	traceback.print_exc()
    return None

def get_all_item_photos(url):
    try:
	print ''
    except Exception, e:
        traceback.print_exc()
    return None


categorys = get_item_category()
print json.dumps(categorys, ensure_ascii=False,indent=4)

for category in categorys:
    category_name = category.get('name')
    category_link = category.get('link')
    item_photos = get_page_item_photos('https:' + category_link)
    print len(item_photos)
    break

