#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cache - temporary before database introduction"""
from typing import Dict
from .model import Device

FIRST_START = True

CHROMECAST: Dict[str, Device]  = dict()
