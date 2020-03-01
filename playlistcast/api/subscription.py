#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscription"""
import graphene
from .model.subscription import TimeMessage, SubscriptionModel
from .model.device import MediaStatus

class Subscription(graphene.ObjectType):
    """Subscription"""
    class Meta:
        """API Description"""
        description = 'Subscriptions'

    time = graphene.Field(TimeMessage)
    media_status = graphene.Field(MediaStatus)

    def resolve_time(self, info):
        """Time subscription"""
        return SubscriptionModel.time

    def resolve_media_status(self, info):
        """MediaStatus subscription"""
        return SubscriptionModel.media_status
