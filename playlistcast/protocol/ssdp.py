#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" SSDP protocol messages """
import socket
import logging
from typing import Dict, Tuple
from io import BytesIO
from http_parser.http import HttpStream

DISCOVER_HOST = '239.255.255.250'
DISCOVER_PORT = 1900
# discover ssdp msg
DISCOVER_MSG = """M-SEARCH * HTTP/1.1\r
HOST:{}:{}\r
ST:upnp:rootdevice\r
MX:2\r
MAN:\"ssdp:discover\"\r
\r\n""".format(DISCOVER_HOST, DISCOVER_PORT).encode()

LOG = logging.getLogger('playlistcast.protocol.ssdp')


async def find_upnp_services() -> Dict[Tuple, HttpStream]:
    """ Find all upnp services around"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.settimeout(2)
    s.sendto(DISCOVER_MSG, (DISCOVER_HOST, DISCOVER_PORT))
    services = {}
    try:
        # https://www.electricmonk.nl/log/2016/07/05/exploring-upnp-with-python/
        while True:
            data, addr = s.recvfrom(65507)
            services[addr] = HttpStream(BytesIO(data))
            LOG.debug(addr)
    except socket.timeout:
        pass
    return services
