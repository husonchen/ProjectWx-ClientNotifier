from consumer import notify_follower
import nsq



if __name__ == '__main__':
    r = nsq.Reader(message_handler=notify_follower.handler,
                   lookupd_http_addresses=['http://127.0.0.1:4161'],
                   topic='reject_notify', channel='send_wx', lookupd_poll_interval=15)
    nsq.run()