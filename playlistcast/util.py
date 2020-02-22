#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Utility methods"""
from string import Template
from datetime import timedelta
import socket

#https://stackoverflow.com/a/8907269
class TimeDeltaFormatter(Template):
    """TimeDeltaFormatter"""
    delimiter = "%"

def strfdelta(tdelta: timedelta, fmt: str) -> str:
    """Format timedelta using formatter"""
    h, rem = divmod(tdelta.seconds, 3600)
    m, s = divmod(rem, 60)
    return TimeDeltaFormatter(fmt).substitute(**{
        'H':f'{h:02}',
        'M':f'{m:02}',
        'S':f'{s:02}',
    })

# https://stackoverflow.com/a/28950776
def get_ip() -> str:
    """Get network assigned ip address"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        raise RuntimeError("IP not detected")
    finally:
        s.close()
    return IP
