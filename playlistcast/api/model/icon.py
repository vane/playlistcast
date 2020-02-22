#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Icon"""
import graphene


class Icon(graphene.ObjectType):
    """Icon"""
    id = graphene.ID()
    mimetype = graphene.String()
    width = graphene.String()
    height = graphene.String()
    depth = graphene.String()
    url = graphene.String()
