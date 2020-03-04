#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
from typing import List
import graphene
from graphql_relay import from_global_id
from graphql.execution.base import ResolveInfo
from playlistcast import cache
from .model.resource_location import ResourceLocation
from .model.device import ChromecastDevice


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    resource_location_all = graphene.List(ResourceLocation)
    resource_location = graphene.Field(ResourceLocation, id=graphene.ID(required=True))

    chromecast_device_all = graphene.List(ChromecastDevice)

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
