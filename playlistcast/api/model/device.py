#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene
from graphql_relay import from_global_id, to_global_id
from .subscription import SubscriptionModel

class Device(graphene.ObjectType):
    id = graphene.ID()
    time = graphene.String()

class DeviceInput(graphene.InputObjectType):
    name = graphene.String(required=True)

class Post(graphene.Mutation):
    class Input:
        data = graphene.Argument(DeviceInput, required=True)

    Output = Device

    def mutate(self, info, data):
        SubscriptionModel.device.on_next(model)
        return model

class Put(graphene.Mutation):
    class Input:
        id = graphene.ID(required=True)
        data = graphene.Argument(DeviceInput, required=True)

    Output = Device

    def mutate(self, info, id, data):
        SubscriptionModel.device.on_next(model)
        return model

class Delete(graphene.Mutation):
    class Input:
        id = graphene.ID(required=True)

    Output = Device

    def mutate(self, info, id):
        SubscriptionModel.device.on_next(model)
        return model
