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

base_url = 'http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84/p{0}?aid=20245884%2C6212826%2C15998012'

def get_shop_list(url):
    try:
        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        headers["Referer"] = "http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84/p1?aid=20245884%2C6212826%2C15998012"
        headers['Cookie'] = '_lxsdk_cuid=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; _lxsdk=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; cy=1; cye=shanghai; _hc.v=0f32a3b6-7385-0888-333e-5c3045e7cad3.1515161390; s_ViewType=10; aburl=1; wed_user_path=27760|0; __mta=251920054.1515203025830.1515203025830.1515203025830.1; _lxsdk_s=160c901323c-8b8-3a9-dad%7C%7C218'

        content = HttpUtils.get(url, headers, 'utf-8')
	print content
        shop_list = parse_shop_list_html_page(content)
        return shop_list
    except:
        traceback.print_exc()
    return None

#parse 商铺列表页面
def parse_shop_list_html_page(content):
    try:
        soup = BeautifulSoup(content, "lxml")
        shop_all_list = soup.find(id="shop-all-list").find_all("li")
        if shop_all_list is not None:
            shops = []
            for shop_item in shop_all_list:
                shop_info = {}
#                logo_url = shop_item.find_all("div", "pic")[0].find_all("img")[0]['data-src'].strip()
#                shop_name = shop_item.find_all("div", "txt")[0].find_all("div", "tit")[0].find_all("a")[0].get_text().strip()
#                shop_url = shop_item.find_all("div", "txt")[0].find_all("div", "tit")[0].find_all("a")[0]["href"].strip()
                shop_avg = shop_item.find_all("div", "txt")[0].find_all("div", "comment")[0].find_all("a")[1].find_all("b")[0].get_text().strip()
                shop_type = shop_item.find_all("div", "txt")[0].find_all("div", "tag-addr")[0].find_all("a")[0].get_text().strip()
                shop_dist = shop_item.find_all("div", "txt")[0].find_all("div", "tag-addr")[0].find_all("a")[1].get_text().strip()
#                shop_addr = shop_item.find_all("div", "txt")[0].find_all("div", "tag-addr")[0].find_all("span", "addr")[0].get_text().strip()
#                shop_group_buys_map = parse_groupon_list(shop_item)
                shop_info = {
#			     "logo":logo_url,
#                            "name":shop_name.encode('utf8'),
                             "url":shop_url,
                            "avg":shop_avg,
                            "type":shop_type,
                            "dist":shop_dist
}

#                shop_expand_info = get_shop_detail_info1(shop_url) if get_shop_detail_info1(shop_url) is not None else get_shop_detail_info2(shop_url)
		shop_expand_info = get_shop_detail_info1(shop_url)
                if shop_expand_info is not None:
                    shop_info.update(shop_expand_info)

		MysqlClient.get_instance().add_shop(shop_info)

                shops.append(shop_info)
                time.sleep(5)
                # print jsonpickle.encode(shops)
#                break

            return shops
    except:
        traceback.print_exc()

    return None

#parse 团购html块
def parse_groupon_list(soup):
    try:
        shop_group_buys_list = []
        if soup.find_all("div", "svr-info") is not None and soup.find_all("div", "svr-info")[0].find_all("div", "si-deal") is not None:
            shop_group_buys = soup.find_all("div", "svr-info")[0].find_all("div", "si-deal")[0].find_all("a")
            for shop_group_buy in shop_group_buys:
                shop_group_buy_url = shop_group_buy['href'].strip()
                shop_group_buy_title = shop_group_buy.get_text().strip()
                if shop_group_buy_url.find("javascript") < 0:
                    shop_group_buys_list.append({"url": shop_group_buy_url, "title": shop_group_buy_title})

        return shop_group_buys_list
    except Exception, e:
        traceback.print_exc(e)

#商铺详情页面1
def get_shop_detail_info1(url):
    try:
        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        headers["Referer"] = "http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84/p1?aid=20245884%2C6212826%2C15998012"
        headers['Cookie'] = '_lxsdk_cuid=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; _lxsdk=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; cy=1; cye=shanghai; _hc.v=0f32a3b6-7385-0888-333e-5c3045e7cad3.1515161390; s_ViewType=10; aburl=1; wed_user_path=27760|0; __mta=251920054.1515203025830.1515203025830.1515203025830.1; _lxsdk_s=160c901323c-8b8-3a9-dad%7C%7C218'

        content = HttpUtils.get(url, headers, 'utf-8')
	print content

        soup = BeautifulSoup(content, "lxml")
#        shop_expand_addr = soup.find(id="basic-info").find_all("div", "address")[0].find_all("span", "item")[0].get_text().strip()

	#tel
        shop_expand_tel = soup.find(id="basic-info").find_all("p", "tel")[0].find_all("span", "item")[0].get_text().strip()

	#open_time
	shop_expand_open = ''
	infos = soup.find(id="basic-info").find_all("div", "other")[0].find_all("p", "info")
	if infos is not None and len(infos) > 0:
	    for info in infos:
		text = info.find_all("span", "info-name")[0].get_text().encode('utf-8')
		if text.find('时间') > 0:
		    shop_expand_open = info.find_all("span", "item")[0].get_text().strip()
		    break

	#photo
	photo_url = 'http://www.dianping.com/ajax/json/shopDynamic/shopTabs?shopId=90951360&cityId=1&shopName=Regiustea%E5%A4%A9%E5%BE%A1%E7%9A%87%E8%8C%B6&power=5&mainCategoryId=244&shopType=10&shopCityId=1&_token=eJxVTt1ugjAYfZdeN9ACbYHEC3WOieKGMowzXiAwJEAtlAx12buvJu5iyZecn%2B%2Bc5HyDbp4BFyOELAzBV94BF2ANaRRA0Ev1IZgSzBgxqGNBkP73mG1CcOziJ%2BDuiYMgNenhbqyV3mPDRtBG6AAVNShkjB2gYam7Z%2BYqAk59L1xdH4ZBy8qEi5IXWnpudHk6C91BDsEmRWoJUI0mUg2F1QOTB%2FZ%2FOlDTVVaWBVcs9y%2FRRlqy%2FVwHMorfr8gMbi%2Br1%2BWsXt2u9nS6Lj%2BaRRETP%2BfPfZO0p5iTSWoNzmbyOpt6YufVbeJdmtDbMZLvGuN8rP0238YirURnZQFfCF1u34Qe663PPVxQsZwXODuG4bgaR3Ul8nA0Aj%2B%2FFDJm5g%3D%3D&uuid=40e49af0-9fce-a1c6-0e90-dbacb64cb3cb.1516376513&platform=1&partner=150&originUrl=http%3A%2F%2Fwww.dianping.com%2Fshop%2F90951360'
	shop_style_photos = []

        #map
        shop_extra = {}
	if content.find("window.shop_config") > -1:
	    js_str_start = content.find("window.shop_config")
	    js_str_suf = content[js_str_start:]
	    js_str_start = js_str_suf.find("{")
	    js_str_end = js_str_suf.find("</script>")
	    js_str = js_str_suf[js_str_start : js_str_end]
	    json_obj = jsonpickle.decode(js_str)
	    shop_extra['shop_name']  = json_obj['shopName']
	    shop_extra['shop_addr']  = json_obj['address']
	    shop_extra['shop_id'] =  json_obj['shopId']
	    shop_extra['shop_full_name'] =  json_obj['fullName']
	    shop_extra['shop_lat'] = json_obj['shopGlat']
	    shop_extra['shop_lng'] = json_obj['shopGlng']
	    shop_extra['shop_type'] = json_obj['shopType']
	    shop_extra['shop_first_category'] = json_obj['categoryName']
	    shop_extra['shop_second_category'] = json_obj['mainCategoryName']
	    shop_extra['shop_logo'] = json_obj['defaultPic'][:json_obj['defaultPic'].find('.jpg')+4]
	    shop_extra['shop_geohash'] = Geohash.encode(float(json_obj['shopGlat']), float(json_obj['shopGlng']), 8) 
	shop_extra['shop_tel'] = shop_expand_tel
	shop_extra['shop_open'] = shop_expand_open
	shop_extra['shop_photos'] = shop_style_photos

	return shop_extra
	
    except Exception, e:
        traceback.print_exc(e)
        print url
    return None

#商铺详情页面样式2
def get_shop_detail_info2(url):
    try:
        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
        headers["Referer"] = "http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84/p1?aid=20245884%2C6212826%2C15998012"
        headers['Cookie'] = '_lxsdk_cuid=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; _lxsdk=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; cy=1; cye=shanghai; _hc.v=0f32a3b6-7385-0888-333e-5c3045e7cad3.1515161390; s_ViewType=10; aburl=1; wed_user_path=27760|0; __mta=251920054.1515203025830.1515203025830.1515203025830.1; _lxsdk_s=160c901323c-8b8-3a9-dad%7C%7C218'

        content = HttpUtils.get(url, headers, 'utf-8')
        soup = BeautifulSoup(content, "lxml")
        shop_expand_addr = soup.find(id="J_boxDetail").find_all("div", "shop-addr")[0].find_all("span")[0].get_text().strip()

        #tel
        shop_expand_tel = ''
        tel_ps = soup.find(id="J_boxDetail").find_all("div", "shopinfor")[0].find_all("p")
        if tel_ps is not None and len(tel_ps) > 0:
            for tel_p in tel_ps:
                if tel_p.get_text().find("电话") > -1:
                    shop_expand_tel = tel_p.find_all("span")[0].get_text().strip()

        #open_time
        shop_expand_open = soup.find(id="J_boxDetail").find_all("div", "more-class")[0].find_all("p")[0].find_all("span")[0].get_text().strip()

        return {"expand_addr" : shop_expand_addr, "tel" : shop_expand_tel, "open_time" : shop_expand_open}
    except Exception, e:
        traceback.print_exc(e)
        print url
    return None


# get_shop_list("http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84%E9%BE%99%E4%B9%8B%E6%A2%A6/p1")
'''
for index in range(1, 1000):
    url = base_url.format(index)
    shop_page_list = get_shop_list(url)
    print json.dumps(shop_page_list, ensure_ascii=False,indent=2)
#     time.sleep(10)
    break
'''
# print jsonpickle.encode(get_shop_detail_info2("http://www.dianping.com/shop/6212826"))
print json.dumps(get_shop_detail_info1("http://www.dianping.com/shop/17985960"), ensure_ascii=False,indent=2)

shop_info = get_shop_detail_info1("http://www.dianping.com/shop/17985960")
MysqlClient.get_instance().add_shop(shop_info)
