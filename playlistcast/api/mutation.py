#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mutation"""
import graphene
from .model import resource_location, chromecast


class Mutation(graphene.ObjectType):
    """Mutation"""
    class Meta:
        """API Description"""
        description = 'Mutation'

    resourceLocationAdd = resource_location.Add.Field()
    resourceLocationChange = resource_location.Change.Field()
    resourceLocationDelete = resource_location.Delete.Field()

    chromecastPause = chromecast.ChromecastPause.Field()
    chromecastPlay = chromecast.ChromecastPlay.Field()
    chromecastVolumeChange = chromecast.ChromecastVolumeChange.Field()
    chromecastSeek = chromecast.ChromecastSeek.Field()
