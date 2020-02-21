#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene
from rx.subjects import Subject


class TimeMessage(graphene.ObjectType):
    id = graphene.ID()
    time = graphene.DateTime()


class SubscriptionModel:
    time = Subject()
    device = Subject()
