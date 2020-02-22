#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""UPNP services"""
import logging
from urllib.parse import urlparse
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup
from http_parser.http import HttpStream

LOG = logging.getLogger('playlistcast.protocol.upnp')


class XMLService:
    """Base XMLService class"""
    def __init__(self, location: str):
        self.location = location
        # https://stackoverflow.com/a/9626596
        self._base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(location))
        self._initialized = False
        self._tree = None

    def _set_data(self):
        """Initialize data"""
        resp = requests.get(self.location)
        self._tree = BeautifulSoup(resp.content, features="html.parser")
        self._initialized = True

    @property
    def xmltree(self) -> BeautifulSoup:
        """Return xml value"""
        if not self._initialized:
            self._set_data()
        return self._tree


class UPNPInfo:
    """Simplified access to parts of UPNP service"""
    def __init__(self, xmltree: BeautifulSoup):
        self.xmltree = xmltree

    @property
    def friendlyname(self) -> str:
        """UPNP device friendly name"""
        return self.xmltree.device.friendlyname.text

    @property
    def manufacturer(self) -> str:
        """UPNP device manufacturer"""
        return self.xmltree.device.manufacturer.text


class ScpdActions(XMLService):
    """SCPD actions interface"""
    def __init__(self, location: str, control_uri: str, event_uri: str):
        XMLService.__init__(self, location)
        self.control_uri = control_uri
        self.event_uri = event_uri

    @property
    def action_names(self) -> List[str]:
        """List scpd action names"""
        return [a.find('name').text for a in self.xmltree.actionlist.findAll('action')]


class UPNPService(XMLService):
    """UPNP service access"""
    def __init__(self, host: str, port: int, location: str):
        XMLService.__init__(self, location)
        self.host = host
        self.port = port

    def __repr__(self):
        return "{}:{} - {}".format(self.host, self.port, self.location)

    @property
    def isdlna(self) -> bool:
        """Bool dlna service"""
        dlna_tag = self.xmltree.device.find('dlna:x_dlnadoc')
        return dlna_tag is not None

    @property
    def scpd_action(self) -> List[ScpdActions]:
        """List of scpd actions"""
        action_list = []
        for service in self.xmltree.servicelist:
            location = self._base_url+service.scpdurl.text
            event_uri = service.eventsuburl.text
            control_uri = service.controlurl.text
            scpd = ScpdActions(location, control_uri, event_uri)
            action_list.append(scpd)
        return action_list

    @property
    def info(self) -> UPNPInfo:
        """UPNP information"""
        return UPNPInfo(self.xmltree)


def from_dict(services_dict: Dict[Tuple, HttpStream]) -> List[UPNPService]:
    """List of UPNPService from ssdp dictionary"""
    services_list = []
    for (host, port), response in services_dict.items():
        headers = response.headers()
        location = headers.get('location')
        service = UPNPService(host, port, location)
        services_list.append(service)
        LOG.debug(service)
    return services_list
