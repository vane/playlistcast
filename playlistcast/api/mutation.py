#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mutation"""
import graphene
from .model import resource_location, device


class Mutation(graphene.ObjectType):
    """Mutation"""
    class Meta:
        """API Description"""
        description = 'Mutation'

    resourceLocationAdd = resource_location.Add.Field()
    resourceLocationChange = resource_location.Change.Field()
    resourceLocationDelete = resource_location.Delete.Field()

    chromecastPause = device.ChromecastPause.Field()
