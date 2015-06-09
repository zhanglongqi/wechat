# coding: UTF-8
import tornado.ioloop
import tornado.web
import hashlib


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


class WechatHandler(tornado.web.RequestHandler):
    def get(self):
        data = self.get_argument()
        print(data)
        signature = data.signature
        timestamp = data.timestamp
        nonce = data.nonce
        echostr = data.echostr
        # 自己的token
        token = "yourtoken"
        # 字典序排序
        list = [token, timestamp, nonce]
        list.sort()
        # sha1加密算法
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        # 如果是来自微信的请求，则回复echostr
        if hashcode == signature:
            # print "true"
            return echostr


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/wechat", WechatHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
