#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene
from typing import Dict
from graphql.execution.base import ResolveInfo
from .chromecast import CHROMECAST, ChromecastDevice
from playlistcast.protocol import m3u

class PlaylistItem(graphene.ObjectType):
    index = graphene.Int()
    name = graphene.String()
    path = graphene.String()

class PlaylistPlay(graphene.Mutation):
    """Play playlist on chromecast device"""
    class Arguments:
        """Play chromecast uid"""
        uid = graphene.String(required=True)
        playlist_path = graphene.String(required=True)

    Output = graphene.Boolean

    def mutate(self, info: ResolveInfo, uid: graphene.String, playlist_path: graphene.String) -> graphene.Boolean: # pylint: disable=W0622
        """Method to play playlist on chromecast"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid)
        data = CHROMECAST[uid]
        if data.device.media_controller.is_playing:
            data.device.media_controller.stop()
        playlist = m3u.M3UPlaylist()
        playlist.load(playlist_path)
        PLAYLIST[uid] = playlist
        data.device.media_controller.play_media(playlist.current_item.path)
        return True

class PlaylistPlayIndex(graphene.Mutation):
    """Play playlist on chromecast device"""
    class Arguments:
        """Play chromecast uid"""
        uid = graphene.String(required=True)
        playlist_path = graphene.String(required=True)
        index = graphene.Int(required=True)

    Output = graphene.Boolean

    def mutate(self, info: ResolveInfo, uid: graphene.String, playlist_path: graphene.String, index: graphene.Int) -> graphene.Boolean: # pylint: disable=W0622
        """Method to play playlist on chromecast"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid)
        data = CHROMECAST[uid]
        if PLAYLIST[uid] is not None:
            playlist = PLAYLIST[uid].playlist
        else:
            playlist = m3u.M3UPlaylist()
            playlist.load(playlist_path)
            PLAYLIST[uid] = Playlist(playlist=playlist, chromecast=data)
        if data.device.media_controller.is_playing:
            data.device.media_controller.stop()
        idx = playlist.index
        idx.current = index
        return True

class Playlist:
    def __init__(self, playlist: m3u.M3UPlaylist, chromecast: ChromecastDevice):
        self.playlist = playlist
        self.chromecast = chromecast

PLAYLIST: Dict[str, Playlist] = dict()
