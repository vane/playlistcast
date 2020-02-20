#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene


class Query(graphene.ObjectType):
    class Meta:
        description = 'Query'

    hello = graphene.String()

    def resolve_hello(self, info):
        return "World"
