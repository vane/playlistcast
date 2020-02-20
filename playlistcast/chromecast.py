#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import logging
from builtins import hasattr
from datetime import timedelta
import urllib.parse
import pychromecast
import pychromecast.controllers.media as chromecast_media
import playlistcast.util

log = logging.getLogger('playlistcast.chromecast')

class PlayerTime:
    def __init__(self, current:int=0, duration:int=0):
        self.current = current
        self.duration = duration

    @property
    def timestring(self) -> str:
        if self.current and self.duration:
            cdelta = timedelta(seconds=self.current)
            ddelta = timedelta(seconds=self.duration)
            return f'{lib.util.strfdelta(cdelta, "%H:%M:%S")}/{lib.util.strfdelta(ddelta, "%H:%M:%S")}'
        return '00:00:00/00:00:00'

    @property
    def percent(self) ->str:
        if self.duration:
            return f'{self.current/self.duration*100:0.1f}%'
        return '0%'

class ChromeCast:
    def __init__(self, media_url:str, media_type:str='video/mp4', stream_type:str=chromecast_media.STREAM_TYPE_BUFFERED):
        self._media_url = media_url
        self._media_type = media_type
        self._stream_type = stream_type
        self.cast = None
        self.media_controller = None
        self.debug = False
        self.new_play = False
        self.media_time = PlayerTime()

    def start(self):
        self._start()
        # TODO refactoring
        mc = self.media_controller
        cast = self.cast
        # FOR DEBUG
        # if debugskip to end
        to_the_end = self.debug
        to_the_end_seconds = 20
        while True:
            if mc.is_playing or mc.is_paused:
                if mc.status:
                    # TODO check if resumed after crash
                    if not self.media_time.duration and mc.status.duration:
                        self.media_time.duration = mc.status.duration
                        self.new_play = True
                    self.media_time.current = mc.status.current_time
                    log.debug(f'{self.media_time.timestring} - {self.media_time.percent}')
                    if to_the_end:
                        mc.update_status()
                        mc.seek(int(self.media_time.duration) - to_the_end_seconds)
                        mc.block_until_active(timeout=30)
                        time.sleep(5)
                        to_the_end = False
                else:
                    log.debug('TODO problem')
            else:
                print('play media {}'.format(self._media_url))
                if self.debug:
                    to_the_end = True
                mc.play_media(self._media_url, self._media_type, stream_type=self._stream_type)
                mc.block_until_active(timeout=30)
                time.sleep(5)
                cast.set_volume(0.65)
                self.media_time.duration = mc.status.duration
                self.new_play = True
            mc.update_status()
            time.sleep(1)

    def change_media(self, media_url:str, media_type:str='video/mp4', stream_type:str=chromecast_media.STREAM_TYPE_BUFFERED):
        self._media_url = media_url
        self._media_type = media_type
        self._stream_type = stream_type
        self.new_play = False

    def seek(self, seconds:int):
        mc = self.media_controller
        mc.update_status()
        mc.seek(seconds)
        mc.block_until_active(timeout=30)

    def _start(self):
        # find and wait for chromecast
        chromecasts = pychromecast.get_chromecasts()
        self.cast = chromecasts[0]
        self.cast.wait(timeout=30)
        print(self.cast.status)
        # media controller
        self.media_controller = self.cast.media_controller
        self.media_controller.block_until_active(timeout=30)
        self.media_controller.register_status_listener(self)

    @classmethod
    def new_media_status(cls, status):
        #log.debug(status)
        pass
