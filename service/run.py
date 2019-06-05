# -*- coding: utf-8 -*-
import argparse
import tornado.httpserver
import tornado.ioloop
import tornado.web
from request_handler import *
from context import g_ctx


class Service(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/status", StatusRequestHandler),
            (r"/log_stream", LogStreamRequestHandler), 
            (r"/log_stream/(.+?)", LogStreamInstanceRequestHandler), 
        ]
        settings = dict(
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="specify port", default=8401, 
            type=int)
    parser.add_argument("-c", "--config", help="specify config file",
            default='/conf/logbus/test.conf')
    args = parser.parse_args()
    g_ctx.init(args.config)
    print('service run on [{}]'.format(args.port))
    server = tornado.httpserver.HTTPServer(Service())
    server.listen(args.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()

