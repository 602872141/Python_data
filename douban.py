import json

import requests
import re

import xlwt
from pyquery import PyQuery as pq




import pymongo
class douban(object):
    def __init__(self):
        self.headers={  'Referer': 'https://movie.douban.com/subject/26752088/comments?start=20&limit=20&sort=new_score&status=P',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest',
                         'Cookie': 'bid=RjgjuBU-PTo; gr_user_id=ae9e94cc-7e02-4024-b3c4-0c2caffc26a1; viewed="27622170"; _vwo_uuid_v2=D3F88C3DBDF94F35B396A97C6A054F9A3|adba2ea65b5ec1f785bc5486017dab5e; ll="118296"; __yadk_uid=2wMpt1WH6XwwDku0qk9TL31mVzCzI834; ct=y; ap=1; ps=y; dbcl2="181209032:Y2c8KOeBGDM"; push_noty_num=0; push_doumail_num=0; ck=hZvX; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1531710788%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DQsYSu5ExScM-SJWiaYJrHE25Eby3911Q4-pc_s7IPc20ZvFLA8nU-AnTXkBLy6b6%26wd%3D%26eqid%3De45bbdfb0000feed000000065b4c0d41%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.904684027.1526545285.1531659187.1531710788.8; __utmc=30149280; __utmz=30149280.1531710788.8.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utma=223695111.1210195025.1531210856.1531659187.1531710788.7; __utmb=223695111.0.10.1531710788; __utmc=223695111; __utmz=223695111.1531710788.7.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1531710788; _pk_id.100001.4cf6=cae95a155b0ad340.1531210856.7.1531710980.1531659213.'
                        }
        self.url='https://movie.douban.com/subject/26752088/comments?start={start}&limit=20&sort=new_score&status=P&comments_only=1'
    def start_request(self,start):


        url=self.url.format(start=start)
        response = requests.get(url=url)
        print(response.status_code)
        if response.status_code==200:
            return response.text
        else:
            proxy=self.get_proxy()
            proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
            response4 = requests.get(url, allow_redirects=False,proxy=proxies)

            print(response4.status_code)
            if response4.status_code == 200:
                return response4.text
    def get_proxy(self):
        PROXY_URL = 'http://127.0.0.1:5555/random'

        try:
            response=requests.get(PROXY_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    def get_Message(self,html):
        print(html)
        json_loads = json.loads(html)
        # doc = pq(html)
        # for item in doc('#comments .coment-item').items():
        #     Message={
        #          'name': item.find('.avatar a').arrt('title'),
        #          'like':item.find(".comment .comment-vote .votes").text()+'点赞',
        #          'text':item.find('p .short').text()
        #         }
        #     print(Message)
        pattern = re.compile('<div class="avatar">(.*?)<div class="comment-item" data-cid=".*?', re.S)
        findall = re.findall(pattern, str(json_loads))
        for result in findall:
            # print(re.findall('<a title="(.*?)" href=.*?',result,re.S))
            # print(re.findall('span class="votes">(\d*)</span>*?', result, re.S)+re.findall('<a href="javascript:;" class="j a_show_login" onclick="">(.*?)</a>.*?',result,re.S))
            # print(re.findall('<span class="short">(.*?)</span>.*?',result,re.S))
            Message={
                'name':re.findall('<a title="(.*?)" href=.*?',result,re.S),
                'like':re.findall('span class="votes">(\d*)</span>*?', result, re.S)+re.findall('<a href="javascript:;" class="j a_show_login" onclick="">(.*?)</a>.*?',result,re.S),
                'text':re.findall('<span class="short">(.*?)</span>.*?',result,re.S)
            }
            # new_workbook = xlwt.Workbook()
            # new_sheet = new_workbook.add_sheet("yaosheng")
            # name=re.findall('<a title="(.*?)" href=.*?',result,re.S)
            # new_sheet.write(number, 0, str(name))
            # new_sheet.write(number, 0, 'like:' + re.findall('span class="votes">(\d*)</span>*?', result, re.S)+re.findall('<a href="javascript:;" class="j a_show_login" onclick="">(.*?)</a>.*?',result,re.S))
            # new_sheet.write(number, 0, 'text:' + re.findall('<span class="short">(.*?)</span>.*?',result,re.S))
            # if number==2000:
            #     new_workbook.save(r"douban.xls")

            print(Message)

            self.go_mongodb(Message)
    def go_mongodb(self,Message):
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.douban
        self.db.yaosheng.insert(Message)


    def main(self):
         for i in range(24,480):
            html = self.start_request(i*20)
            self.get_Message(html)

if __name__=='__main__':
    douban=douban()
    douban.main()