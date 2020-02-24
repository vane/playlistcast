#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Scheduled tasks"""
from datetime import datetime
import aiocron
from playlistcast.protocol import ssdp
from .api.subscription import TimeMessage, SubscriptionModel


@aiocron.crontab('* * * * * */1', start=True)
def time_task():
    """Sends time every second"""
    t = datetime.now()
    msg = TimeMessage(id=str(t.timestamp()), time=t)
    SubscriptionModel.time.on_next(msg)
    print("test_task run : ", t)


@aiocron.crontab('* * * * 0 0', start=True)
def find_upnp_task():
    """Find upnp devices every minute"""
    ssdp.find_upnp_services()
