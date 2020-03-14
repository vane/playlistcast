#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Playlist api"""
from typing import Dict
import graphene
from graphql.execution.base import ResolveInfo
from playlistcast import db, error
from playlistcast.protocol import m3u
from .chromecast import CHROMECAST, ChromecastDevice

class PlaylistItem(graphene.ObjectType):
    """Single playlist item"""
    index = graphene.Int()
    name = graphene.String()
    path = graphene.String()


class PlaylistPlayOptions(graphene.InputObjectType):
    """Playlist play options"""
    uid = graphene.String(required=True)
    name = graphene.String(required=True)
    path = graphene.String(required=True)
    index = graphene.Int()

class PlaylistPlay(graphene.Mutation):
    """Play playlist on chromecast device"""
    class Arguments:
        """Play chromecast uid"""
        uid = graphene.String(required=True)
        name = graphene.String(required=True)

    Output = graphene.Boolean

    def mutate(self, info: ResolveInfo, options: PlaylistPlayOptions) -> graphene.Boolean: # pylint: disable=W0622
        """Method to play playlist on chromecast"""
        model = db.session.query(db.ResourceLocation)\
            .filter(db.ResourceLocation.name == options.name).first()
        if not model:
            raise error.ResourcePathError('Invalid path {}'.format(options.name))
        if options.uid not in CHROMECAST:
            raise error.ChromecastUUIDError(options.uid)
        # create new playlist or use existing one
        if PLAYLIST[options.uid] is not None:
            playlist = PLAYLIST[options.uid]
            p = playlist.playlist
        else:
            p = m3u.M3UPlaylist()
            p.load(model.location, options.path)
            data = CHROMECAST[options.uid]
            playlist = Playlist(playlist=p, chromecast=data)
            PLAYLIST[options.uid] = playlist
        # deal with change status
        mc = playlist.chromecast.device.media_controller
        if mc.is_playing:
            mc.stop()
        if options.index:
            p.set_index(options.index)
        # urlpath = f'http://{util.get_ip()}/{config.PORT}/resource/'
        # urlpath += f'{options.name}/{m3udir}/{p.current_item.path}'
        playlist.device.media_controller.play_media(p.current_item.path)
        return True

# HELPER
class Playlist:
    """Playlist with api and interface data"""
    def __init__(self, playlist: m3u.M3UPlaylist, chromecast: ChromecastDevice):
        self.playlist = playlist
        self.chromecast = chromecast

PLAYLIST: Dict[str, Playlist] = dict()
