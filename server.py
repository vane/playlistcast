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

class IndexHandler(tornado.web.RequestHandler):
    """Serve index.html"""
    # pylint: disable=W0223
    def get(self):
        """Get request"""
        path = os.path.join(STATIC_PATH, 'index.html')
        with open(path, 'rb') as file:
            self.finish(file.read())


def startup():
    """Run some scheduled tasks on start"""
    loop = asyncio.get_event_loop()
    loop.create_task(ssdp.find_upnp_services())
    loop.create_task(chromecast.list_devices())
    LOG.debug('startup tasks complete')

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    # configuration
    DEBUG = False
    PORT = 9666
    HOST = '0.0.0.0'

    # server
    SCHEMA = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
    ENDPOINTS = [
        (r'/subscriptions', GraphQLSubscriptionHandler, dict(opts=dict(sockets=[],
                                                                       subscriptions={}),
                                                             schema=SCHEMA)),
        (r'/graphql', GraphQLHandler, dict(schema=SCHEMA)),
        (r'/graphiql', GraphiQLHandler),
        (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': STATIC_PATH}),
        (r'/', IndexHandler),
        (r'/resource/(.*)', browse.BrowseResourceHandler),
    ]
    APP = tornado.web.Application(ENDPOINTS)
    APP.listen(PORT, HOST)

    startup()

    tornado.ioloop.IOLoop.current().start()
