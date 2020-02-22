#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Services"""
import graphene


class UPNPService(graphene.ObjectType):
    """UPNPService"""
    id = graphene.ID()
    serviceType = graphene.String()
    serviceId = graphene.String()
    controlURL = graphene.String()
    eventSubURL = graphene.String()
    SCPDURL = graphene.String()
