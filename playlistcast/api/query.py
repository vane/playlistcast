#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
from typing import List
import graphene
from graphql_relay import from_global_id
from graphql.execution.base import ResolveInfo
from playlistcast import cache
from .model.firststart import FirstStart
from .model.resource_location import ResourceLocation
from .model.device import ChromecastDevice


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    hello = graphene.String()
    first_start = graphene.Field(FirstStart)

    resource_location_all = graphene.List(ResourceLocation)
    resource_location = graphene.Field(ResourceLocation, id=graphene.ID(required=True))

    chromecast_device_all = graphene.List(ChromecastDevice)

    def resolve_hello(self, info: ResolveInfo) -> str:
        """Return World from hello"""
        return "World"

    def resolve_playlist(self, info: ResolveInfo) -> str:
        """Return playlist"""
        return "foo"

    def resolve_first_start(self, info: ResolveInfo) -> FirstStart:
        """Is starting first time"""
        fs = FirstStart()
        fs.value = cache.FIRST_START
        return fs

    def resolve_resource_location_all(self, info: ResolveInfo) -> List[ResourceLocation]:
        """Return ResourceLocation list"""
        return ResourceLocation.get_query(info).all()

    def resolve_resource_location(self, info: ResolveInfo, id: graphene.ID) -> ResourceLocation:  # pylint: disable=W0622
        """Return ResourceLocation"""
        id = from_global_id(id)[1]
        return ResourceLocation.get_node(info, id)

    def resolve_chromecast_device_all(self, info: ResolveInfo) -> List[ChromecastDevice]:
        """List all chromecast devices"""
        output = [val.data for val in cache.CHROMECAST.values()]
        return output
