#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Cache - temporary before database introduction"""
from typing import Dict
from playlistcast import model

CHROMECAST: Dict[str, model.Device]  = dict()
