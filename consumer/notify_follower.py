# -*- coding: utf-8 -*-
import json
import MySQLdb as mdb
from util.memcache_util import Client
import config
import requests

con = mdb.connect('localhost', 'xiaob', 'skdfjkasdf', 'xiaob')
con.ping(True)
cur = con.cursor()
client = Client(config.prefix)
url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='

def handler(message):
    try:
        ids = json.loads(message.body)
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
        data = '{"touser":"%s","msgtype":"text","text":{"content":"您的好评返现申请不通过，可能因为上传的图片不符合要求。正确多次不通过截图联系淘宝客服"}}'% open_id
        requests.post(u,data=data)
    return True





