#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging

__author__ = 'Yh'

weibo_log_file = 'log/weibo.log'
lecture_log_fmt = '%(asctime)s : %(name)s - %(message)s'

weibo_logger = logging.getLogger('lecture_log')
weibo_handler = logging.handlers.RotatingFileHandler(weibo_log_file,
                                                               maxBytes=1024 * 1024,
                                                               encoding='utf-8',
                                                               backupCount=5)
weibo_fmt = logging.Formatter(lecture_log_fmt)
weibo_handler.setFormatter(weibo_fmt)

weibo_logger.addHandler(weibo_handler)
weibo_logger.setLevel(logging.INFO)

def get_weibo_log():
    return weibo_logger