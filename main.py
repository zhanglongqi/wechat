#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
longqi 9/6/15 22:11

"""
import tornado.ioloop
import tornado.web
import hashlib
from wechat_sdk import WechatBasic

from tornado.options import define, options

define("port", default=80, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


token = 'test'
wechat = WechatBasic(token=token)


class WechatHandler(tornado.web.RequestHandler):
    def get(self):
        print('URI', self.request.uri)
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr = self.get_argument('echostr')

        args_list = [token, timestamp, nonce]
        print(args_list)
        args_list.sort()
        # sha1
        tmp_str = ''.join(args_list)
        hashcode = hashlib.sha1(tmp_str.encode('utf-8')).hexdigest()
        # if success return echostr to wechat
        print('hashcode', hashcode)
        if hashcode == signature:
            print("true")
            self.write(echostr)
        else:
            self.write('fail ... ')

    def post(self, *args, **kwargs):
        print('URI', self.request.uri)
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        if wechat.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
            print('POST pass: ', self.request.body)


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/wechat/", WechatHandler),
])
application.settings['debug'] = True
if __name__ == "__main__":
    application.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
