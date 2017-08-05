# -*- coding: utf-8 -*-
import json
import MySQLdb as mdb
from util.memcache_util import Client
import config
import requests

con = mdb.connect('127.0.0.1', 'xiaob', 'skdfjkasdf', 'xunhui')
con.ping(True)
cur = con.cursor()
client = Client(config.prefix)
url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='

def handler(message):
    try:
        content = json.loads(message.body)
        print content
    except:
        return True
    open_id = content['open_id']
    shop_id = content['shop_id']
    cur.execute('SELECT namespace from shop_setting WHERE shop_id=%d', int(shop_id))
    data = cur.fetchone()
    namespace = data[0]
    access_token = client.get(namespace + '_' + 'access_token')
    if not access_token:
        cur.execute("SELECT v from server_config where k = 'access_token' and name_space='wx'")
        data = cur.fetchone()
        access_token = data[0]
        client.set('access_token', access_token)

    u = url + access_token


    data = '{"touser":"%s","msgtype":"text","text":{"content":"红包发放成功，请检查您的微信零钱。"}}'% open_id
    requests.post(u,data=data)
    return True





