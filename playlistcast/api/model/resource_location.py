#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resource location"""
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from graphql_relay import from_global_id
from playlistcast import db
from .resource import ResourceAuthInput
from .subscription import SubscriptionModel


class ResourceLocation(SQLAlchemyObjectType):
    """ResourceLocation"""
    class Meta:
        """Describes ResourceLocation"""
        model = db.ResourceLocation
        interfaces = (db.Node, )

class ResourceLocationInput(graphene.InputObjectType):
    """ResourceLocationInput"""
    name = graphene.String(required=True)
    location = graphene.String(reqiored=True)
    protocol = graphene.String(required=True)
    auth = ResourceAuthInput(required=False)

class Post(graphene.Mutation):
    """Add ResourceLocation"""
    class Arguments:
        """Add ResourceLocation arguments"""
        data = graphene.Argument(ResourceLocationInput, required=True)

    Output = ResourceLocation

    def mutate(self, info, data):
        """Add ResourceLocation"""
        model = db.ResourceLocation(name=data.name, location=data.location, protocol=data.protocol)
        db.session.add(model)
        db.session.commit()
        SubscriptionModel.resource_location.on_next(model)
        return model

class Put(graphene.Mutation):
    """Modify ResourceLocation"""
    class Arguments:
        """Modify ResourceLocation arguments"""
        id = graphene.ID(required=True)
        data = graphene.Argument(ResourceLocationInput, required=True)

    Output = ResourceLocation

    def mutate(self, info, id, data):
        """Modify ResourceLocation"""
        model_id = from_global_id(id)[1]
        model = ResourceLocation.get_query(info).get(model_id)
        if not model:
            raise RuntimeError("Invalid id {}".format(id))
        model.name = data.name
        model.location = data.location
        model.protocol = data.protocol
        db.session.commit()
        SubscriptionModel.resource_location.on_next(model)
        return model

class Delete(graphene.Mutation):
    """Delete resource location"""
    class Arguments:
        """Delete ResourceLocation arguments"""
        id = graphene.ID(required=True)

    Output = ResourceLocation

    def mutate(self, info, id):
        """Delete ResourceLocation"""
        model_id = from_global_id(id)[1]
        model = ResourceLocation.get_query(info).get(model_id)
        if not model:
            raise RuntimeError("Invalid id {}".format(id))
        db.session.delete(model)
        db.session.commit()
        SubscriptionModel.resource_location.on_next(model)
        return model
