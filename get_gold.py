#coding=utf-8
#__author__ = wanghan
import requests
import re
import urllib, urllib2
import json
import time

class Let_Us_Get_Gold():

    def get_news_data(self):
        news_url = 'http://api2.souyue.mobi/d3api2/webdata/channel.groovy'
        sy_news_data = {
            "category":"11225",
            "lastId":"0",
            "token":"",
            "vc":"5.0.2"
        }
        news_decode = urllib.urlencode(sy_news_data)
        news_req = urllib2.Request(url = news_url,data = news_decode)
        # news_req.add_header('Accept-Encoding','gzip')
        news_req.add_header('User-Agent','Android')
        news_json = urllib2.urlopen(news_req)
        news_json_data = json.loads(news_json.read())
        news_body_data = news_json_data['body']
        return news_body_data

    def get_gold(self, news_body_data, wx_username, sy_c):
        geturl = 'http://m.zhongsou.com/newsdetail/goldAuthorization'
        for x in xrange(9):
            keyword = news_body_data[x]['keyword']
            srpId = news_body_data[x]['id']
            url = news_body_data[x]['url']
            title = news_body_data[x]['title']
            newsurl = 'http://m.zhongsou.com/newsdetail/index?' \
                      'keyword=%s&' \
                      'srpId=%s&' \
                      'url=%s&' \
                      'sy_c=%s&' \
                      'isSub=1' % (keyword, srpId, url, sy_c)
            print newsurl
            wx_news_data = requests.get(newsurl)
            try:
                golddata = ''.join(re.findall(r'{"[a-zA-Z0-9].*}', wx_news_data.content))
                valiCode = json.loads(golddata)['valiCode']
                goldNum = json.loads(golddata)['goldNum']
                data = {
                    'md5url' : url,
                    'preurl' : newsurl,
                    'userId' : 'null',
                    'userName' : wx_username,
                    'valiCode' : valiCode
                }
                for n in xrange(int(goldNum)):
                    time.sleep(5)
                    res = requests.post(url=geturl, data=data)
                    print res.content, '文章标题：',title
            except Exception,e:
                print "您已获得", title, e

if __name__ == '__main__':
    wx_username = "WX翰子3036"
    sy_c = "1rMGkGis188LLXo4YSB88u4B8qnlxTKaoYnqdzpmaV7MrXH3k9b7HS9kxDFzs8T%2F%2B45uDk2J3Qr%2FbIE07x5rhKJTuh7nfbZ%2B%2B6yptAMQR%2Fveumxyo3K%2FhvJa8KvqfH01qpLufmWZ2wkWekQ1c9lpRexIoGjmPCpyhjcBK6BDbi%2BMZJ3qmxNu8TqwVoIRefNnPmirRgopIsCjcSUP8P0UfYcgdhMFREwvYFvjBi4mBb9%2FPZaQxBuVToU%3D+"
    news_body_data = Let_Us_Get_Gold().get_news_data()
    Let_Us_Get_Gold().get_gold(news_body_data, wx_username, sy_c)



# 金币查看界面
# https://zspay.zhongsou.com/coin/mypurse?sy_c=1Q05HLpDk5Bi45V%2FlrWChWqI%2B9nJRFOoEEzrCTqMKep%2BKtlHyrnTDHOLtGSUL%2F7GPMgT9mvLAvRzJb70Ak0XIMcLuDATV6yu%2FHzQFjhzUdOcPYz%2F4OFsRRimtNMG%2F%2FI2bPhNJ%2FSj3Eq3lgBBY8%2B05A70p5XajisNEn5ZLsi8w4OgcOfbUOZVT2Sj1QzRuSjvKESBxIqTq1DT72aTUV4rfPNQP6HUtHHdvJ3WqV1MNfcTftjmIu54YZ8%3D+

        # http://m.zhongsou.com/newsdetail/index?
        # keyword=电商&
        # srpId=5898209&
        # url=http://business.sohu.com/20151120/n427263268.shtml&
        # sy_c=1WRYGkQLAE50KnRILYrQbaRZjM4avVaUEovqk1lcLfyNtYGA85 9Y9Rv0XX/UXWYUiwpgxuS7XK3GuRABQDzRdRrUskNLn0RoaCkbLXfTX9AZv11xkq3LMcVc wFSxin5KOqU30ubuTn 6sY nlx7stmS963h1KCveR/u7Kqc3eEYi8hb12G5I5vrSqhCKsnkkCTEoMsBxTAk SDW/pXomf2aZKsIMo3WRl8CcBGhqE93pC0Ky45XHo= &
        # isSub=1
