#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Chromecast"""
import logging
from typing import List
from datetime import timedelta
import pychromecast
import pychromecast.controllers.media as chromecast_media # pylint: disable=W0611
import playlistcast.api.model.chromecast as chromecast_model
from playlistcast import util
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

async def list_devices() -> List[chromecast_model.ChromecastModel]:
    """Detect and return chromecast devices"""
    chromecasts = await util.awaitable(pychromecast.get_chromecasts)
    output = []
    all_keys = list(chromecast_model.CHROMECAST.keys())
    for pych in chromecasts:
        uid = str(pych.uuid)
        if uid in chromecast_model.CHROMECAST:
            all_keys.remove(uid)
            device = chromecast_model.CHROMECAST[uid]
            output.append(device.data)
        else:
            await util.awaitable(pych.wait, timeout=30)
            # pychromecast
            ch = util.convert(pych, chromecast_model.ChromecastModel, ('media_controller', 'status'))

            pych.media_controller.block_until_active(timeout=30)
            # pychromecast status
            if pych.status is not None:
                s = util.convert(pych.status, chromecast_model.CastStatus, ('media_controller', 'status', 'uuid'))
                s.uuid = uid
                ch.status = s

            # pychromecast media_controller
            mc = util.convert(pych.media_controller, chromecast_model.MediaController, ('status', 'uuid'))
            mc.uuid = uid
            # pychromecast media_controller media_status
            st = pych.media_controller.status
            ms = util.convert(st, chromecast_model.MediaStatus, ('uuid', 'track_list'))
            ms.uuid = uid
            # media_status subtitles
            media_tracks = list()
            for tr in st.subtitle_tracks:
                track = util.convert(tr, chromecast_model.MediaTrack)
                media_tracks.append(track)
            ms.track_list = media_tracks

            mc.status = ms
            ch.media_controller = mc
            output.append(ch)
            device = chromecast_model.ChromecastDevice(pych, ch)
            chromecast_model.CHROMECAST[uid] = device
            SubscriptionModel.chromecast.on_next(ch)
    # REMOVE remaining keys cause those are expired devices
    # TODO send update to UI
    if len(all_keys) > 0:
        for key in all_keys:
            del chromecast_model.CHROMECAST[key]
    return output
