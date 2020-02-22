#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
import graphene
from graphql.execution.base import ResolveInfo
from playlistcast.api import cache
from .model.firststart import FirstStart


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    hello = graphene.String()
    firstStart = graphene.Field(FirstStart)

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
