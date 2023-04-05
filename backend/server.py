
import tornado.web
import tornado.ioloop
import tornado.gen
import tornado.escape
import tornado.options
import tornado.httpserver

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
                (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static/"}),
                (r"/dashboard", DashboardHandler),
                (r"/req", ReqHandler),
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

tasks_pool = []
class ReqHandler(tornado.web.RequestHandler):
    def post(self):
        global tasks_pool
        print(self.request.body)
        self.finish({})


def main():
    server = Application()
    server.listen(7000, '0.0.0.0')
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()

