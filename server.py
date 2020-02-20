#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import graphene
import tornado.web
import tornado.ioloop
from playlistcast.api import Subscription, Query, Mutation

# https://stackoverflow.com/a/18812776
# Add vendor directory to module search path
parent_dir = os.path.abspath(os.path.dirname(__file__))
vendor_dir = os.path.join(parent_dir, 'vendor/tornadoql')

sys.path.append(vendor_dir)
from tornadoql.tornadoql import GraphQLSubscriptionHandler, GraphQLHandler, GraphiQLHandler


STATIC_PATH = os.path.abspath('frontend/build')

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        path = os.path.join(STATIC_PATH, 'index.html')
        with open(path, 'rb') as f:
            self.finish(f.read())

if __name__ == '__main__':
    # configuration
    debug = False
    port = 9666

    # server
    schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
    endpoints = [
        (r'/subscriptions', GraphQLSubscriptionHandler, dict(opts=dict(sockets=[],
                                                                       subscriptions={}),
                                                             schema=schema)),
        (r'/graphql', GraphQLHandler, dict(schema=schema)),
        (r'/graphiql', GraphiQLHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
        (r'/', IndexHandler),
    ]
    app = tornado.web.Application(endpoints)
    app.listen(port, "0.0.0.0")

    tornado.ioloop.IOLoop.current().start()


