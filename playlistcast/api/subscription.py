#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscription"""
import graphene
from .model.subscription import TimeMessage, SubscriptionModel

class Subscription(graphene.ObjectType):
    """Subscription"""
    class Meta:
        """API Description"""
        description = 'Subscriptions'

    time = graphene.Field(TimeMessage)

    def resolve_time(self, info):
        """Time subscription"""
        return SubscriptionModel.time
