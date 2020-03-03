#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application custom error messages"""
import tornado.web


class ResourcePathError(tornado.web.HTTPError):
    """Invalid ResourceLocation path"""
    code = 1001
    def __init__(self, message):
        tornado.web.HTTPError.__init__(self, reason=message)


class ChromecastUUIDError(tornado.web.HTTPError):
    """Invalid Chromecast uuid"""
    code = 1001
    message = "Chromecast with uuid '{}' not found"
    def __init__(self, uid):
        tornado.web.HTTPError.__init__(self, reason=self.message.format(uid))
