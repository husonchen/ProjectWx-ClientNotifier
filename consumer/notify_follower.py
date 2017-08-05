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
        ids = json.loads(message.body)
        print ids
    except:
        return True
    access_token = client.get('access_token')
    if not access_token:
        cur.execute("SELECT v from server_config where k = 'access_token' and name_space='wx'")
        data = cur.fetchone()
        access_token = data[0]
        client.set('access_token', access_token)
    u = url + access_token
    q = ''
    for id in ids:
        q += id + ','
    q = q[:-1]
    num = cur.execute("select open_id from user_upload where id in (%s)"%q)
    rows = cur.fetchmany(num)
    for row in rows:
        open_id = row[0]
        data = '{"touser":"%s","msgtype":"text","text":{"content":"您的好评返现申请不通过，请前往淘宝（我的订单--确认收货--晒图并好评）完成后，并上传评价截图（不是好评的晒图，是评价内容的截图）领取2-8元现金红包。"}}'% open_id
        requests.post(u,data=data)
    return True





