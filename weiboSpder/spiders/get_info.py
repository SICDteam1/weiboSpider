#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import re

from scrapy import Selector

from weiboSpder import items

__author__ = 'Yh'


# 从用户主界面获取用户ID
def get_userID_from_mainPage(body):
    p_id = re.compile(r'\$CONFIG\[\'oid\'\]=\'(.*)\'')
    try:
        id = p_id.search(body).group(1)
    except:
        raise Exception('id不存在')

    return id


# 获取用户信息
def get_userItem(body, user_bit):
    """
    :type body: str
    :param body: 用户主页网页
    :return:item: 用户信息item
            concern_link: 所关注用户的链接
            fans_link: 粉丝的链接
    """
    item = items.userItem()

    # 获取ID
    user_id = int(get_userID_from_mainPage(body))
    item['id'] = user_id

    # 获取用户名
    p_name = re.compile(r'\$CONFIG\[\'onick\'\]=\'(.*)\'')
    try:
        name_ = p_name.search(body).group(1)
        item['name'] = name_
    except:
        item['name'] = ''

    # 是否是加V用户
    script_heads = Selector(text=body).xpath('//script/text()').extract()
    head_body = ''
    content_body = ''
    num_body = ''
    relation_body = ''

    for script_head in script_heads:
        p_head = re.compile(r'^\s*FM\.view\(\{(.*)\}\)', re.M)
        p_head_s = p_head.search(script_head.replace('\n', '').replace('\t', ''))

        if p_head_s:
            json_head = '{' + p_head_s.group(1) + '}'
            data = json.loads(json_head)
            if data.get('domid'):
                if 'Pl_Official_Headerv6' in data.get('domid'):  # 从该段中获取是否加V和性别信息
                    head_body = data.get('html')
                elif 'Pl_Core_UserInfo' in data.get('domid'):  # 从该段中获取加V描述，地址，生日
                    content_body = data.get('html')
                elif 'Pl_Core_T8CustomTriColumn' in data.get('domid'):
                    num_body = data.get('html')
                elif 'Pl_Core_UserGrid' in data.get('domid'):
                    relation_body = data.get('html')
    if head_body:
        v = Selector(text=head_body).xpath("//em[@class='W_icon icon_pf_approve']").extract_first()
        v_co = Selector(text=head_body).xpath("//em[contains(@class, 'icon_pf_approve_co')]").extract_first()
        if v:
            item['is_v'] = 1  # 个人
        elif v_co:
            item['is_v'] = 2  # 机构
        else:
            item['is_v'] = 0

        # 获取性别
        female = Selector(text=head_body).xpath("//i[@class='W_icon icon_pf_female']").extract_first()
        male = Selector(text=head_body).xpath("//i[@class='W_icon icon_pf_male']").extract_first()
        if female:
            item['sex'] = 1  # 女
        elif male:
            item['sex'] = 2  # 男
        else:
            item['sex'] = 0  # 出错或未知

        # 获取加V描述
        v_des = Selector(text=head_body).xpath("//div[@class='pf_intro']/text()")
        if v_des:
            item['v_des'] = v_des.extract_first().strip()
        else:
            item['v_des'] = ''
    else:
        item['is_v'] = -1  # 出错
        item['sex'] = 0
        item['v_des'] = ''

    # 获得微博等级
    if content_body:
        level_ = Selector(text=content_body).xpath("//a[contains(@class,'W_icon_level')]/span/text()").extract_first()
        if level_:
            item['level'] = int(level_.strip('Lv. '))
        else:
            item['level'] = -1

        # 获取地址和生日
        item['address'] = ''
        item['birthday'] = ''
        contents = Selector(text=content_body) \
            .xpath("//div[@class='detail']/ul[@class='ul_detail']/li[@class='item S_line2 clearfix']")
        for content in contents:
            icon = content.xpath("./span[contains(@class, 'item_ico W_f')]/em/@class").extract_first()
            if icon == 'W_ficon ficon_cd_place S_ficon':
                addr = content.xpath("./span[contains(@class, 'item_text W_f')]/text()").extract_first().strip()
                item['address'] = addr
            elif icon == 'W_ficon ficon_constellation S_ficon':
                birthday = content.xpath("./span[contains(@class, 'item_text W_f')]/text()").extract_first().strip()
                item['birthday'] = birthday
    else:
        item['level'] = -1
        item['address'] = ''
        item['birthday'] = ''

    # 获取关注、粉丝、微博的数量
    concern_link = ''
    fans_link = ''

    if num_body:
        num_infos = Selector(text=num_body).xpath("//a[@class='t_link S_txt1']")
        has_link = False
        if num_infos:
            text_xpath = "./span[@class='S_txt2']/text()"
            num_xpath = "./strong[contains(@class, 'W_f')]/text()"
            has_link = True
        else:
            num_infos = Selector(text=num_body).xpath("//td[@class='S_line1']")
            text_xpath = "./span[@class='S_txt2']/text()"
            num_xpath = "./strong[contains(@class,'W_f')]/text()"

        for num_info in num_infos:
            info = num_info.xpath(text_xpath).extract_first()
            num = num_info.xpath(num_xpath).extract_first()
            if num:
                num = int(num.strip())
            else:
                num = -1

            if info == '关注':
                item['concern_num'] = num
                if has_link:
                    concern_link = num_info.xpath("./@href").extract_first()
            elif info == '粉丝':
                item['fans_num'] = num
                if has_link:
                    fans_link = num_info.xpath("./@href").extract_first()
            elif info == '微博':
                item['blog_num'] = num

        # 从微关系块获得关注、粉丝的链接信息
        if not has_link:
            relation_infos = Selector(text=relation_body) \
                .xpath(
                "//div[@class='obj_name']/h2[contains(@class, 'main_title W_fb W_f')]/a[contains(@class, 'S_txt')]")
            for relation in relation_infos:
                link = relation.xpath("./@href").extract_first()
                text = relation.xpath('./text()').extract_first()
                if '关注' in text:
                    concern_link = link
                elif '粉丝' in text:
                    fans_link = link
    else:
        item['concern_num'] = -1  # 未知或出错
        item['fans_num'] = -1
        item['blog_num'] = -1

    return item, concern_link, fans_link


# 获取博客的信息
def get_blogs(user_id, body):
    # 获取有微博的块
    blog_body = ''
    script_heads = Selector(text=body).xpath('//script/text()').extract()

    for script_head in script_heads:
        p_head = re.compile(r'^\s*FM\.view\(\{(.*)\}\)', re.M)
        p_head_s = p_head.search(script_head.replace('\n', '').replace('\t', ''))

        if p_head_s:
            json_head = '{' + p_head_s.group(1) + '}'
            data = json.loads(json_head)
            if data.get('domid'):
                if 'Pl_Official_MyProfileFeed' in data.get('domid'):
                    blog_body = data.get('html')

    blogs = Selector(text=blog_body).xpath("//div[contains(@class, 'WB_cardwrap WB_feed_type')]")
    for blog in blogs:
        item = items.blogItem()
        item['user_id'] = user_id
        from weiboSpder.utils.uuid import get_uuid
        item['id'] = get_uuid()

        # 获取mid
        mid = blog.xpath("./@mid").extract_first()
        item['m_id'] = mid

        blog_detail = blog.xpath("./div[@class='WB_feed_detail clearfix']/div[@class='WB_detail']")
        # 获取博客时间
        blog_time = blog_detail.xpath("./div[contains(@class, 'WB_from S_txt')]/a/@title").extract_first()
        # if '今天' in blog_time:
        #     import datetime
        #     blog_time.replace('今天', datetime.date.today())
        # elif '昨天' in blog_time:
        #     import  datetime
        #     blog_time.replace('昨天', datetime.date.today() - datetime.timedelta(days=1))
        item['time'] = blog_time

        blog_date = blog_detail.xpath("./div[contains(@class, 'WB_from S_txt')]/a/@date").extract_first()
        item['date'] = blog_date

        # 获取博客内容
        blog_text = blog_detail.xpath("./div[contains(@class, 'WB_text W_f')]").extract_first()  # 包含博客中的标签，暂时不做数据清洗
        # if Selector(text=blog_text).xpath("//a[@class='WB_text_opt']/text()").extract_first() == '展开全文': # 用获得的json数据代替blogtext做处理。暂不做处理
        item['content'] = blog_text

        # @信息
        blog_at = blog_detail \
            .xpath("./div[contains(@class, 'WB_text W_f')]/a[@extra-data='type=atname']/text()").extract()
        item['at'] = [x[1:] for x in blog_at]

        # # #话题信息
        blog_topic = blog_detail \
            .xpath("./div[contains(@class, 'WB_text W_f')]/a[@extra-data='type=topic']/text()").extract()
        item['topics'] = [x[1:-1] for x in blog_topic]

        # 转发了微博时，获取转发信息
        # 获取转发微博的块
        forward_area = blog_detail \
            .xpath("./div[@class='WB_feed_expand']/div/div[contains(@class, 'WB_expand S_bg')]")
        forward_link = None
        forward_item = None
        item['forward_id'] = ''
        if forward_area:
            forward_link, forward_item = get_forward_info(forward_area)
            item['forward_id'] = forward_item['id']

        # 获取微博下方转发、评论和赞的数量
        blog_bottom_list = blog.xpath(
            "./div[@class='WB_feed_handle']/div[@class='WB_handle']/ul/li/a[contains(@class, S_txt)]/span/span")
        if not blog_bottom_list:
            return None

        for blog_bottom in blog_bottom_list:
            bottom_type = blog_bottom.xpath("./@node-type").extract_first()
            node_num = blog_bottom.xpath("./span/em/text()")[-1].extract()
            if bottom_type == 'forward_btn_text':  # 转发的数量
                if node_num.isdigit():
                    item['forward_num'] = int(node_num)
                elif node_num == '转发':
                    item['forward_num'] = 0
                else:
                    item['forward_num'] = -1
            elif bottom_type == 'comment_btn_text':  # 评论的数量
                if node_num.isdigit():
                    item['comment_num'] = int(node_num)
                elif node_num == '评论':
                    item['comment_num'] = 0
                else:
                    item['comment_num'] = -1

            # 赞的数量
            praise_num = blog_bottom.xpath("./span[@node-type='like_status']/em/text()").extract()
            if praise_num:
                praise_num = praise_num[-1]
                if praise_num.isdigit():
                    item['praise_num'] = int(praise_num)
                elif praise_num == '赞':
                    item['praise_num'] = 0
                else:
                    item['praise_num'] = -1

        yield item, forward_link, forward_item


# 获取转发消息
def get_forward_info(forward_info):
    user_link = forward_info.xpath("./div[@class='WB_info']/a/@href").extract_first()

    forwardItem = items.forwardBlogItem()
    from weiboSpder.utils.uuid import get_uuid
    forwardItem['id'] = get_uuid()

    user_card = forward_info.xpath("./div[@class='WB_info']/a/@usercard").extract_first()
    if user_card:
        ids = user_card.split('&')
        for user_id in ids:
            user_id = user_id.strip()
            if user_id.startswith('id='):
                forwardItem['user_id'] = user_id
                break

    blog = forward_info.xpath("./div[@class='WB_text']").extract_first()
    forwardItem['content'] = blog
    wb_func = forward_info.xpath("./div[@class='WB_func clearfix']")
    m_id = wb_func.xpath("./div[@class='WB_handle W_fr']/@mid").extract_first()
    forwardItem['m_id'] = m_id

    date = wb_func.xpath("./div[contains(@class, 'WB_from S_txt')]/a/@date").extract_first()
    forwardItem['date'] = date

    blog_time = wb_func.xpath("./div[contains(@class, 'WB_from S_txt')]/a/@title").extract_first()
    forwardItem['time'] = blog_time

    # @信息
    blog_at = forward_info.xpath("./div[@class='WB_text']/a[@extra-data='type=atname']/text()").extract()
    forwardItem['at'] = [x[1:] for x in blog_at]

    # # #话题信息
    blog_topic = forward_info.xpath("./div[@class='WB_text']/a[@extra-data='type=topic']/text()").extract()
    forwardItem['topics'] = [x[1:-1] for x in blog_topic]

    # 初始化
    forwardItem['forward_num'] = 0
    forwardItem['comment_num'] = 0
    forwardItem['praise_num'] = 0

    bottomList = wb_func.xpath("./div[@class='WB_handle W_fr']/ul[@class='clearfix']/li")
    for bottom in bottomList:
        ems = bottom.xpath("./span[contains(@class, line S_line)]/a/span/em")
        em_icon = ems[0].xpath("./@class").extract_first()
        em_num = ems[1].xpath("./@class").extract_first()
        if 'ficon_forward' in em_icon:
            if em_num.isdigit():
                forwardItem['forward_num'] = int(em_num)
        elif 'ficon_repeat' in em_icon:
            if em_num.isdigit():
                forwardItem['comment_num'] = int(em_num)
        elif 'ficon_praised' in em_icon:
            if em_num.isdigit():
                forwardItem['praise_num'] = int(em_num)

    return user_link, forwardItem


# 获取评论的信息
def get_comment(blog_id, body):
    """
    :param blog_id:
    :param body:
    :return: comment:评论
             user_link:评论的用户链接
    """
    comment_body_list = Selector(text=body) \
        .xpath("//div[@class='list_box']/div[@class='list_ul']/div[@class='list_li S_line1 clearfix']")
    for comment_body in comment_body_list:
        comment = items.commentItem()
        from weiboSpder.utils.uuid import get_uuid
        comment['id'] = get_uuid()

        comment['blog_id'] = blog_id

        user = comment_body.xpath("./div[contains(@class,'WB_face W_f')]/a")
        user_id = user.xpath("./img/@usercard").extract_first()[3:]
        if user_id:
            comment['user_id'] = int(user_id)
        else:
            continue

        user_link = user.xpath("./@href").extract_first()
        comment_content = comment_body.xpath("./div[@class='list_con']/div[@class='WB_text']").extract_first()
        comment['content'] = comment_content

        s = Selector(text=comment_content).xpath("//child::node()/text()").extract()
        result = ''.join(s).strip('\n\t ')

        time = comment_body \
            .xpath("./div[@class='list_con']/div[@class='WB_func clearfix']"
                   "/div[contains(@class, 'WB_from S_txt')]/text()").extract_first()
        comment['time'] = time

        praise = comment_body.xpath("./span[@node-type='like_status']/em").extract_first()
        if praise:
            praise_num = int(praise.strip())
            comment['praise_num'] = praise_num
        else:
            comment['praise_num'] = 0

        yield comment, user_link


# 获取关注的用户列表
def get_concern_user_list(body):
    user_list = ''
    script_heads = Selector(text=body).xpath('//script/text()').extract()
    for script_head in script_heads:
        p_head = re.compile(r'^\s*FM\.view\(\{(.*)\}\)', re.M)
        p_head_s = p_head.search(script_head.replace('\n', '').replace('\t', ''))

        if p_head_s:
            json_head = '{' + p_head_s.group(1) + '}'
            data = json.loads(json_head)
            if data.get('domid'):
                if 'Pl_Official_HisRelation_' in data.get('domid'):
                    user_list = data.get('html')

    if not user_list:
        yield None, None
    else:
        user_body_list = Selector(text=user_list).xpath("//div[@class='follow_inner']/ul[@class='follow_list']/li")
        if not user_body_list:
            yield None, None
        else:
            for user_body in user_body_list:
                # 根据关注的是否有性别标志来判断关注的是不是人
                male = user_body.xpath("./dl/dd/div/a/i[@class='W_icon icon_male']")
                female = user_body.xpath(
                    "./dl/dd/div/a/i[@class='W_icon icon_female']")
                if male or female:
                    user_link = user_body.xpath("./dl/dd/div[contains(@class, 'info_name W_fb W_f')]"
                                                "/a[contains(@class, 'S_txt')]/@href").extract_first()
                    user_id_text = user_body.xpath("./dl/dd/div[contains(@class, 'info_name W_fb W_f')]"
                                                   "/a[contains(@class, 'S_txt')]/@usercard").extract_first()

                    user_id = user_id_text.split('&')
                    id = -1
                    for x in user_id:
                        if 'id=' in x:
                            id = int(x.split('=')[-1])
                            break

                    yield user_link, id


# 获取用户的粉丝列表
def get_fans_user_list(body):
    user_list = ''
    script_heads = Selector(text=body).xpath('//script/text()').extract()
    for script_head in script_heads:
        p_head = re.compile(r'^\s*FM\.view\(\{(.*)\}\)', re.M)
        p_head_s = p_head.search(script_head.replace('\n', '').replace('\t', ''))

        if p_head_s:
            json_head = '{' + p_head_s.group(1) + '}'
            data = json.loads(json_head)
            if data.get('domid'):
                if 'Pl_Official_HisRelation_' in data.get('domid'):
                    user_list = data.get('html')
    user_body_list = Selector(text=user_list).xpath("//div[@class='follow_inner']/ul[@class='follow_list']/li")
    for user_body in user_body_list:
        user_link = user_body.xpath("./div[contains(@class, 'info_name W_fb W_f')]"
                                    "/a[contains(@class, 'S_txt')]/@href").extract_first()
        yield user_link
