#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Subscriptions management"""
import graphene
from rx.subjects import Subject


class TimeMessage(graphene.ObjectType):
    """TimeMessage"""
    # pylint: disable=R0903
    id = graphene.ID()
    time = graphene.DateTime()


class SubscriptionModel:
    """SubscriptionModel"""
    # pylint: disable=R0903
    time = Subject()
    device = Subject()
