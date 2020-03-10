#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
import os
from pathlib import Path
from typing import List
import graphene
from graphql_relay import from_global_id
from graphql.execution.base import ResolveInfo
from playlistcast import util, db
from .model.resource_location import ResourceLocation, Directory, File
from .model.chromecast import ChromecastModel, CastStatus, CHROMECAST


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    resource_location_all = graphene.List(ResourceLocation)
    resource_location = graphene.Field(ResourceLocation, id=graphene.ID(required=True))

    list_directory = graphene.Field(Directory, name=graphene.String(required=True), subpath=graphene.String())

    chromecast_device_all = graphene.List(ChromecastModel)

    def resolve_resource_location_all(self, info: ResolveInfo) -> List[ResourceLocation]:
        """Return ResourceLocation list"""
        return ResourceLocation.get_query(info).all()

    def resolve_resource_location(self, info: ResolveInfo, id: graphene.ID) -> ResourceLocation:  # pylint: disable=W0622
        """Return ResourceLocation"""
        id = from_global_id(id)[1]
        return ResourceLocation.get_node(info, id)

    def resolve_list_directory(self, info: ResolveInfo, name: graphene.String, subpath: graphene.String = '') -> Directory:
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
            cs = CastStatus()
            cs.uuid = val.data.uuid
            util.convert(val.device.status, cs, ('media_controller', 'status', 'uuid'))
            val.data.status = cs
            output.append(val.data)
        return output
