#-*- encoding:utf-8 -*-
#2014-12-18
#author: windyer
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import json
import thread
import time
import random
class ProStatus(object):
    ''' 处理类 '''

    w_register = []

    def register(self, callbacker):
        ''' 记录客户端连接实例 '''
        self.w_register.append(callbacker)

    def unregister(self, callbacker):
        ''' 删除客户端连接实例 '''
        self.w_register.remove(callbacker)

    def makelines(self, data):
        ''' 处理接受的行内容 '''
        self.trigger(data)

    def trigger(self, data):
        ''' 向所有被记录客户端发送最新内容 '''
        print "trigger"
        for callabler in self.w_register:
            print data
            try:
                callabler.write_message(data+"\n")
            except:
                pass

class ReceiveNewLinesHandler(tornado.web.RequestHandler):
    ''' 接受服务器端脚本提交的最新行内容 '''
    def post(self, *args, **kwargs):
        data = self.request.arguments
        post_data = {}
        for key in data:
            post_data[key] = data[key][0]
        post_data = json.dumps(post_data)
        ProStatus().makelines(post_data)

class JsHandler(tornado.web.RequestHandler):
    ''' 接受服务器端脚本提交的最新行内容 '''

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def post(self, *args, **kwargs):
        self.finish({'cpu':random.randint(1,100)})

class CpussHandler(tornado.web.RequestHandler):
    ''' 接受服务器端脚本提交的最新行内容 '''

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Content-type', 'application/json')

    def post(self, *args, **kwargs):
        data = []
        print "1"*100,args,kwargs
        for i in range(3600):
            data.append(random.randint(1,100))
        self.finish({'data':data,'cpuss':random.randint(1,100)})

class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    pool = set()

    def check_origin(self, origin):
        return True

    def open(self):
        ProStatus().register(self)
        WebSocketHandler.pool.add(self)
        pass
    def on_message(self, message):
        for i in WebSocketHandler.pool:
            i.write_message(message+"\n")
            print "massage",message

    def on_close(self):
        print "close"*100
        ProStatus().unregister(self)
        WebSocketHandler.pool.remove(self)
        pass




class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/pull', WebSocketHandler),
            (r'/push', ReceiveNewLinesHandler),
            (r'/js', JsHandler),
            (r'/cpuss', CpussHandler)

        ]

        print "sssss"
        settings = { "template_path": "."}
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
