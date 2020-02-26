#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Files browser"""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from playlistcast import db


class File(graphene.ObjectType):
    """File"""
    name = graphene.String()
    is_directory = graphene.Boolean()


class ResourceAuth(SQLAlchemyObjectType):
    """ResourceAuth"""
    class Meta:
        """Describes ResourceAuth"""
        model = db.ResourceAuth
        interfaces = (db.Node, )


class ResourceAuthInput(graphene.InputObjectType):
    """ResourceAuthInput"""
    username = graphene.String(required=True)
    password = graphene.String(required=True)
