#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Playlist information"""
import graphene


class PlayIndex(graphene.ObjectType):
    """PlayIndex"""
    start = graphene.Int()
    end = graphene.Int()
    current = graphene.Int()


class Playlist(graphene.ObjectType):
    """Playlist"""
    basepath = graphene.String()
    path = graphene.String()
    name = graphene.String()
    index = PlayIndex()


class PlaylistInfo(graphene.ObjectType):
    """PlaylistInfo"""
    location = graphene.String()
    name = graphene.String()
