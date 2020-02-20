#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pathlib
import random
import copy
import time
import logging
import requests
from typing import List, Dict, Any

log = logging.getLogger('playlistcast.m3u')


class PlayIndex:
    def __init__(self, start:int=0, end:int=0, current:int=None):
        self.start = start
        self.end = end
        self.current = current

    def next(self) -> int:
        if self.current is None or self.current >= self.end:
            self.current = self.start
        else:
            self.current += 1
        log.debug('PlayIndex.next {}'.format(self.current))
        return self.current

    def to_dict(self) -> Dict:
        return {
            'start': self.start,
            'end': self.end,
            'current': self.current
        }

    @staticmethod
    def fromdict(data:Any):
        return PlayIndex(start=data['start'], end=data['end'], current=data['current'])

class PlaylistItem:
    def __init__(self, basepath:str='', path:str='', name:str=''):
        self._basepath = basepath
        self._path = path
        self._name = name

    @property
    def path(self) -> str:
        return '{}/{}'.format(self._basepath, self._path)

    @property
    def name(self) -> str:
        return self._name

    def __repr__(self):
        return self.path

class FileLoader:
    @staticmethod
    def load_disk_file(fpath:str) -> (str, str):
        # check path
        path = pathlib.Path(fpath)
        if not path.exists():
            raise ValueError('File not exists')
        basepath = path.parent
        # open file
        data = b''
        with open(fpath, 'rb') as f:
            data = f.read().decode()
        return data, basepath

    @staticmethod
    def load_http_file(fpath:str) -> (str, str):
        resp = requests.get(fpath)
        basepath = '/'.join(resp.url.split('/')[:-1])
        return resp.content.decode(), basepath

class M3UPlaylist:
    def __init__(self, index_default:PlayIndex=None):
        self._items = [PlaylistItem()]
        self._index = PlayIndex()
        self._index_default = index_default

    @property
    def items(self) -> List[PlaylistItem]:
        return self._items

    @property
    def index(self) -> int:
        return self._index

    # PUBLIC
    def load(self, fpath:str):
        data, basepath = self._load_file(fpath)
        a = data.split('\n')
        # check first line
        if a[0].startswith('#EXTM3U'):
            # find first item and parse
            found = False
            for i in range(0, len(a)):
                if a[i].startswith('#EXTINF'):
                    # check if last line is empty string
                    found = True
                    if not a[-1]:
                        self._items = self._parse_playlist(basepath, a[i:-1])
                    else:
                        self._items = self._parse_playlist(basepath, a[i:])
                    if self._index_default is not None:
                        self._index = PlayIndex.fromdict(self._index_default.to_dict())
                    else:
                        self._index = PlayIndex(start=0, end=len(self._items)-1, current=None)
                    break
            if not found:
                raise ValueError('Empty file or playlist')
        else:
            raise ValueError('Invalid file content')

    def set_index(self, index: PlayIndex):
        self._index = index

    def next(self) -> PlaylistItem:
        item = self.items[self._index.next()]
        log.debug('M3UPlaylist.next {} {}'.format(item.path, item.name))
        return item

    # PRIVATE
    def _parse_playlist(self, basepath:str, data:List) -> List[PlaylistItem]:
        name = None
        out = []
        for el in data:
            if el.startswith('#EXTINF'):
                name = el.split(',')[1]
            else:
                item = PlaylistItem(basepath, el, name)
                out.append(item)
        return out

    def _load_file(self, fpath:str) -> (str, str):
        if fpath.startswith('http'):
            return FileLoader.load_http_file(fpath)
        else:
            return FileLoader.load_disk_file(fpath)
