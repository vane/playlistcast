#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mutation"""
import graphene
from .model import resource_location, chromecast, playlist


class Mutation(graphene.ObjectType):
    """Mutation"""
    class Meta:
        """API Description"""
        description = 'Mutation'

    resource_location_add = resource_location.Add.Field()
    resource_location_change = resource_location.Change.Field()
    resource_location_delete = resource_location.Delete.Field()

    chromecast_pause = chromecast.ChromecastPause.Field()
    chromecast_play = chromecast.ChromecastPlay.Field()
    chromecast_volume_change = chromecast.ChromecastVolumeChange.Field()
    chromecast_seek = chromecast.ChromecastSeek.Field()

    playlist_play = playlist.PlaylistPlay.Field()
    playlist_play_index = playlist.PlaylistPlayIndex.Field()
