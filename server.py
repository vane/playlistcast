#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Runs playlistcast media server"""
import os
import sys
import asyncio
import logging
import graphene
import tornado.web
import tornado.ioloop
from playlistcast import config, util
from playlistcast.protocol import chromecast, ssdp
from playlistcast.api import Subscription, Query, Mutation
from playlistcast.api import browse

# https://stackoverflow.com/a/18812776
# Add vendor directory to module search path
PARENT_DIR = os.path.abspath(os.path.dirname(__file__))
VENDOR_DIR = os.path.join(PARENT_DIR, 'vendor/tornadoql')

sys.path.append(VENDOR_DIR)
from tornadoql.tornadoql import GraphQLSubscriptionHandler, GraphQLHandler, GraphiQLHandler # pylint: disable=E0401,C0413


STATIC_PATH = os.path.abspath('frontend/build')
LOG = logging.getLogger('playlistcast')
ALLOWED_HEADERS = ("content-type",)

class GQLSubscriptionHandler(GraphQLSubscriptionHandler):
    def set_default_headers(self):
        origin = self.request.headers.get("Origin")
        method = self.request.headers.get("Access-Control-Request-Method")
        header = self.request.headers.get("Access-Control-Request-Headers")
        print(f"RequestHandler {method} - {origin} - {header}")
        # here can restrict origin - ex for throtling
        if config.DEBUG and origin:
            self.set_header("Access-Control-Allow-Origin", origin)
        if config.DEBUG and method:
            self.set_header("Access-Control-Allow-Method", method)
        if header in ALLOWED_HEADERS:
            self.set_header("Access-Control-Expose-Headers", header)
            self.set_header("Access-Control-Allow-Headers", header)
    def check_origin(self, origin):
        if config.DEBUG:
            return True
        return False

class GQLHandler(GraphQLHandler):
    def set_default_headers(self):
        origin = self.request.headers.get("Origin")
        method = self.request.headers.get("Access-Control-Request-Method")
        header = self.request.headers.get("Access-Control-Request-Headers")
        print(f"RequestHandler {method} - {origin} - {header}")
        # here can restrict origin - ex for throtling
        if config.DEBUG and origin:
            self.set_header("Access-Control-Allow-Origin", origin)
        if config.DEBUG and method:
            self.set_header("Access-Control-Allow-Method", method)
        if header in ALLOWED_HEADERS:
            self.set_header("Access-Control-Expose-Headers", header)
            self.set_header("Access-Control-Allow-Headers", header)

class GiQLHandler(GraphiQLHandler):
    def set_default_headers(self):
        origin = self.request.headers.get("Origin")
        method = self.request.headers.get("Access-Control-Request-Method")
        header = self.request.headers.get("Access-Control-Request-Headers")
        print(f"RequestHandler {method} - {origin} - {header}")
        # here can restrict origin - ex for throtling
        if config.DEBUG and origin:
            self.set_header("Access-Control-Allow-Origin", origin)
        if config.DEBUG and method:
            self.set_header("Access-Control-Allow-Method", method)
        if header in ALLOWED_HEADERS:
            self.set_header("Access-Control-Expose-Headers", header)
            self.set_header("Access-Control-Allow-Headers", header)

class IndexHandler(tornado.web.RequestHandler):
    """Serve index.html"""
    # pylint: disable=W0223
    def get(self):
        """Get request"""
        path = os.path.join(STATIC_PATH, 'index.html')
        with open(path, 'rb') as file:
            self.finish(file.read())

class ConfigHandler(tornado.web.RequestHandler):
    """Serve config.js"""
    # pylint: disable=W0223
    def get(self):
        uri = f'{util.get_ip()}:{config.PORT}'
        # uri = f'localhost:{config.PORT}'
        resp = 'window.playlistcast = {};window.playlistcast.uri = "%s";'% uri
        self.finish(resp)

def startup():
    """Run some scheduled tasks on start"""
    loop = asyncio.get_event_loop()
    loop.create_task(ssdp.find_upnp_services())
    loop.create_task(chromecast.list_devices())
    LOG.debug('startup tasks complete')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # server
    SCHEMA = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
    ENDPOINTS = [
        (r'/subscriptions', GQLSubscriptionHandler, dict(opts=dict(sockets=[],
                                                                       subscriptions={}),
                                                             schema=SCHEMA)),
        (r'/config.js', ConfigHandler),
        (r'/graphql', GQLHandler, dict(schema=SCHEMA)),
        (r'/graphiql', GiQLHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
        (r'/', IndexHandler),
        (r'/resource/(.*)', browse.BrowseResourceHandler),
    ]
    APP = tornado.web.Application(ENDPOINTS)
    APP.listen(config.PORT, config.HOST)

    startup()

    import playlistcast.scheduler # pylint: disable=W0611

    tornado.ioloop.IOLoop.current().start()
