
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
import tornado.escape
# import tornado.options
# import tornado.httpserver

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"}),
                (r"/dashboard", DashboardHandler),
                (r"/req", ReqHandler),
                (r"/pool", PoolHandler),
                (r"/", MainHandler),
            ]
        settings = {"debug":True}
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.redirect('/dashboard')


class DashboardHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

# tasks_pool = []
class ReqHandler(tornado.web.RequestHandler):
    def post(self):
        # global tasks_pool
        print(self.request.body)
        for handler in PoolHandler.miners:
            handler.write_message(self.request.body)
        self.finish({})


class PoolHandler(tornado.websocket.WebSocketHandler):
    miners = set()

    def check_origin(self, origin):
        return True

    def open(self):
        if self not in PoolHandler.miners:
            PoolHandler.miners.add(self)
            print('self added')

    def on_close(self):
        if self in PoolHandler.miners:
            PoolHandler.miners.remove(self)
            print('self removed')

    # @tornado.gen.coroutine
    def on_message(self, message):
        print(message)


def main():
    server = Application()
    server.listen(7000, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

