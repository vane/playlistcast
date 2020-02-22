#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Mutation"""
import graphene
from .model import firststart


class Mutation(graphene.ObjectType):
    """Mutation"""
    class Meta:
        """API Description"""
        description = 'Mutations'

    postFirstStart = firststart.Post.Field()
