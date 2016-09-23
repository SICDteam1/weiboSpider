#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

from weiboSpder import items
from weiboSpder.spiders import settings
from weiboSpder.spiders.get_info import get_userItem, get_blogs, get_comment, get_userID_from_mainPage, \
    get_concern_user_list, get_fans_user_list

import re

import scrapy
from scrapy import Request
from scrapy.spiders import CrawlSpider

from weiboSpder.spiders.login_api import get_login_cookie
from weiboSpder.utils.url_util import get_comment_url, get_concern_url, get_fans_url
from weiboSpder.utils.user_bit import userBit
from weiboSpder.utils.uuid import get_uuid
from weiboSpder.utils.weibo_log import get_weibo_log

__author__ = 'Yh'


class WeiboSpider(CrawlSpider):
    name = 'weibo'
    allowed_domains = [
        'weibo.com'
    ]
    start_urls = [
        'http://www.weibo.com/mygroups?ishotfeed=1&leftnav=1&page_id=102803_ctg1_1760_-_ctg1_1760'
    ]  # 热门微博页

    cookies = None
    parse_depth = None

    global user_bit;
    user_bit = userBit()

    rules = (

    )

    hot_user = set()

    logger = get_weibo_log()

    def start_requests(self):
        for url_ in self.start_urls:
            if not self.cookies:
                self.cookies = get_login_cookie(url_)
                self.parse_depth = settings.PARSE_DEPTH
            yield Request(url_,
                          cookies=self.cookies,
                          callback=self.get_hot_user)

    # 爬取上热门微博的用户信息
    def get_hot_user(self, response):
        body_ = response.body.decode()
        p = re.compile("<a\s+.*?class\s*=\s*\"W_f14 W_fb S_txt1\".*?\s+href\s*=\s*\"(.*?)\"")
        urls = p.findall(body_.replace('\\\"', '\"'))
        for url_ in urls:
            url_ = url_.replace('\\', '')
            self.logger.info('hot: %s', url_)
            self.hot_user.add(url_)

        # 跟进热门链接
        for hot_url in self.hot_user:
            url_ = response.urljoin(hot_url)
            self.logger.info('follow: %s', url_)
            yield scrapy.Request(url_,
                                 # cookies=self.cookies,
                                 callback=self.parse_user_page,
                                 method='POST',
                                 meta={'depth': 0})

    # 进入用户界面处理用户信息
    def parse_user_page(self, response):
        try:
            body_ = response.body.decode()
        except Exception:
            body_ = response.body.decode('GBK')
        depth = response.meta['depth']
        # user_link_list = []

        user_id = int(get_userID_from_mainPage(body_))
        if not user_bit.is_user_exist(user_id):
            user_bit.insert_user(user_id)
            item, concern_link, fans_link = get_userItem(body_, user_bit)  # 获取用户信息 UserItem
            yield item

            if concern_link and item['concern_num'] > 0:
                concern_request_link = response.urljoin(concern_link)
                self.logger.info('concern link : %s', concern_request_link)
                yield Request(concern_request_link,
                              callback=self.parse_concern,
                              cookies=self.cookies,
                              meta={'user_id': item['id'],
                                    # 'link_list': user_link_list,
                                    'page': 1})

            if fans_link and item['fans_num'] > 0:
                fans_request_link = response.urljoin(fans_link)
                self.logger.info('concern link : %s', fans_request_link)
                yield Request(fans_request_link,
                              callback=self.parse_fans,
                              cookies=self.cookies,
                              meta={'user_id': item['id'],
                                    # 'link_list': user_link_list,
                                    'page': 1})

            # 请求用户主页的全部微博页
            user_request_link = response.urljoin('?profile_ftype=1&is_all=1#_0')
            self.logger.info('user main page : %s', user_request_link)
            yield Request(user_request_link,
                          # cookies=self.cookies,
                          callback=self.parse_blog,
                          meta={'user_id': item['id']}
                          # 'link_list': user_link_list}
                          )

            # if depth < self.parse_depth:
            #     for user_link in user_link_list:
            #         request_link = response.urljoin(user_link)
            #         self.logger.info('user main page link : %s', request_link)
            #         yield Request(request_link,
            #                       callback=self.parse_user_page,
            #                       method='POST',
            #                       cookies=self.cookies,
            #                       meta={'depth': depth + 1})

    # 处理用户页面博客
    def parse_blog(self, response):
        user_id = response.meta['user_id']
        # user_link_list = response.meta['link_list']
        body_ = response.body.decode()

        for blog_item, forward_user, forward_item in get_blogs(user_id, body_):
            yield blog_item  # 返回博客item

            # 获取每个博客的评论
            comment_url = get_comment_url(blog_item['m_id'], 1)  # 拼接Url

            # 请求博客所有评论页面
            self.logger.info('comment : %s', comment_url)
            yield Request(comment_url,
                          callback=self.parse_comment,
                          cookies=self.cookies,
                          meta={'blog_id': blog_item['id'],
                                'm_id': blog_item['m_id']
                                # 'link_list': user_link_list
                                })
            if forward_user:
                user_link = response.urljoin(forward_user)
                self.logger.info('forward user link : %s', user_link)
                request = Request(user_link,
                                  cookies=self.cookies,
                                  callback=self.parse_user_page
                                  )
                yield request

            if forward_item:
                yield forward_item

                forward_comment_url = get_comment_url(blog_item['m_id'], 1)  # 拼接Url
                # 请求博客所有评论页面
                self.logger.info('forward comment : %s', forward_comment_url)
                yield Request(forward_comment_url,
                              callback=self.parse_comment,
                              cookies=self.cookies,
                              meta={'blog_id': blog_item['id'],
                                    'm_id': blog_item['m_id']
                                    # 'link_list': user_link_list
                                    })

    # 仅获得userItem
    # def parse_user_item(self, response):
    #     """
    #     :param response:
    #     :return: userItem
    #     """
    #     body_ = response.body.decode()
    #
    #     user_id = int(get_userID_from_mainPage(body_))
    #     if not user_bit.is_user_exist(user_id):
    #         item, _, _ = get_userItem(body_, user_bit)  # 获取用户信息 UserItem
    #         user_bit.insert_user(user_id)
    #         yield item

    # 获取博客的评论信息
    def parse_comment(self, response):
        blog_id = response.meta['blog_id']
        m_id = response.meta['m_id']
        # user_link_list = response.meta['link_list']

        body_ = response.body.decode('GBK')

        data = json.loads(body_)
        if data.get('data') and data.get('data').get('count') \
                and data.get('data').get('count') > 0:
            comment_data = data.get('data')
            if comment_data:
                comment_body = comment_data.get('html')
                page = comment_data.get('page')
                # 获取评论当前页和总页数
                if page:
                    page_num = page.get('totalpage')
                    current_page = page.get('pagenum')
                else:
                    page_num = 1
                    current_page = 1
                comment_count = comment_data.get('count')
                if comment_count > 0:
                    for comment, user_link in get_comment(blog_id, comment_body):
                        yield comment  # 返回评论
                        # if not user_bit.is_user_exist(comment['user_id']): # 查看评论的用户是否已经爬取过
                        comment_request_link = response.urljoin(user_link)
                        self.logger.info('comment user link : %s', comment_request_link)
                        request = Request(comment_request_link,
                                          cookies=self.cookies,
                                          callback=self.parse_user_page
                                          )
                        yield request
                        # user_link_list.append(user_link)
                        # id_ = int(comment['user_id'])
                        # user_bit.insert_user(id_)

                    # 获取下一页的评论
                    if current_page < page_num:
                        comment_url = get_comment_url(m_id, page_num + 1)
                        self.logger.info('next page link : %s', comment_url)
                        yield Request(comment_url,
                                      callback=self.parse_comment,
                                      # cookies=self.cookies,
                                      meta={'blog_id': blog_id,
                                            'm_id': m_id
                                            # 'link_list': user_link_list
                                            })

    # 获取关注用户列表
    def parse_concern(self, response):
        body = response.body
        user_id = response.meta['user_id']
        # user_link_list = response.meta['link_list']
        page_num = response.meta['page']

        for user, id_ in get_concern_user_list(body):
            if user:
                # user_link_list.append(user)  # 将用户加入用户列表

                user_link = response.urljoin(user)
                self.logger.info('concern list user link : %s', user_link)
                yield Request(user_link,
                              cookies=self.cookies,
                              callback=self.parse_user_page
                              # meta={'link_list': user_link_list}
                              )

            if id_ and id_ != -1:
                fans_item = items.fansItem()
                fans_item['id'] = get_uuid()
                fans_item['fans'] = user_id
                fans_item['focuse'] = id_

                yield fans_item

        # 爬取下一页关注列表
        if page_num < 5:
            next_page_link = get_concern_url(page_num + 1)
            self.logger.info('concern next page link : %s', next_page_link)
            yield Request(response.urljoin(next_page_link),
                          callback=self.parse_concern,
                          cookies=self.cookies,
                          meta={'user_id': user_id,
                                # 'link_list': user_link_list,
                                'page': page_num + 1})

    # 获取粉丝用户列表
    def parse_fans(self, response):
        body = response.body
        user_id = response.meta['user_id']
        # user_link_list = response.meta['link_list']
        page_num = response.meta['page']

        for user, id_ in get_concern_user_list(body):
            if user:
                user_link = response.urljoin(user)
                # user_link_list.append(user)
                self.logger.info('fans user link : %s', user_link)
                yield Request(user_link,
                              cookies=self.cookies,
                              callback=self.parse_user_page)

            if id_ and id_ != -1:
                fans_item = items.fansItem()
                fans_item['id'] = get_uuid()
                fans_item['fans'] = id_
                fans_item['focuse'] = user_id

                yield fans_item

        # 爬取下一页粉丝列表列表
        if page_num < 5:
            next_page_link = get_fans_url(page_num + 1)
            self.logger.info('fans next page link : %s', next_page_link)
            yield Request(response.urljoin(next_page_link),
                          callback=self.parse_fans,
                          cookies=self.cookies,
                          meta={'user_id': user_id,
                                # 'link_list': user_link_list,
                                'page': page_num + 1})
