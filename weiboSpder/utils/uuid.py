#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import uuid

__author__ = 'Yh'


def get_uuid():
    u = uuid.uuid1()
    return u.hex
