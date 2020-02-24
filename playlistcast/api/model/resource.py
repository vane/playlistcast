#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Files browser"""
import graphene


class File(graphene.ObjectType):
    """File"""
    name = graphene.String()
    is_directory = graphene.Boolean()


class ResourceAuth(graphene.ObjectType):
    """ResourceAuth"""
    username = graphene.String()
    password = graphene.String()


class ResourceAuthInput(graphene.InputObjectType):
    """ResourceAuthInput"""
    username = graphene.String(required=True)
    password = graphene.String(required=True)
