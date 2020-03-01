#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mutation"""
import graphene
from .model import firststart
from .model import resource_location


class Mutation(graphene.ObjectType):
    """Mutation"""
    class Meta:
        """API Description"""
        description = 'Mutation'

    postFirstStart = firststart.Post.Field()

    resourceLocationAdd = resource_location.Add.Field()
    resourceLocationChange = resource_location.Change.Field()
    resourceLocationDelete = resource_location.Delete.Field()
