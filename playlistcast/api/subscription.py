#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene
from .model.subscription import TimeMessage, SubscriptionModel
from .model import device

class Subscription(graphene.ObjectType):
    class Meta:
        description = 'Subscriptions'

    time = graphene.Field(TimeMessage)

    device = graphene.Field(device.Device)

    def resolve_time(self, info):
        return SubscriptionModel.time

    def resolve_device(self, info):
        return SubscriptionModel.device
