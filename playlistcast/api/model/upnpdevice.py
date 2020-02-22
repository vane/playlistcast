#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""UPNPDevice model"""
import graphene
from .icon import Icon
from .service import UPNPService

class UPNPDevice(graphene.ObjectType):
    """UPNPDevice"""
    id = graphene.ID()
    deviceType = graphene.String()
    friendlyName = graphene.String()
    manufacturer = graphene.String()
    modelName = graphene.String()
    UDN = graphene.String()
    icon = Icon()
    serviceList = graphene.List(UPNPService)
