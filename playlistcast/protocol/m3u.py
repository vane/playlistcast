#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""M3U playlist format"""
import pathlib
import logging
from typing import List, Dict, Any
import requests

LOG = logging.getLogger('playlistcast.protocol.m3u')


class PlayIndex:
    """PlayIndex"""
    def __init__(self, start: int = 0, end: int = 0, current: int = None):
        self.start = start
        self.end = end
        self.current = current

    def next(self) -> int:
        """Increment current index"""
        if self.current is None or self.current >= self.end:
            self.current = self.start
        else:
            self.current += 1
        LOG.debug('PlayIndex.next %s', self.current)
        return self.current

    def to_dict(self) -> Dict:
        """Playlist as dictionary"""
        return {
            'start': self.start,
            'end': self.end,
            'current': self.current
        }

    @staticmethod
    def fromdict(data: Any):
        """Playlist index"""
        return PlayIndex(start=data['start'], end=data['end'], current=data['current'])

class PlaylistItem:
    """Playlist item"""
    def __init__(self, basepath: str = '', path: str = '', name: str = ''):
        self._basepath = basepath
        self._path = path
        self._name = name

    @property
    def path(self) -> str:
        """Item path"""
        return '{}/{}'.format(self._basepath, self._path)

    @property
    def name(self) -> str:
        """Item name"""
        return self._name

    def __repr__(self):
        return self.path

class FileLoader:
    """FileLoader"""
    @staticmethod
    def load_disk_file(fpath: str) -> (str, str):
        """Load file from disk"""
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
    def load_http_file(fpath: str) -> (str, str):
        """Load file from http"""
        resp = requests.get(fpath)
        basepath = '/'.join(resp.url.split('/')[:-1])
        return resp.content.decode(), basepath

class M3UPlaylist:
    """M3UPlaylist"""
    def __init__(self, index_default: PlayIndex = None):
        self._items = [PlaylistItem()]
        self._index = PlayIndex()
        self._index_default = index_default

    @property
    def items(self) -> List[PlaylistItem]:
        """Get list of PlaylistItem"""
        return self._items

    @property
    def current_item(self) -> PlaylistItem:
        item = self.items[self._index.current]
        return item


    @property
    def index(self) -> PlayIndex:
        """Get play index"""
        return self._index

    # PUBLIC
    def load(self, fpath: str):
        """Load m3u playlist from file"""
        data, basepath = self._load_file(fpath)
        a = data.split('\n')
        # check first line
        if a[0].startswith('#EXTM3U'):
            # find first item and parse
            found = False
            for i, item in enumerate(a):
                if item.startswith('#EXTINF'):
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
        """Change index"""
        self._index = index

    def next(self) -> PlaylistItem:
        """Next PlaylistItem"""
        item = self.items[self._index.next()]
        LOG.debug('M3UPlaylist.next %s %s', item.path, item.name)
        return item

    # PRIVATE
    def _parse_playlist(self, basepath: str, data: List) -> List[PlaylistItem]:
        """"Parse m3u playlist"""
        name = None
        out = []
        for el in data:
            if el.startswith('#EXTINF'):
                name = el.split(',')[1]
            else:
                item = PlaylistItem(basepath, el, name)
                out.append(item)
        return out

    def _load_file(self, fpath: str) -> (str, str):
        """Load m3u file from various locations"""
        if fpath.startswith('http'):
            return FileLoader.load_http_file(fpath)
        return FileLoader.load_disk_file(fpath)
