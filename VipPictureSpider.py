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

'''
categorys = get_item_category()
print json.dumps(categorys, ensure_ascii=False,indent=4)

for category in categorys:
    category_name = category.get('name')
    category_link = category.get('link')
    item_photos = get_page_item_photos('https:' + category_link)
    print len(item_photos)
    break
'''

#print get_page_item_photos('https://list.tmall.com/search_product.htm?spm=a3204.7084713.1996500281.1.YTOuRF&user_id=725677994&cat=51454011&active=1&style=g&acm=lb-zebra-27092-331834.1003.4.457096&sort=td&scm=1003.4.lb-zebra-27092-331834.OTHER_14434945515601_457096&industryCatId=51462017#J_Filter')

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
headers["Referer"] = "http://category.vip.com/search-2-0-34.html?q=3|29810||&rp=30071|29733"
headers["Cookie"] = "vip_rip=180.166.27.254; vip_address=%257B%2522pname%2522%253A%2522%255Cu4e0a%255Cu6d77%255Cu5e02%2522%252C%2522cname%2522%253A%2522%255Cu4e0a%255Cu6d77%2522%252C%2522pid%2522%253A%2522103101%2522%252C%2522cid%2522%253A%2522103101101%2522%257D; vip_province=103101; vip_province_name=%E4%B8%8A%E6%B5%B7%E5%B8%82; vip_city_name=%E4%B8%8A%E6%B5%B7; vip_city_code=103101101; vip_wh=VIP_SH; tmp_mars_cid=1517462384176_2db927c8fa6f4e126723a275d141f857; user_class=a; VipUINFO=luc%3Aa%7Csuc%3Aa%7Cbct%3Ac_new%7Chct%3Ac_new%7Cbdts%3A0%7Cbcts%3A0%7Ckfts%3A0%7Cc10%3A0%7Crcabt%3A0%7Cp2%3A0%7Cp3%3A1%7Cp4%3A0%7Cp5%3A0; mars_pid=0; mars_sid=014ad273fed59d4ba6c2775a6d773eac; visit_id=8A6597017574CD8A6D11268CEC9DEA61; _smt_uid=5a72a3dd.4c330ad5; _jzqco=%7C%7C%7C%7C%7C1.388757318.1517462493164.1517464279050.1517464468459.1517464279050.1517464468459.0.0.0.17.17; mars_cid=1517462384176_2db927c8fa6f4e126723a275d141f857"

print HttpUtils.get('http://category.vip.com/ajax/mapi.php?service=product_info&callback=categoryMerchandiseInfo1&productIds=397162302%2C402479499%2C397084450%2C316878392%2C395919709%2C210917217%2C395919238%2C403361638%2C403298168%2C349448091%2C399967286%2C383762945%2C402479496%2C395919666%2C397084538%2C395919452%2C383762895%2C398672612%2C180935108%2C401226617%2C180935500%2C399967850%2C404310643%2C402479617%2C374176968%2C399970118%2C323336922%2C403298126%2C397084451%2C403283092%2C394130257%2C376104993%2C402280084%2C399967465%2C399967586%2C395919727%2C357314891%2C397084422%2C402479571%2C334123470%2C397084426%2C383762928%2C399969685%2C395919541%2C396251399%2C395919522%2C404138003%2C349310491%2C399969871%2C399967380&functions=brandShowName%2CsurprisePrice%2CpcExtra&warehouse=VIP_SH&mobile_platform=1&app_name=shop_pc&app_version=4.0&mars_cid=1517462384176_2db927c8fa6f4e126723a275d141f857&fdc_area_id=103101101&_=1517467667887', headers, 'utf-8')
print len(HttpUtils.get('http://category.vip.com/search-2-0-3.html?q=1|29810||&rp=30071|29733', headers, 'utf-8'))
