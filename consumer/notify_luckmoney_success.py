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
url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='

def handler(message):
    try:
        print message.body
        content = json.loads(message.body)
    except:
        message.finish()
        return True
    open_id = content['open_id']
    order_id = content['order_id']
    shop_id = int(content['shop_id'])
    mp_id = content['mp_id']
    if mp_id == '' or mp_id is None:
        message.finish()
        return
    mp_id = int(mp_id)
    money = content['money']
    # if open_id != 'oX4WF0fUTswQFQ11E_ugJ4CyEQR8':
    #     message.finish()
    #     return
    cur.execute('SELECT source_openid,source_namespace from openid_match WHERE pay_openid="%s" order by update_time desc limit 1 '% open_id)
    data = cur.fetchone()
    source_openid = data[0]
    source_namespace = data[1]
    if not source_namespace.isdigit():
        message.finish()
        return
    # mp_id = int(source_namespace)
    mp = client.get('_mp_info_id_%d'%mp_id)
    template_id = client.get('xunhui_template_msg_%d_%s' % (mp_id,'TM00211'))
    if not template_id:
        cur.execute("SELECT template_id from template_msg where mp_id = '%d' and template_id_short='TM00211'" % mp_id)
        data = cur.fetchone()
        template_id = data[0]
        client.set('xunhui_template_msg_%d_%s' % (mp_id,'TM00211'), template_id)

    data = {"touser":source_openid, "template_id": template_id,
     "url": "http://wx.51dingxiao.com/cross_refund/oauth1?name=%d"%mp_id,
     "data": {"first": {"value": mp.nick_name, "color": "#173177"},
              "order": {"value": order_id, "color": "#173177"}, "money": {"value": str(1.0*int(money)/100)+'元', "color": "#173177"},
              "remark": {"value": "请到微信支付公众号查收", "color": "#173177"}}}
    u = url + mp.authorizer_access_token

    r = requests.post(u,data=json.dumps(data,ensure_ascii=True))
    # print r.text
    message.finish()
    return True





