#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
from typing import List
import graphene
from graphql_relay import from_global_id
from graphql.execution.base import ResolveInfo
from playlistcast.api import cache
from .model.firststart import FirstStart
from .model.resource_location import ResourceLocation


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    hello = graphene.String()
    firstStart = graphene.Field(FirstStart)

    all_resource_location = graphene.List(ResourceLocation)
    resource_location = graphene.Field(ResourceLocation, id=graphene.ID(required=True))

    def resolve_hello(self, info: ResolveInfo) -> str:
        """Return World from hello"""
        return "World"

    def resolve_playlist(self, info: ResolveInfo) -> str:
        """Return playlist"""
        return "foo"

    def resolve_firstStart(self, info: ResolveInfo) -> FirstStart:
        """Is starting first time"""
        fs = FirstStart()
        fs.value = cache.FIRST_START
        return fs

    def resolve_all_resource_location(self, info):
        """Return ResourceLocation list"""
        return ResourceLocation.get_query(info).all()

    def resolve_resource_location(self, info, id):
        """Return ResourceLocation"""
        id = from_global_id(id)[1]
        return ResourceLocation.get_node(info, id)
