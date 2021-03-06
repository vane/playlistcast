#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscriptions management"""
import graphene
from rx.subjects import Subject


class TimeMessage(graphene.ObjectType):
    """TimeMessage"""
    id = graphene.ID()
    time = graphene.DateTime()


class SubscriptionModel:
    """SubscriptionModel"""
    chromecast = Subject()
    media_status = Subject()
    resource_location = Subject()
    time = Subject()
