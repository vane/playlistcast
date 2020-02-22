#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Query"""
import graphene


class Query(graphene.ObjectType):
    """Query"""
    class Meta:
        """API Description"""
        description = 'Query'

    hello = graphene.String()

    def resolve_hello(self, info):
        """Return World from hello"""
        return "World"

    def resolve_playlist(self, info):
        """Return playlist"""
        return "foo"
