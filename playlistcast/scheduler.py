#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scheduled tasks"""
import traceback
from datetime import datetime
import aiocron
from pychromecast.error import UnsupportedNamespace
from playlistcast.protocol import ssdp, chromecast
from playlistcast import cache
from .api.subscription import TimeMessage, SubscriptionModel


@aiocron.crontab('* * * * * */1', start=True)
async def time_task():
    """Sends time every 30 seconds"""
    t = datetime.now()
    msg = TimeMessage(id=str(t.timestamp()), time=t)
    SubscriptionModel.time.on_next(msg)
    print("test_task run : ", t)


@aiocron.crontab('*/5 * * * *', start=True)
async def find_upnp_task():
    """Find upnp devices every 5 minutes"""
    await ssdp.find_upnp_services()


@aiocron.crontab('*/10 * * * *', start=True)
async def find_chromecast_task():
    """Check for new chromecast devices every 10 minutes"""
    await chromecast.list_devices()
    print('o.O')

@aiocron.crontab('* * * * * */10', start=True)
async def update_chromecast_status():
    """Update chromecast status every 10 seconds"""
    for ch in cache.CHROMECAST.values():
        try:
            ch.device.media_controller.update_status()
        except UnsupportedNamespace:
            traceback.format_exc()
