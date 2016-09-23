#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Yh'

import cmath
from BitVector import BitVector


class Bloom(object):
    def __init__(self, err_rate=0.000001, element_num=1000000):
        # 计算BitSet所需要的位数
        self.bit_num = -1 * element_num * cmath.log(err_rate) / (cmath.log(2) * cmath.log(2))

        # 四字节对齐
        self.bit_num = self.align_4byte(self.bit_num.real)

        # 分配内存
        self.bit_array = BitVector(size=self.bit_num)

        # 计算hash函数的个数
        hash_num_ = cmath.log(2) * self.bit_num / element_num
        self.hash_num = int(hash_num_.real) + 1

        # 产生hash函数的种子
        self.hash_seeds = self.generate_seeds(self.hash_num)

    # 插入数据
    def insert_element(self, element):
        """
        :param element:
        :return:
        """
        for seed in self.seeds:
            hash_value = abs(self.hash_element(element, seed))
            # 取模,防越界
            hash_value %= self.bit_num

            self.bit_array[hash_value] = 1

    # 检查数据是否存在
    def is_element_exist(self, element):
        """
        :param element:
        :return:
        """
        for seed in self.hash_seeds:
            hash_value = abs(self.hash_element(element, seed))
            hash_value %= self.bit_num

            if self.bit_array[hash_value] == 0:
                return False
        return True

    # 内存对齐
    @staticmethod
    def align_4byte(bit_num):
        """
        :param bit_num:
        :return:
        """
        num = 32 * (int(bit_num / 32) + 1)

        return num

    # 产生hash函数的种子
    @staticmethod
    def generate_seeds(hash_num):
        """
        :param hash_num:
        :return:
        """
        count = 0
        # 连续两个种子的最小差值
        gap = 50
        # 初始化hash种子为0
        hash_seeds = []
        for index in range(hash_num):
            hash_seeds.append(0)
        for index in range(10, 10000):
            max_num = int(cmath.sqrt(1.0 * index).real)
            flag = 1
            for num in range(2, max_num):
                if index % num == 0:
                    flag = 0
                    break

            if flag == 1:
                # 连续两个hash种子的差值要大才行
                if count > 0 and (index - hash_seeds[count - 1]) < gap:
                    continue
                hash_seeds[count] = index
                count += 1

            if count == hash_num:
                break
        return hash_seeds

    @staticmethod
    def hash_element(element, seed):
        """
        :param element:
        :param seed:
        :return:
        """
        hash_value = 1
        for ch in str(element):
            ch_value = ord(ch)
            hash_value = hash_value * seed + ch_value

        return hash_value
