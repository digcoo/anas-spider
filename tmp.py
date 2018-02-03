# encoding=utf8  
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import copy
import time
import urllib2
import traceback
import jsonpickle
import json
from bs4 import BeautifulSoup
import Geohash
from MysqlClient import *

from HttpUtils import *
from FileUtils import *

#base_url = 'http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84/p{0}?aid=20245884%2C6212826%2C15998012'
base_url = 'http://www.dianping.com/search/keyword/1/10_%E6%A1%82%E6%9E%97%E8%B7%AF/p{0}'

headers = {}
headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36"
headers["Referer"] = "http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84/p1?aid=20245884%2C6212826%2C15998012"
headers["Cookie"] = 'cy=1; cityid=1; cye=shanghai; aburl=1; cy=1; cye=shanghai; _lxsdk_cuid=1615b98491fc8-06bee841b104dd-4323461-100200-1615b98491f7c; _lxsdk=1615b98491fc8-06bee841b104dd-4323461-100200-1615b98491f7c; _hc.v="\"861aac4a-b627-48c2-bc7c-3402f9f3923b.1517660078\""; s_ViewType=10; Hm_lvt_dbeeb675516927da776beeb1d9802bd4=1517666028; Hm_lpvt_dbeeb675516927da776beeb1d9802bd4=1517666028; __mta=145576587.1517666031604.1517666031604.1517666031604.1; wed_user_path=1191|0; _lxsdk_s=1615bd927ce-32-f24-1f2%7C%7C16'

#商铺详情页面1
def get_shop_detail_info1(url):
    try:
        content = HttpUtils.get(url, headers, 'utf-8')
	print content
        soup = BeautifulSoup(content, "lxml")
#        shop_expand_addr = soup.find(id="basic-info").find_all("div", "address")[0].find_all("span", "item")[0].get_text().strip()

	#tel
	shop_expand_tel = ''
	if len(soup.find(id="basic-info").find_all("p", "tel")) > 0 and len(soup.find(id="basic-info").find_all("p", "tel")[0].find_all("span", "item")) > 0:
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
        print 'exception : ' + url
    return None

#商铺详情页面样式2
def get_shop_detail_info2(url):
    try:
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
#        traceback.print_exc(e)
        print url
    return None

def get_shop_id_list(url):
    try:
	content = HttpUtils.get(url, headers, 'utf-8')
	start = content.find('brandList') + len('brandList') + 1
	target_brands_str = content[start : ]
	end = start + target_brands_str.find(']') + 1
	ids = []
	json_array = jsonpickle.decode(content[start : end])
	for i in range(0, len(json_array)):
	    ids.append(json_array[i].get('id'))
	return ids

    except Exception, e:
	traceback.print_exc()
    return None



# print jsonpickle.encode(get_shop_detail_info2("http://www.dianping.com/shop/6212826"))
#print json.dumps(get_shop_detail_info1("http://www.dianping.com/shop/17985960"), ensure_ascii=False,indent=2)

#shop_info = get_shop_detail_info1("http://www.dianping.com/shop/17985960")
#MysqlClient.get_instance().add_shop(shop_info)

shop_ids = get_shop_id_list('http://www.dianping.com/shop/4600410')
print jsonpickle.encode(shop_ids)
#shop_ids = [4619365, 9027818, 5441863, 18340046, 4698384, 5165991, 5321259, 18339562, 90943549, 5279943, 79488371, 82620601, 8010491, 6636134, 5345442, 5141088, 19701153, 5164689, 95679722, 6037506, 13763694, 72441676, 24619883, 78978734, 6858857, 23091824, 8009996, 77358221, 49420192, 92549664, 72459376, 77358557, 77255540, 5520216, 77354393, 92678979, 92508843, 33508084, 19112878, 98452845, 79272347, 83247636, 91689747, 4698402, 77358417, 16715583, 21575561, 77354640, 76764167, 80671556, 5355844, 92328200, 81316061, 49119956, 83327249, 77492667, 57543758, 16978740, 77358585, 67191419, 22132769, 75175751, 67392092, 8848222, 18242874, 4619011, 93536844, 77358165, 67004261, 5443954, 5281183, 66070562, 77358321, 5432596, 91919801, 96683316, 23149737, 83130218, 98452888, 82980740, 83363438, 77358480, 77358381, 37943422, 81482456, 4698364, 68107295, 5320024, 5172076, 77354907, 49927799, 66838904, 5165953, 35512165, 77354517, 18210180, 82953833, 77358456, 97231797, 5636065, 81190028, 79246380, 98453914, 9965204, 5491057, 5432629, 83170934, 8998933, 74610791, 82166093, 22689086, 83049719, 91591811, 42345636, 23220912, 69585903, 18228879, 5166007, 5307235, 5381419, 21875288, 5172088, 20859629, 93485460, 97482834, 94787400, 63902719, 95021703, 80970830, 82730366, 50445984, 83302982, 73408340, 13925762, 58844183, 6102709, 5456191, 73969883, 92341505, 83127419, 26233182, 58208387, 58331210, 18210116, 93317551, 5387252, 77358583, 77358226, 77460424, 24788425, 98454239, 80963358, 43611638, 82423014, 93186304, 5700857, 98453489, 17960438, 77355904, 77358196, 66623904, 98454257, 98453579, 97817996, 9775389, 58605165, 74623332, 69657346, 5235698, 5093885, 73149099, 5636129, 23993596, 67648450, 77358514, 80890656, 97566074, 71740542, 18094073, 18210341, 19467836, 97281098, 4698371, 74623338, 98453144, 81785148, 77355067, 24070957, 98453984, 98453018, 58478769, 22269922, 13877002, 69560107, 67008469, 77358280, 5321249, 77131336, 98454476, 98453147, 70357728, 98454182, 77355565, 82903485, 72458166, 69115168, 18478025, 92369659, 6183218, 5460332, 21877804, 5636180, 49056966, 5165945, 49501617, 5718257, 5115647, 5451806, 26954618, 6212826, 13863949, 77358157, 77358430, 66893061, 5164676, 77355844, 18478238, 67440079, 13765120, 18068408, 96722081, 4698389, 4698374, 77358496, 82699311, 77358526, 92832832, 5518121, 77355451, 9000792, 72458250, 27332024, 22895381, 66256690, 5291874, 97175041, 5424825, 82182799, 98454231, 97173496, 98454048, 98454246, 18008287, 27381414, 38052062, 5636163, 5273694, 79151513, 77355041, 27314106, 67437135, 18181672, 80634025, 23603723, 76070367, 4698393, 77355599, 72458956, 11571898, 79614395, 4296270, 18393976, 5172081, 27339105, 24267878, 5313927, 69277238, 5172078, 5281905, 8890388, 98148963, 67861251, 81366400, 68174190, 62315672, 82709956, 13714413, 71333447, 19352529, 5319996, 80200868, 77154956]
err_ids = []
rema_ids = copy.deepcopy(shop_ids)

suc_shops = []

'''
for shop_id in shop_ids:
    url = 'http://www.dianping.com/shop/' + str(shop_id)
    rema_ids.remove(shop_id)
    print 'rema:' + jsonpickle.encode(rema_ids)
#    print url
    shop_info = get_shop_detail_info1(url)
    if shop_info is None:
	shop_info = get_shop_detail_info2(url)
	if shop_info is None:
	    print 'no data : ' + str(shop_id)
	    err_ids.append(shop_id)
	    time.sleep(10)
	    continue
    try:
	target_shop_info = { your_key: shop_info[your_key] for your_key in ['shop_geohash', 'shop_logo', 'shop_lat', 'shop_lng', 'shop_tel', 'shop_name', 'shop_second_category', 'shop_id', 'shop_addr', 'shop_first_category'] }

	FileUtils.list_to_csv([list(target_shop_info.viewvalues())], '/home/ubuntu/digcoo/anas-spider/shops_data', 'xinzhuang_longzhimeng_' + str(shop_id) + '.csv')

    except Exception, e:
#	traceback.print_exc()
	print 'no data : ' + str(shop_id)
        err_ids.append(shop_id)

#    suc_shops.append(list(target_shop_info.viewvalues()))

    time.sleep(10)
#    break

#FileUtils.list_to_csv(suc_shops, '/home/ubuntu/digcoo/anas-spider/shops_data', 'xinzhuang_longzhimeng.csv')
print jsonpickle.encode(err_ids)
'''
print get_shop_detail_info1('http://www.dianping.com/shop/18340046') 
