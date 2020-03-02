#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chromecast"""
import time
import logging
from typing import List
from datetime import timedelta
import pychromecast
import pychromecast.controllers.media as chromecast_media
from playlistcast.api.model.device import ChromecastDevice, MediaController, MediaStatus, CastStatus
from playlistcast import util, cache
from playlistcast.api.subscription import SubscriptionModel

LOG = logging.getLogger('playlistcast.protocol.chromecast')
DEBUG = False

class PlayerTime:
    """PlayerTime"""
    def __init__(self, current: int = 0, duration: int = 0):
        self.current = current
        self.duration = duration

    @property
    def timestring(self) -> str:
        """Return formated media time"""
        if self.current and self.duration:
            cdelta = timedelta(seconds=self.current)
            ddelta = timedelta(seconds=self.duration)
            current = util.strfdelta(cdelta, "%H:%M:%S")
            duration = util.strfdelta(ddelta, "%H:%M:%S")
            return f'{current}/{duration}'
        return '00:00:00/00:00:00'

    @property
    def percent(self) ->str:
        """Return formated percent of media progress"""
        if self.duration:
            return f'{self.current/self.duration*100:0.1f}%'
        return '0%'

class DummyChromeast:
    """Chromecast"""
    def __init__(self, media_url: str, media_type: str = 'video/mp4', name: str = 'Hell TV'):
        self._media_url = media_url
        self._media_type = media_type
        self._name = name
        self.cast = None
        self.media_controller = None
        self.new_play = False
        self.media_time = PlayerTime()

    def start(self):
        """Start chromecast"""
        self._start()
        # TODO refactoring
        mc = self.media_controller
        cast = self.cast
        # FOR DEBUG
        # if debugskip to end
        to_the_end = DEBUG
        to_the_end_seconds = 20
        while True:
            if mc.is_playing or mc.is_paused:
                if mc.status:
                    # TODO check if resumed after crash
                    if not self.media_time.duration and mc.status.duration:
                        self.media_time.duration = mc.status.duration
                        self.new_play = True
                    self.media_time.current = mc.status.current_time
                    LOG.debug('%s - %s', self.media_time.timestring, self.media_time.percent)
                    if to_the_end:
                        mc.update_status()
                        mc.seek(int(self.media_time.duration) - to_the_end_seconds)
                        mc.block_until_active(timeout=30)
                        time.sleep(5)
                        to_the_end = False
                else:
                    LOG.debug('TODO problem')
            else:
                print('play media {}'.format(self._media_url))
                if DEBUG:
                    to_the_end = True
                mc.play_media(self._media_url, self._media_type)
                mc.block_until_active(timeout=30)
                time.sleep(5)
                cast.set_volume(0.65)
                self.media_time.duration = mc.status.duration
                self.new_play = True
            mc.update_status()
            time.sleep(1)

    def change_media(self, media_url: str, media_type: str = 'video/mp4'):
        """Change chromecast media"""
        self._media_url = media_url
        self._media_type = media_type
        self.new_play = False

    def seek(self, seconds: int):
        """Seek in media"""
        mc = self.media_controller
        mc.update_status()
        mc.seek(seconds)
        mc.block_until_active(timeout=30)

    def _start(self):
        """Find chromecasts"""
        # find and wait for chromecast
        chromecasts = pychromecast.get_chromecasts()
        for ch in chromecasts:
            if ch.name == self._name:
                self.cast = ch
                self.cast.wait(timeout=30)
        print(self.cast.status)
        # media controller
        self.media_controller = self.cast.media_controller
        self.media_controller.block_until_active(timeout=30)
        self.media_controller.register_status_listener(self)

    @classmethod
    def new_media_status(cls, status):
        """ Subscribe for chromecast status messages"""
        #LOG.debug(status)
        pass

class Device:
    def __init__(self, device, data):
        self.device = device
        self.data = data
        self.device.media_controller.register_status_listener(self)

    def new_media_status(self, status):
        """Subscribe for chromecast status messages"""
        s = MediaStatus()
        s.uuid = self.data.uuid
        util.convert(status, s, ('uuid',))
        SubscriptionModel.media_status.on_next(s)
        print(self.data.name, self.data.uuid, status)

async def list_devices() -> List[ChromecastDevice]:
    """Detect and return chromecast devices"""
    chromecasts = pychromecast.get_chromecasts()
    output = []
    all_keys = list(cache.CHROMECAST.keys())
    for pych in chromecasts:
        uid = str(pych.uuid)
        if uid in cache.CHROMECAST:
            all_keys.remove(uid)
            device = cache.CHROMECAST[uid]
            output.append(device.data)
        else:
            pych.wait(timeout=30)
            # pychromecast
            ch = ChromecastDevice()
            util.convert(pych, ch, ('media_controller', 'status'))

            pych.media_controller.block_until_active(timeout=30)
            # pychromecast status
            if pych.status is not None:
                s = CastStatus()
                s.uuid = uid
                util.convert(pych.status, s, ('media_controller', 'status', 'uuid'))
                ch.status = s

            # pychromecast media_controller
            mc = MediaController()
            mc.uuid = uid
            util.convert(pych.media_controller, mc, ('status', 'uuid'))

            # pychromecast media_controller media_status
            ms = MediaStatus()
            ms.uuid = uid
            util.convert(pych.media_controller.status, ms, ('uuid',))

            mc.status = ms
            ch.media_controller = mc
            output.append(ch)
            device = Device(pych, ch)
            cache.CHROMECAST[uid] = device
    # REMOVE remaining keys cause those are expired devices
    # TODO send update to UI
    if len(all_keys) > 0:
        for key in all_keys:
            del cache.CHROMECAST[key]
    return output
