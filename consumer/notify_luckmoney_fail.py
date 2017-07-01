# -*- coding: utf-8 -*-
import json
import MySQLdb as mdb
from util.memcache_util import Client
import config
import requests

con = mdb.connect('127.0.0.1', 'xiaob', 'skdfjkasdf', 'xiaob')
con.ping(True)
cur = con.cursor()
client = Client(config.prefix)
url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='

def handler(message):
    try:
	print message.body
        content = json.loads(message.body)
    except:
        return True
    access_token = client.get('access_token')
    if not access_token:
        cur.execute("SELECT v from server_config where k = 'access_token' and name_space='wx'")
        data = cur.fetchone()
        access_token = data[0]
        client.set('access_token', access_token)

    u = url + access_token
    open_id = content['open_id']
    data = '{"touser":"%s","msgtype":"text","text":{"content":"红包发放失败，由于您的用户状态异常，使用常用的活跃的微信号可避免这种情况，请联系淘宝客服索取红包。"}}'% open_id
    s = requests.post(u,data=data.encode('utf-8'))
    print s.text
    return True





