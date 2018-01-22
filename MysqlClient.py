#encoding=utf-8

import pymysql.cursors
import datetime
import time
import traceback
import jsonpickle

class MysqlClient:

    __instance = None

    @staticmethod
    def get_instance():
        if MysqlClient.__instance is None:
            MysqlClient.__instance = MysqlClient()
        return MysqlClient.__instance

    def __init__(self):
	self.connection = None

    def conn(self):
        try:
            self.connection = pymysql.connect(host='47.100.53.10',
                             user='root',
                             password='Root123!',
                             db='anas',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        except Exception, e:
            traceback.print_exc()

    def close(self):
	try:
#	    self.connection.close()
	    print ''
	except Exception, e:
	    traceback.print_exc()


#=================================================shop================================================================

    def add_shop(self, shop):
        try:

	    if shop.get('shop_id') is not None:
		local = self.query_by_user_id(shop.get('shop_id'))
		print local
		if local is not None and len(local) > 0:
		    return None

	    self.conn()
            with self.connection.cursor() as cursor:
                sql = "INSERT INTO `digcoo_anas_shop` (`user_id`, `name`, `picture`, `tel`, `addr`, `open_mobile`, `business_id`, `lat`, `lng`, `geohash`, `follow_num`, `status`, `logo`, `create_date`, `update_date`) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now())"
		cursor.execute(sql, (shop['shop_id'], shop['shop_full_name'], 'http://img.91jm.com/2013/06/D0HEB7XWLR2X.jpg', shop['shop_tel'], shop['shop_addr'], 1, 2, shop['shop_lat'], shop['shop_lng'], shop['shop_geohash'], 99, 1, shop['shop_logo'], ))
                self.connection.commit()

        except Exception, e:    
	    traceback.print_exc()
	finally:
	    self.close()


    def query_by_user_id(self, user_id):
	try:
	    self.conn()
	    with self.connection.cursor() as cursor:
		query_sql = "select `id` from `digcoo_anas_shop` where `user_id` = " + str(user_id)
		cursor.execute(query_sql)
                return cursor.fetchall()

	except Exception, e:
	    traceback.print_exc()
	finally:
	    self.close()

	return None
