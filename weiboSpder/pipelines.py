# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from scrapy import Selector

from weiboSpder.items import userItem, blogItem, commentItem, fansItem, forwardBlogItem


# 博客信息清理
def clean_content(content):
    content = Selector(text=content).xpath("//child::node()/text()").extract()
    result = ''.join(content).strip('\n\t ')

    return result


# 评论信息数据清理
def clean_comment(comment):
    pass


class SavePipeline(object):
    def __init__(self, mysql_user_name, mysql_password, mysql_db):
        self.mysql_user_name = mysql_user_name
        self.mysql_password = mysql_password
        self.mysql_db = mysql_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mysql_user_name=crawler.settings.get('MYSQL_USER_NAME'),
            mysql_password=crawler.settings.get('MYSQL_PASSWORD'),
            mysql_db=crawler.settings.get('MYSQL_DB')
        )

    def open_spider(self, spider):
        self.connect = mysql.connector.connect(
            user=self.mysql_user_name,
            password=self.mysql_password,
            database=self.mysql_db
        )

    def close_spider(self, spider):
        self.connect.close()

    def process_item(self, item, spider):
        cursor = self.connect.cursor()

        sql = self.generate_insert_sql(item)
        if sql:
            cursor.execute(sql)
            self.connect.commit()

        cursor.close()
        return item

    @staticmethod
    def generate_insert_sql(item):
        if isinstance(item, userItem):
            print(item['address'])
            sql = '''
                INSERT INTO wb_user (USER_ID,
                                     USER_NAME,
                                     USER_IS_V,
                                     USER_ADDR,
                                     USER_SEX,
                                     USER_V_DES,
                                     USER_CONCERN_NUM,
                                     USER_FANS_NUM,
                                     USER_BLOG_NUM,
                                     USER_LEVEL
                                     )
                  VALUES ("%d", "%s", "%d", "%s", "%d", "%s", "%d", "%d", "%d", "%d")
            ''' % (item['id'],
                   item['name'],
                   item['is_v'],
                   item['address'],
                   item['sex'],
                   item['v_des'],
                   item['concern_num'],
                   item['fans_num'],
                   item['blog_num'],
                   item['level']
                   )
            return sql

        elif isinstance(item, blogItem):
            blog = clean_content(item['content'])
            sql = '''
                INSERT INTO wb_blog (BLOG_ID,
                                     USER_ID,
                                     BLOG_CONTENT,
                                     BLOG_TIME,
                                     BLOG_TOPICS,
                                     BLOG_AT,
                                     BOLG_PRAISE_NUM,
                                     BLOG_M_ID,
                                     BLOG_COMMENT_NUM,
                                     BLOG_FORWARD_NUM,
                                     BLOG_FORWARD_ID,
                                     BLOG_DATE
                                     )
                  VALUES ("%s", "%d", "%s", "%s", "%s", "%s", "%d", "%s", "%d", "%d", "%s", "%s")
            ''' % (item['id'],
                   item['user_id'],
                   blog,
                   item['time'],
                   item['topics'],
                   item['at'],
                   item['praise_num'],
                   item['m_id'],
                   item['comment_num'],
                   item['forward_num'],
                   item['forward_id'],
                   item['date']
                   )
            return sql
        elif isinstance(item, forwardBlogItem):
            blog = clean_content(item['content'])
            sql = '''
                INSERT INTO wb_forward_blog (BLOG_ID,
                                     USER_ID,
                                     BLOG_CONTENT,
                                     BLOG_TIME,
                                     BLOG_TOPICS,
                                     BLOG_AT,
                                     BOLG_PRAISE_NUM,
                                     BLOG_M_ID,
                                     BLOG_COMMENT_NUM,
                                     BLOG_FORWARD_NUM,
                                     BLOG_DATE
                                     )
                  VALUES ("%s", "%d", "%s", "%s", "%s", "%s", "%d", "%s", "%d", "%d", "%s")
            ''' % (item['id'],
                   item['user_id'],
                   blog,
                   item['time'],
                   item['topics'],
                   item['at'],
                   item['praise_num'],
                   item['m_id'],
                   item['comment_num'],
                   item['forward_num'],
                   item['date']
                   )
            return sql

        elif isinstance(item, commentItem):
            comment = clean_content(item['content'])
            sql = '''
                INSERT INTO wb_comment (COMMENT_ID,
                                        COMMENT_USER_ID,
                                        COMMENT_BLOG_ID,
                                        COMMENT_TIME,
                                        COMMENT_PRAISE_NUM,
                                        COMMENT_CONTENT
                                        )
                  VALUES ("%s", "%d", "%s", "%s", "%d", "%s")
            ''' % (item['id'],
                   item['user_id'],
                   item['blog_id'],
                   item['time'],
                   item['praise_num'],
                   comment
                   )
            return sql

        elif isinstance(item, fansItem):
            sql = '''
                INSERT INTO wb_fans (FANS_ID,
                                     FANS_FOCUSE,
                                     FANS_FANS
                                     )
                  VALUES ("%s", "%d", "%d")
            ''' % (item['id'],
                   item['focuse'],
                   item['fans']
                   )
            return sql

        else:
            return None

