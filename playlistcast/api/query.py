#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
import os
from pathlib import Path
from typing import List
import graphene
from graphql_relay import from_global_id
from graphql.execution.base import ResolveInfo
from playlistcast import util, db, config, error
from playlistcast.protocol import m3u
from .model.resource_location import ResourceLocation, Directory, File
from .model.chromecast import ChromecastModel, CastStatus, CHROMECAST
from .model.playlist import PlaylistItem


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    resource_location_all = graphene.List(ResourceLocation)
    resource_location = graphene.Field(ResourceLocation, id=graphene.ID(required=True))

    list_directory = graphene.Field(
        Directory,
        name=graphene.String(required=True),
        subpath=graphene.String()
    )

    chromecast_device_all = graphene.List(ChromecastModel)

    playlist_items = graphene.Field(
        graphene.List(PlaylistItem),
        name=graphene.String(required=True),
        path=graphene.String(required=True)
    )

    def resolve_resource_location_all(self, info: ResolveInfo) -> List[ResourceLocation]:
        """Return ResourceLocation list"""
        return ResourceLocation.get_query(info).all()

    def resolve_resource_location(self, info: ResolveInfo, id: graphene.ID) -> ResourceLocation:  # pylint: disable=W0622
        """Return ResourceLocation"""
        id = from_global_id(id)[1]
        return ResourceLocation.get_node(info, id)

    def resolve_list_directory(self, info: ResolveInfo, name: graphene.String, subpath: graphene.String = '') -> Directory:
        """ Browse directories
            name - ResourceLocation -> name
            subpath - string path of current directory
        """
        model = db.session.query(db.ResourceLocation).filter(db.ResourceLocation.name == name).first()
        if not model:
            raise error.ResourcePathError('Invalid path {}'.format(name))
        d = Directory()
        d.resource_name = name
        d.resource_path = '/resource/{}/{}'.format(name, subpath)
        d.subpath = subpath
        path = os.path.join(model.location, subpath)
        if not os.path.exists(path):
            raise error.ResourcePathError('Path not exists {}'.format(path))
        if not os.path.isdir(path):
            raise error.ResourcePathError('Path is not directory {}'.format(path))
        files = list()
        for fname in sorted(os.listdir(path)):
            p = Path(os.path.join(path, fname))
            stat = p.stat()
            f = File(name=fname, size=stat.st_size, is_dir=p.is_dir(), suffix=p.suffix)
            files.append(f)
        d.files = files
        return d

    def resolve_chromecast_device_all(self, info: ResolveInfo) -> List[ChromecastModel]:
        """List all chromecast models"""
        output = []
        for val in CHROMECAST.values():
            # update model
            cs = util.convert(val.device.status, CastStatus, ('media_controller', 'status', 'uuid'))
            cs.uuid = val.data.uuid
            val.data.status = cs
            output.append(val.data)
        return output

    def resolve_playlist_items(self, info: ResolveInfo, name: graphene.String, path: graphene.String) -> List[PlaylistItem]:
        """Get list of playlist items"""
        model = db.session.query(db.ResourceLocation).filter(db.ResourceLocation.name == name).first()
        if not model:
            raise error.ResourcePathError('Invalid path {}'.format(name))
        playlist = m3u.M3UPlaylist()
        m3udir = playlist.load(model.location, path)
        output = list()
        for p in playlist.items:
            urlpath = 'http://'+util.get_ip()+':'+str(config.PORT)+'/resource/'+name+'/'+str(m3udir)+'/'+p.path
            item = PlaylistItem(index=p.index, name=p.name, path=urlpath)
            output.append(item)
        return output
