#!/usr/bin/env python
# -*- coding: utf-8 -*-
""""UPNPDevice model"""
import graphene
from .service import UPNPService

class CastStatus(graphene.ObjectType):
    """Chromecast CastStatus"""
    app_id = graphene.String()
    display_name = graphene.String()
    icon_url = graphene.String()
    is_active_input = graphene.Boolean()
    is_stand_by = graphene.Boolean()
    status_text = graphene.String()

class MediaStatus(graphene.ObjectType):
    """Chromecast MediaStatus"""
    adjusted_current_time = graphene.Int()
    album_artist = graphene.String()
    album_name = graphene.String()
    artist = graphene.String()
    content_id = graphene.String()
    content_type = graphene.String()
    current_time = graphene.Int()
    duration = graphene.Int()
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
    app_id = graphene.String()
    is_active = graphene.Boolean()
    is_idle = graphene.Boolean()
    is_paused = graphene.Boolean()
    is_playing = graphene.Boolean()
    media_session_id = graphene.Int()
    status = graphene.Field(MediaStatus)

class ChromecastDevice(graphene.ObjectType):
    """Chromecast Device"""
    name = graphene.String()
    uuid = graphene.String()
    is_idle = graphene.Boolean()
    uri = graphene.String()
    host = graphene.String()
    port = graphene.Int()
    media_controller = graphene.Field(MediaController)


class UPNPDevice(graphene.ObjectType):
    """UPNPDevice"""
    id = graphene.ID()
    deviceType = graphene.String()
    friendlyName = graphene.String()
    manufacturer = graphene.String()
    modelName = graphene.String()
    UDN = graphene.String()
    serviceList = graphene.List(UPNPService)
