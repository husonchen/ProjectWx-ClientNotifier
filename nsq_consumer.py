from consumer import notify_follower
from consumer import notify_luckmoney_fail
import nsq
import sys  


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8') 
    r = nsq.Reader(message_handler=notify_follower.handler,
                   lookupd_http_addresses=['http://127.0.0.1:4161'],
                   topic='reject_notify', channel='send_wx', lookupd_poll_interval=15)

    r2 = nsq.Reader(message_handler=notify_luckmoney_fail.handler,
                   lookupd_http_addresses=['http://127.0.0.1:4161'],
                   topic='luckymoney_fail', channel='send_wx', lookupd_poll_interval=15)

    nsq.run()
