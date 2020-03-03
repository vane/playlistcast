#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Application models"""
from .api.model.device import MediaStatus
from .api.model.subscription import SubscriptionModel
from playlistcast import util

class Device:
    """Device with api and interface data"""
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
