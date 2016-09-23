#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from BitVector.BitVector import BitVector

__author__ = 'Yh'


class userBit(object):
    def __init__(self, bit_size=10000000000):
        self.bit_array = BitVector(size=bit_size)

    def insert_user(self, user_id):
        try:
            id_ = int(user_id)
            self.bit_array[id_] = 1
        except TypeError:
            return None

    def is_user_exist(self, user_id):
        if self.bit_array[int(user_id)] == 0:
            return False
        return True
