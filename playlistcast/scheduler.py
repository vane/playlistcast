#!/usr/bin/env python
# -*- coding: utf-8 -*-
import aiocron
from datetime import datetime
from .api.subscription import TimeMessage, SubscriptionModel


@aiocron.crontab('* * * * * */1', start=True)
def test_task():
    t = datetime.now()
    msg = TimeMessage(id=str(t.timestamp()), time=t)
    SubscriptionModel.time.on_next(msg)
    print("test_task run : ", t)
