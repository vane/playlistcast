#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""M3U playlist format"""
import os
import pathlib
import logging
from typing import List, Dict, Any
import requests

LOG = logging.getLogger('playlistcast.protocol.m3u')

class PlaylistItem:
    """Playlist item"""
    def __init__(self, index:int, path: str = '', name: str = ''):
        self._index = index
        self._path = path
        self._name = name

    @property
    def path(self) -> str:
        """Item path"""
        return self._path

    @property
    def name(self) -> str:
        """Item name"""
        return self._name

    @property
    def index(self) -> int:
        """Item index"""
        return self._index

    def __repr__(self):
        return self.path

class M3UPlaylist:
    """M3UPlaylist"""
    def __init__(self):
        self._index = 1
        self._items = [PlaylistItem(self._index)]

    @property
    def items(self) -> List[PlaylistItem]:
        """Get list of PlaylistItem"""
        return self._items

    @property
    def current_item(self) -> PlaylistItem:
        item = self.items[self._index - 1]
        return item


    @property
    def index(self) -> int:
        """Get play index"""
        return self._index

    # PUBLIC
    def load(self, location: str, fpath: str):
        """Load m3u playlist from file"""
        data = self._load_file(location, fpath)
        m3u_dir = pathlib.Path(fpath).parent
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
                        self._items = self._parse_playlist(a[i:-1])
                    else:
                        self._items = self._parse_playlist(a[i:])
                    break
            if not found:
                raise ValueError('Empty file or playlist')
        else:
            raise ValueError('Invalid file content')
        return m3u_dir

    def set_index(self, index: int):
        """Change index"""
        self._index = index

    def next(self) -> PlaylistItem:
        """Next PlaylistItem"""
        self._index += 1
        if self._index > len(self.items):
            self._index = 1
        item = self.items[self._index]
        LOG.debug('M3UPlaylist.next %s %s', item.path, item.name)
        return item

    # PRIVATE
    def _parse_playlist(self, data: List) -> List[PlaylistItem]:
        """"Parse m3u playlist"""
        name = None
        out = []
        i = 1
        for el in data:
            if el.startswith('#EXTINF'):
                name = el.split(',')[1]
            else:
                item = PlaylistItem(i, el, name)
                out.append(item)
                i += 1
        return out

    def _load_file(self, location:str, path: str) -> (str, str):
        """Load m3u file from disk"""
        # check path
        fpath = os.path.join(location, path)
        if not os.path.exists(fpath):
            raise ValueError('File not exists')
        # open file
        data = b''
        with open(fpath, 'rb') as f:
            data = f.read().decode()
        return data
