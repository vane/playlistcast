#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Database model"""
from graphene.relay.node import AbstractNode, NodeField
from graphql_relay import from_global_id, to_global_id
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True, echo=True)

session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))

Base = declarative_base()
# We will need this for querying
Base.query = session.query_property()

class ResourceLocation(Base):
    """ResourceLocation"""
    __tablename__ = 'resource_location'
    id = Column(Integer, primary_key=True) # pylint: disable=W0622
    name = Column(String, unique=True)
    location = Column(String)
    protocol = Column(String)
    auth = relationship('ResourceAuth', uselist=False, back_populates='location')

class ResourceAuth(Base):
    """ResourceAuthentication"""
    __tablename__ = 'resource_auth'
    id = Column(Integer, primary_key=True) # pylint: disable=W0622
    username = Column(String)
    password = Column(String)
    location_id = Column(Integer, ForeignKey('resource_location.id'))
    location = relationship("ResourceLocation", back_populates="auth")

# -
# Graphql node
# -
class Node(AbstractNode):
    """An object with an ID"""

    @classmethod
    def Field(cls, *args, **kwargs):  # noqa: N802
        """Field"""
        return NodeField(cls, *args, **kwargs)

    @classmethod
    def node_resolver(cls, only_type, root, info, id):  # pylint: disable=W0622
        """node_resolver"""
        return cls.get_node_from_global_id(info, id, only_type=only_type)

    @classmethod
    def get_node_from_global_id(cls, info, global_id, only_type=None):
        """get_node_from_global_id"""
        try:
            _type, _id = cls.from_global_id(global_id)
            graphene_type = info.schema.get_type(_type).graphene_type
        except Exception:
            return None

        if only_type:
            assert graphene_type == only_type, ("Must receive a {} id.").format(
                only_type._meta.name # pylint: disable=W0212
            )

        # We make sure the ObjectType implements the "Node" interface
        if cls not in graphene_type._meta.interfaces: # pylint: disable=W0212
            return None

        get_node = getattr(graphene_type, "get_node", None)
        if get_node:
            return get_node(info, _id)
        return None

    @classmethod
    def from_global_id(cls, global_id):
        """from_global_id"""
        return from_global_id(global_id)

    @classmethod
    def to_global_id(cls, type, id): # pylint: disable=W0622
        """to_global_id"""
        return to_global_id(type, id)

#Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
