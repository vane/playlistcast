#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscription"""
import graphene
from .model.subscription import TimeMessage, SubscriptionModel
from .model import upnpdevice

class Subscription(graphene.ObjectType):
    """Subscription"""
    class Meta:
        """API Description"""
        description = 'Subscriptions'

    time = graphene.Field(TimeMessage)

    device = graphene.Field(upnpdevice.UPNPService)

    def resolve_time(self, info):
        """Time subscription"""
        return SubscriptionModel.time

    def resolve_device(self, info):
        """Device subscription"""
        return SubscriptionModel.device
