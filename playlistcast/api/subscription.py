#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscription"""
import graphene
from graphql.execution.base import ResolveInfo
from .model.subscription import TimeMessage, SubscriptionModel
from .model.device import MediaStatus,ChromecastDevice

class Subscription(graphene.ObjectType):
    """Subscription"""
    class Meta:
        """API Description"""
        description = 'Subscriptions'

    time = graphene.Field(TimeMessage)
    media_status = graphene.Field(MediaStatus)
    chromecast = graphene.Field(ChromecastDevice)

    def resolve_time(self, info: ResolveInfo) -> TimeMessage:
        """Time subscription"""
        return SubscriptionModel.time

    def resolve_media_status(self, info: ResolveInfo) -> MediaStatus:
        """MediaStatus subscription"""
        return SubscriptionModel.media_status

    def resolve_chromecast(self, info: ResolveInfo) -> ChromecastDevice:
        """ChromecastDevice subscription"""
        return SubscriptionModel.chromecast
