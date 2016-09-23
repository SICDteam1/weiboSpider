# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# 定义数据库中的表
# 用户表
class userItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    is_v = scrapy.Field()  # 是否是加V用户
    address = scrapy.Field()
    sex = scrapy.Field()
    birthday = scrapy.Field()
    v_des = scrapy.Field()  # 加V描述
    concern_num = scrapy.Field()  # 关注数量
    fans_num = scrapy.Field()  # 粉丝的数量
    blog_num = scrapy.Field()  # 博客的数量
    level = scrapy.Field()  # 等级
    exp_value = scrapy.Field()  # 经验值


# 博客表
class blogItem(scrapy.Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    m_id = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    topics = scrapy.Field()
    at = scrapy.Field()
    praise_num = scrapy.Field()
    comment_num = scrapy.Field()
    forward_num = scrapy.Field()  # 转发的数量
    forward_id = scrapy.Field()  # 转发微博的ID
    date = scrapy.Field()  # 时间的数字表示


#转发博客表
class forwardBlogItem(scrapy.Item):
    id = scrapy.Field()
    user_id = scrapy.Field()
    m_id = scrapy.Field()
    content = scrapy.Field()
    time = scrapy.Field()
    topics = scrapy.Field()
    at = scrapy.Field()
    praise_num = scrapy.Field()
    comment_num = scrapy.Field()
    forward_num = scrapy.Field()  # 转发的数量
    date = scrapy.Field()  # 时间的数字表示


# 评论表
class commentItem(scrapy.Item):
    id = scrapy.Field()
    blog_id = scrapy.Field()
    user_id = scrapy.Field()
    time = scrapy.Field()
    praise_num = scrapy.Field()
    content = scrapy.Field()


# 粉丝关注表
class fansItem(scrapy.Item):
    id = scrapy.Field()
    focuse = scrapy.Field()
    fans = scrapy.Field()


# 话题表
class topicItem(scrapy.Item):
    id = scrapy.Field()
    blog_id = scrapy.Field()
    user = scrapy.Field()
    name = scrapy.Field()
    read_num = scrapy.Field()
    discuss_num = scrapy.Field()
    fans_num = scrapy.Field()