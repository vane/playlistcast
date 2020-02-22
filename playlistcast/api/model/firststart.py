#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""First start state"""
import graphene
from playlistcast.api import cache


class FirstStart(graphene.ObjectType):
    """FirstStart"""
    value = graphene.Boolean()


class FirstStartInput(graphene.InputObjectType):
    """FirstStartInput"""
    value = graphene.Boolean(required=True)


class Post(graphene.Mutation):
    """Post"""
    class Arguments:
        """Input argument"""
        data = graphene.Argument(FirstStartInput, required=True)

    Output = FirstStart

    def mutate(self, info, data):
        """Modify firststart value"""
        cache.FIRST_START = data.value
        firststart = FirstStart()
        firststart.value = cache.FIRST_START
        return firststart
