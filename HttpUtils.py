# encoding=utf-8
import urllib2
import traceback
import jsonpickle

class HttpUtils:

    @staticmethod
    def get(url, headers, charset):
        response = None
        try:
            req = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(req)
            # req = urllib2.Request(url)
            # req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
            # req.add_header("Referer", "http://www.dianping.com/")
            # response = urllib2.urlopen(req)
            buf = response.read()
            return buf.decode(charset)
        except Exception, e:
            if hasattr(e, 'code'):
                print('get url = %s, return_code=%s, reason = %s' % (url, e.code, e.reason))
                if e.code == 404:
                    return ''
            return None
        finally:
            if response is not None:
                response.close()


if __name__ == '__main__':
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
    headers["Referer"] = 'http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84%E4%BB%B2%E7%9B%9B'
    headers['Cookie'] = '_lxsdk_cuid=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; _lxsdk=160c6a7a179c8-02393e4445bc62-b7a103e-100200-160c6a7a179c8; cy=1; cye=shanghai; _hc.v=0f32a3b6-7385-0888-333e-5c3045e7cad3.1515161390; s_ViewType=10; aburl=1; wed_user_path=27760|0; __mta=251920054.1515203025830.1515203025830.1515203025830.1; _lxsdk_s=160c901323c-8b8-3a9-dad%7C%7C218'
    url = 'http://www.dianping.com/search/keyword/1/0_%E8%8E%98%E5%BA%84%E4%BB%B2%E7%9B%9B/p2?aid=23982023%2C6212826%2C15998012'

    text = HttpUtils.get(url, headers, 'utf-8')
    print text
