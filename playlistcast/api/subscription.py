#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscription"""
import graphene
from graphql.execution.base import ResolveInfo
from .model.subscription import TimeMessage, SubscriptionModel
from .model.chromecast import MediaStatus,ChromecastModel

class Subscription(graphene.ObjectType):
    """Subscription"""
    class Meta:
        """API Description"""
        description = 'Subscriptions'

    time = graphene.Field(TimeMessage)
    media_status = graphene.Field(MediaStatus)
    chromecast = graphene.Field(ChromecastModel)

    def resolve_time(self, info: ResolveInfo) -> TimeMessage:
        """Time subscription"""
        return SubscriptionModel.time

    def resolve_media_status(self, info: ResolveInfo) -> MediaStatus:
        """MediaStatus subscription"""
        return SubscriptionModel.media_status

    def resolve_chromecast(self, info: ResolveInfo) -> ChromecastModel:
        """ChromecastModel subscription"""
        return SubscriptionModel.chromecast
