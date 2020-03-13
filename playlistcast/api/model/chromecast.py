#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""Device model"""
import asyncio
import graphene
import pychromecast
from typing import Dict
from pychromecast.controllers import media
from graphql.execution.base import ResolveInfo
from playlistcast import error, util
from .subscription import SubscriptionModel

class SubtitleTrack(graphene.ObjectType):
    """Chromecast MediaStatus SubtitleTrack"""
    trackId = graphene.Int()
    type = graphene.String()
    language = graphene.String()

class CastStatus(graphene.ObjectType):
    """Chromecast CastStatus"""
    uuid = graphene.String()
    app_id = graphene.String()
    display_name = graphene.String()
    icon_url = graphene.String()
    is_active_input = graphene.Boolean()
    is_stand_by = graphene.Boolean()
    status_text = graphene.String()
    volume_level = graphene.Float()
    volume_muted = graphene.Boolean()

class MediaStatus(graphene.ObjectType):
    """Chromecast MediaStatus"""
    uuid = graphene.String()
    adjusted_current_time = graphene.Int()
    album_artist = graphene.String()
    album_name = graphene.String()
    artist = graphene.String()
    content_id = graphene.String()
    content_type = graphene.String()
    current_time = graphene.Float()
    duration = graphene.Float()
    episode = graphene.String()
    idle_reason = graphene.String()
    last_updated = graphene.String()
    media_is_generic = graphene.Boolean()
    media_is_movie = graphene.Boolean()
    media_is_musictrack = graphene.Boolean()
    media_is_photo = graphene.Boolean()
    media_is_tvshow = graphene.Boolean()
    media_session_id = graphene.String()
    playback_rate = graphene.Int()
    player_is_idle = graphene.Boolean()
    player_is_paused = graphene.Boolean()
    player_is_playing = graphene.Boolean()
    player_state = graphene.String()
    season = graphene.String()
    series_title = graphene.String()
    stream_type = graphene.String()
    stream_type_is_buffered = graphene.Boolean()
    stream_type_is_live = graphene.Boolean()
    subtitle_tracks = graphene.List(of_type=SubtitleTrack)
    supports_pause = graphene.Boolean()
    supports_queue_next = graphene.Boolean()
    supports_queue_prev = graphene.Boolean()
    supports_seek = graphene.Boolean()
    supports_skip_backward = graphene.Boolean()
    supports_skip_forward = graphene.Boolean()
    supports_stream_mute = graphene.Boolean()
    supports_stream_volume = graphene.Boolean()
    title = graphene.String()
    track = graphene.String()
    volume_level = graphene.Int()
    volume_muted = graphene.Boolean()

class MediaController(graphene.ObjectType):
    """Chromecast MediaController"""
    uuid = graphene.String()
    app_id = graphene.String()
    is_active = graphene.Boolean()
    is_idle = graphene.Boolean()
    is_paused = graphene.Boolean()
    is_playing = graphene.Boolean()
    media_session_id = graphene.Int()
    status = graphene.Field(MediaStatus)

class ChromecastModel(graphene.ObjectType):
    """Chromecast Device"""
    name = graphene.String()
    uuid = graphene.String()
    is_idle = graphene.Boolean()
    uri = graphene.String()
    host = graphene.String()
    port = graphene.Int()
    media_controller = graphene.Field(MediaController)
    status = graphene.Field(CastStatus)

# MUTATIONS

class ChromecastPause(graphene.Mutation):
    """Pause chromecast device"""
    class Arguments:
        """Pause chromecast uid"""
        uid = graphene.String(required=True)

    Output = graphene.Boolean

    def mutate(self, info: ResolveInfo, uid: graphene.String) -> graphene.Boolean: # pylint: disable=W0622
        """Method to pause chromecast"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid)
        data = CHROMECAST[uid]
        data.device.media_controller.pause()
        return True

class ChromecastPlay(graphene.Mutation):
    """Play chromecast device"""
    class Arguments:
        """Play chromecast uid"""
        uid = graphene.String(required=True)

    Output = graphene.Boolean

    def mutate(self, info: ResolveInfo, uid: graphene.String) -> graphene.Boolean: # pylint: disable=W0622
        """Method to play chromecast"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid)
        data = CHROMECAST[uid]
        data.device.media_controller.play()
        return True

class ChromecastVolumeChange(graphene.Mutation):
    """Chromecast volume change"""
    class Arguments:
        """Chromecast volume change uid and volume float value"""
        uid = graphene.String(required=True)
        volume = graphene.Float(required=True)

    Output = graphene.Boolean

    def mutate(self,
               info: ResolveInfo,
               uid: graphene.String,
               volume: graphene.Float) -> graphene.Boolean: # pylint: disable=W0622
        """Method to volume change uid and volume float value"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid=uid)
        data = CHROMECAST[uid]
        if volume > 1:
            raise error.ChromecastVolumeError(volume=volume)
        data.device.set_volume(volume)
        return True

class ChromecastSeek(graphene.Mutation):
    """Chromecast volume change"""
    class Arguments:
        """Chromecast volume change uid and volume float value"""
        uid = graphene.String(required=True)
        value = graphene.Float(required=True)

    Output = graphene.Boolean

    def mutate(self,
               info: ResolveInfo,
               uid: graphene.String,
               value: graphene.Float) -> graphene.Boolean: # pylint: disable=W0622
        """Method to volume change uid and volume float value"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid=uid)
        data = CHROMECAST[uid]
        data.device.media_controller.seek(value)
        return True

class ChromecastSubtitleEnable(graphene.Mutation):
    """Chromecast subtitle enable"""
    class Arguments:
        """Chromecast subtitle enable uid and track_id int value"""
        uid = graphene.String(required=True)
        track_id = graphene.Int(required=True)

    Output = graphene.Boolean

    def mutate(self,
               info: ResolveInfo,
               uid: graphene.String,
               track_id:graphene.Int) -> graphene.Boolean:
        """Method to change subtitle track"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid=uid)
        data = CHROMECAST[uid]
        data.device.media_controller.enable_subtitle()
        return True

class ChromecastSubtitleDisable(graphene.Mutation):
    """Chromecast subtitle disable"""
    class Arguments:
        """Chromecast subtitle disable uid"""
        uid = graphene.String(required=True)

    Output = graphene.Boolean

    def mutate(self,
               info: ResolveInfo,
               uid: graphene.String) -> graphene.Boolean:
        """Disable subtitles"""
        if uid not in CHROMECAST:
            raise error.ChromecastUUIDError(uid=uid)
        data = CHROMECAST[uid]
        data.device.media_controller.disable_subtitle()
        return True
# HELPER CLASSES

class ChromecastDevice:
    """Device with api and interface data"""
    def __init__(self, device: pychromecast.Chromecast, data: ChromecastModel):
        self.device = device
        self.data = data
        self.device.media_controller.register_status_listener(self)

    def ensure_in_loop(self):
        """Tries to get asyncio loop and creates one if not exists"""
        try:
            asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

    def new_media_status(self, status: media.MediaStatus):
        """Subscribe for chromecast status messages"""
        s = util.convert(status, MediaStatus, ('uuid','subtitle_tracks'))
        subtitle_tracks = list()
        for tr in status.subtitle_tracks:
            if 'type' in tr and tr['type'] == 'TEXT':
                subtitle_track = util.convert(tr, SubtitleTrack)
                subtitle_tracks.append(subtitle_track)
        s.subtitle_tracks = subtitle_tracks
        s.uuid = self.data.uuid
        self.ensure_in_loop()
        self.data.media_controller.status = s
        SubscriptionModel.media_status.on_next(s)
        print(self.data.name, self.data.uuid, status)

CHROMECAST: Dict[str, ChromecastDevice] = dict()
