#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resource location"""
import graphene
from playlistcast.api import cache
from .resource import ResourceAuth, ResourceAuthInput
from .subscription import SubscriptionModel


class ResourceLocation(graphene.ObjectType):
    """ResourceLocation"""
    id = graphene.ID()
    name = graphene.String()
    location = graphene.String()
    protocol = graphene.String()
    authentication = ResourceAuth()

class ResourceLocationInput(graphene.InputObjectType):
    """ResourceLocationInput"""
    name = graphene.String(required=True)
    location = graphene.String(reqiored=True)
    protocol = graphene.String(required=True)
    authenticaiton = ResourceAuthInput()

class Post(graphene.Mutation):
    """Add ResourceLocation"""
    class Arguments:
        """Add ResourceLocation arguments"""
        data = graphene.Argument(ResourceLocationInput, required=True)

    Output = ResourceLocation

    def mutate(self, info, data):
        """Add ResourceLocation"""
        model = ResourceLocation()
        if data.name in cache.RESOURCE_LOCATION:
            raise RuntimeError("Name {} already exists invalid method POST should use PUT".format(data.name))
        cache.INDEX += 1
        model.id = cache.INDEX
        model.name = data.name
        model.location = data.location
        model.protocol = data.protocol
        cache.RESOURCE_LOCATION[data.name] = model
        SubscriptionModel.resource_location.on_next(model)
        return model

class Put(graphene.Mutation):
    """Modify ResourceLocation"""
    class Arguments:
        """Modify ResourceLocation arguments"""
        name = graphene.String(required=True)
        data = graphene.Argument(ResourceLocationInput, required=True)

    Output = ResourceLocation

    def mutate(self, info, name, data):
        """Modify ResourceLocation"""
        if name not in cache.RESOURCE_LOCATION:
            raise RuntimeError("Invalid name {}".format(name))
        model = cache.RESOURCE_LOCATION[name]
        model.name = data.name
        model.location = data.location
        model.protocol = data.protocol
        SubscriptionModel.resource_location.on_next(model)
        return model

class Delete(graphene.Mutation):
    """Delete resource location"""
    class Arguments:
        """Delete ResourceLocation arguments"""
        name = graphene.String(required=True)

    Output = ResourceLocation

    def mutate(self, info, name):
        """Delete ResourceLocation"""
        if name not in cache.RESOURCE_LOCATION:
            raise RuntimeError("Invalid name {}".format(name))
        model = cache.RESOURCE_LOCATION[name]
        del cache.RESOURCE_LOCATION[name]
        SubscriptionModel.resource_location.on_next(model)
        return model
