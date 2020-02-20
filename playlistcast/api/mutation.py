#!/usr/bin/env python
# -*- coding: utf-8 -*-
import graphene
from .model import device


class Mutation(graphene.ObjectType):
    class Meta:
        description = 'Mutations'

    postDevice = device.Post.Field()
    putDevice = device.Put.Field()
    delDevice = device.Delete.Field()
