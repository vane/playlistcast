#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scheduled tasks"""
from datetime import datetime
import aiocron
from playlistcast.protocol import ssdp, chromecast
from .api.subscription import TimeMessage, SubscriptionModel


@aiocron.crontab('* * * * * */30', start=True)
async def time_task():
    """Sends time every second"""
    t = datetime.now()
    msg = TimeMessage(id=str(t.timestamp()), time=t)
    SubscriptionModel.time.on_next(msg)
    print("test_task run : ", t)


@aiocron.crontab('*/5 * * * *', start=True)
async def find_upnp_task():
    """Find upnp devices every minute"""
    await ssdp.find_upnp_services()


@aiocron.crontab('*/10 * * * *', start=True)
async def find_chromecast_task():
    """Periodically check for new chromecast devices"""
    await chromecast.list_devices()
    print('o.O')
