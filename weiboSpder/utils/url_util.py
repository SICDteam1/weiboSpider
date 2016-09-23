#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Yh'


# 拼接评论Url
def get_comment_url(m_id, page_num):
    base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6'

    import time
    now_time = str(time.time()).replace('.', '')[:-3]
    comment_data = {
        'id': m_id,
        'page': page_num,
        '__rnd': now_time
    }
    if page_num == 1:
        comment_data.pop('page')
    for key, value in comment_data.items():
        base_url = str(base_url) + '&' + str(key) + '=' + str(value)

    return base_url


# 获取关注列表下一页的链接，只允许访问5页
def get_concern_url(page):
    # if page > 5: # 微博只允许爬取前五页
    #     return None

    url = '?relate=fans&page=' + str(page) + '#Pl_Official_HisRelation__64'
    return url


# 获取粉丝列表的下一页链接
def get_fans_url(page):
    # if page > 5:  # 微博只允许爬取前五页
    #     return None

    url = '?pids=Pl_Official_HisRelation__64&page=' \
         + str(page) \
         + '#Pl_Official_HisRelation__64'
    return url
