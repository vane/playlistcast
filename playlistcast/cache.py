#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cache - temporary before database introduction"""
from typing import Dict
from .model import Device

CHROMECAST: Dict[str, Device]  = dict()
