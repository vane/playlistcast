#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Serve static files using ResourceLocation defined resources"""
import os
from typing import Optional
import urllib.parse
import tornado.web
from playlistcast import db, error


class BrowseResourceHandler(tornado.web.StaticFileHandler):
    """Serve attached resources"""
    # pylint: disable=W0223
    def initialize(self):
        """Override hack"""
        self.root = ''

    def set_etag_header(self):
        """Override hack"""
        pass

    @classmethod
    def get_absolute_path(cls, root: str, path: str):
        """Override hack"""
        return path

    def validate_absolute_path(self, root: str, absolute_path: str) -> Optional[str]:
        """Override hack"""
        return absolute_path

    async def get(self, *args, **kwargs):
        """Get request"""
        a = args[0].split('/')
        model = db.session.query(db.ResourceLocation).filter(db.ResourceLocation.name == a[0]).first()
        if not model:
            raise error.ResourcePathError('Invalid path {}'.format(args[0]))
        uri = '/resource/'
        if len(a) > 0:
            uri += args[0]
            path = os.path.join(model.location, '/'.join(a[1:]))
        else:
            path = model.location
        if not os.path.exists(path):
            raise error.ResourcePathError('Path not exists {}'.format(path))
        if os.path.isdir(path):
            content = ''
            back = '/'.join(uri.split('/')[:-1])
            # back link if not absolute
            if back != '/resource':
                content = '<a href={}>..</a><br />'.format(urllib.parse.quote(back))
            for name in sorted(os.listdir(path)):
                content += '<a href={path}>{name}</a><br />'.format(**{
                    'name': name,
                    'path': urllib.parse.quote(uri+'/'+name),
                })
            msg = """<html>
            <body>
            %s
            </body>
            </html>
            """ % content
            self.finish(msg)
        else:
            await tornado.web.StaticFileHandler.get(self, path)
