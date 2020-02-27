#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web


class ResourcePathError(tornado.web.HTTPError):
    code = 1001
    def __init__(self, message):
        tornado.web.HTTPError.__init__(self, reason=message)
