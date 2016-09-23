# from scrapy.selector import Selector
#
# a = '''
#     <div class="WB_detail">
#             <div class="WB_info">
#                 <a suda-uatrack="key=feed_headnick&amp;value=pubuser_nick:4021826785414290" target="_blank" class="W_f14 W_fb S_txt1" nick-name="DeKol" title="DeKol" href="/u/5980173226?refer_flag=0000015010_&amp;from=feed&amp;loc=nickname" usercard="id=5980173226&amp;refer_flag=0000015010_">DeKol</a>            </div>
#             <div class="WB_from S_txt2">
#                 <a target="_blank" href="/5980173226/E99OumIvg?ref=home&amp;rid=0_0_1_2815982929783515702" title="2016-09-20 16:54" date="1474361689000" class="S_txt2" node-type="feed_list_item_date" suda-data="key=tblog_home_new&amp;value=feed_time:4021826785414290">9月20日 16:54</a> 来自 <a class="S_txt2" suda-data="key=tblog_home_new&amp;value=feed_come_from" action-type="app_source" target="_blank" href="http://app.weibo.com/t/feed/6vtZb0" rel="nofollow">微博 weibo.com</a>            </div>
#                         <div class="WB_text W_f14" node-type="feed_list_content">
#                                     en 。。。。                            </div>
#                                                         <div class="WB_feed_expand">
#                     <div class="W_arrow_bor W_arrow_bor_t"><i class="S_bg1_br"></i></div>
#                     <div class="WB_expand S_bg1" node-type="feed_list_forwardContent">
#                                                                             <div class="WB_info">
#                                                                     <a target="_blank" suda-uatrack="key=feed_headnick&amp;value=transuser_nick:4021549306451085" class="W_fb S_txt1" node-type="feed_list_originNick" nick-name="Dm蜜桃" href="/u/2414098821?refer_flag=0000015010_&amp;from=feed&amp;loc=nickname" title="Dm蜜桃" usercard="id=2414098821&amp;refer_flag=0000015010_">
#                                     @Dm蜜桃</a><a action-type="ignore_list" suda-uatrack="key=home_vip&amp;value=home_feed_vip" title="微博会员" target="_blank" href="http://vip.weibo.com/personal?from=main"><em class="W_icon icon_member5"></em></a><a target="_blank" href="http://huodong.weibo.com/travel2016?ref=icon " title="带着微博去旅行"><i class="W_icon icon_airball"></i></a>                                                            </div>
#                                                         <div class="WB_text" node-type="feed_list_reason">
#                                                                     和郭小狗一起吃饭，她让我结账。我觉得特别不公平，这次凭什么是我请阿？上回吃的麻辣烫，上上次吃得烤串，上上上次吃的拉面等等，哪回不是她请的🙄                                                            </div>
#                                                                                                 <!-- 微博心情，独立于标准的ul节点 -->
#
# <div class="WB_media_wrap clearfix" node-type="feed_list_media_prev">
#     <div class="media_box">
#                                     <!--图片个数大于1，不渲染卡片-->
#                 <!--TODO 只显示图片-->
#
#     <!--picture_count == 9-->
#     <ul class="WB_media_a WB_media_a_mn WB_media_a_m9 clearfix" node-type="fl_pic_list" action-data="uid=2414098821&amp;pic_ids=8fe43985jw1f7z9n3b5kbj223u35s7wh,8fe43985jw1f7z9n5luphj223u35stqs,8fe43985jw1f7z9nbnlzcj235s23u1kx,8fe43985jw1f7z9nggax9j235s23u7wh,8fe43985jw1f7z9njqo3vj235s23u4qp,8fe43985jw1f7z9nmmt5kj235s23u1kx,8fe43985jw1f7z9mzfq8rj22o51s3e81,8fe43985jw1f7z9nz1ybuj21s32o5kjl,8fe43985jw1f7z9o48rssj22o51s3neo&amp;mid=4021549306451085&amp;pic_objects=&amp;object_ids=1042018%3A06425eaa1029fd21a280894d6581b020%2C1042018%3A23c87c92765c5756c150153ce55cb6f7%2C1042018%3Abc1e851908e3173133de9ab083c882b3%2C1042018%3Ae01c75214eb6dbff1233f6f38f80c0b1%2C1042018%3A3d7a2bec0efcf4c7a3c837a98442e2b3%2C1042018%3A34cece19fe632d5b8c68bb8f44d2727d%2C1042018%3Ad1f43c5997055162dd3bb5ac3f47bccc%2C1042018%3A85c0a8e71e1e5ccfe14d749070fc655a%2C1042018%3Afc6ac034d6928971a018605b0fbace79&amp;photo_tag_pids=">
#                                 <li class="WB_pic li_1 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9n3b5kbj223u35s7wh" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9n3b5kbj223u35s7wh">
#                 <img src="http://ww2.sinaimg.cn/thumb180/8fe43985jw1f7z9n3b5kbj223u35s7wh.jpg">
#                             </li>
#                                 <li class="WB_pic li_2 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9n5luphj223u35stqs" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9n5luphj223u35stqs">
#                 <img src="http://ww3.sinaimg.cn/thumb180/8fe43985jw1f7z9n5luphj223u35stqs.jpg">
#                             </li>
#                                 <li class="WB_pic li_3 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9nbnlzcj235s23u1kx" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9nbnlzcj235s23u1kx">
#                 <img src="http://ww2.sinaimg.cn/thumb180/8fe43985jw1f7z9nbnlzcj235s23u1kx.jpg">
#                             </li>
#                                 <li class="WB_pic li_4 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9nggax9j235s23u7wh" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9nggax9j235s23u7wh">
#                 <img src="http://ww3.sinaimg.cn/thumb180/8fe43985jw1f7z9nggax9j235s23u7wh.jpg">
#                             </li>
#                                 <li class="WB_pic li_5 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9njqo3vj235s23u4qp" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9njqo3vj235s23u4qp">
#                 <img src="http://ww3.sinaimg.cn/thumb180/8fe43985jw1f7z9njqo3vj235s23u4qp.jpg">
#                             </li>
#                                 <li class="WB_pic li_6 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9nmmt5kj235s23u1kx" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9nmmt5kj235s23u1kx">
#                 <img src="http://ww1.sinaimg.cn/thumb180/8fe43985jw1f7z9nmmt5kj235s23u1kx.jpg">
#                             </li>
#                                 <li class="WB_pic li_7 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9mzfq8rj22o51s3e81" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9mzfq8rj22o51s3e81">
#                 <img src="http://ww1.sinaimg.cn/thumb180/8fe43985jw1f7z9mzfq8rj22o51s3e81.jpg">
#                             </li>
#                                 <li class="WB_pic li_8 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9nz1ybuj21s32o5kjl" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9nz1ybuj21s32o5kjl">
#                 <img src="http://ww2.sinaimg.cn/thumb180/8fe43985jw1f7z9nz1ybuj21s32o5kjl.jpg">
#                             </li>
#                                 <li class="WB_pic li_9 S_bg1 S_line2 bigcursor" action-data="pic_id=8fe43985jw1f7z9o48rssj22o51s3neo" action-type="fl_pics" suda-uatrack="key=tblog_newimage_feed&amp;value=image_feed_unfold:4021549306451085:8fe43985jw1f7z9o48rssj22o51s3neo">
#                 <img src="http://ww3.sinaimg.cn/thumb180/8fe43985jw1f7z9o48rssj22o51s3neo.jpg">
#                             </li>
#             </ul>
#                         </div>
# </div>                                                                <div class="WB_expand_media_box" style="display: none;" node-type="feed_list_media_disp"></div>
#                                                         <div class="WB_func clearfix">
#                                 <div class="WB_handle W_fr" mid="4021549306451085">
#                                     <ul class="clearfix">
#                                         <li><span class="line S_line1">
#                                             <a class="S_txt2" target="_blank" href="/2414098821/E92AWr4dL?type=repost" suda-uatrack="key=feed_trans_weibo&amp;value=transfer:4021549306451085"><span><em class="W_ficon ficon_forward S_ficon"></em><em>180</em></span></a></span></li>
#                                         <li><span class="line S_line1">
#                                             <a class="S_txt2" target="_blank" href="/2414098821/E92AWr4dL" suda-uatrack="key=feed_trans_weibo&amp;value=comment:4021549306451085"><span><em class="W_ficon ficon_repeat S_ficon"></em><em>352</em></span></a>
#                                         </span></li>
#                                         <li><span class="line S_line1">
#                                         <a class="S_txt2" href="javascript:void(0);" action-type="fl_like" action-data="version=mini&amp;qid=heart&amp;mid=4021549306451085&amp;like_src=1" title="赞">
#                                                                                                                                                                                                                                                                                                                                                                                                                     <span node-type="like_status" class=""><em class="W_ficon ficon_praised S_txt2">ñ</em><em>4610</em></span>                                         </a></span></li>
#                                     </ul>
#                                 </div>
#                                 <div class="WB_from S_txt2">
#                                     <a class="S_txt2" target="_blank" href="/2414098821/E92AWr4dL" title="2016-09-19 22:32" date="1474295534000" node-type="feed_list_item_date" suda-uatrack="key=feed_trans_weibo&amp;value=time:4021549306451085">9月19日 22:32</a> 来自 <a class="S_txt2" action-type="app_source" target="_blank" href="http://app.weibo.com/t/feed/5yiHuw" rel="nofollow">iPhone 6 Plus</a>                                </div>
#                             </div>
#                                             </div>
#                 </div>
#                                         	                    <!-- feed区 大数据tag -->
# <!-- /feed区 大数据tag -->                    </div>
# '''
# a = Selector(text=a).xpath("./div[@class='WB_feed_expand']/div/div[contains(@class, 'WB_expand S_bg')]")
# if a:
#     user_info = a.xpath("./div[@class='WB_info']/a/@href").extract()
#
# print(a)
#
from scrapy.selector import Selector
body = '<html><body><span>good</span></body></html>'
a = Selector(text=body, type='html').xpath('//span/text()').extract()
print(a)

# a = 'id=2414098821&refer_flag=0000015010_'
# ids = a.split('&')
# for id in ids:
#     id = id.strip()
#     if id.startswith('id='):
#         print(id.split('=')[1])
#         break;
#
# a = '\u3010310\u4e07\u5f20\u201c\u957f\u5b89\u901a\u201d\u5361\u53bb\u5411\u6210\u8c1c\u3011\u6c47\u62a5\u6750\u6599\u4e2d\u957f\u5b89\u901a\u5361\u5df2\u8fc7\u5343\u4e07\u5f20\uff0c\u4e3a\u4f55\u5bf9\u5916\u79f0690\u4e07\u5f20?\u6240\u5dee\u7684310\u4e07\u5f20\uff0c\u6309\u6bcf\u5f20\u536118\u5143\u7684\u5de5\u672c\u8d39\u8ba1\u7b97\uff0c\u81f3\u5c11\u6d89\u53ca5580\u4e07\u5143\u30029\u670819\u65e5\u4e0b\u5348\uff0c\u897f\u5b89\u57ce\u5e02\u4e00\u5361\u901a\u6709\u9650\u516c\u53f8\u526f\u603b\u7ecf\u7406\u90b9\u950b\u79f0\uff0c\u81ea\u5df1\u624d\u8c03\u5230\u8be5\u516c\u53f8\u51e0\u4e2a\u6708\uff0c\u5177\u4f53\u539f\u56e0\u4e0d\u6e05\u695a\u3002\u6b64\u524d\u5bf9\u8bb0\u8005\u79f0\u53d1\u884c\u4e86690\u4e07\u5f20\u957f\u5b89\u901a\u5361\u7684\u8be5\u516c\u53f8\u8fd0\u8425\u90e8\u8d1f\u8d23\u4eba\u4e5f\u6ca1\u6709\u7ed9\u51fa\u89e3\u91ca\u3002<a  suda-uatrack=\"key=tblog_card&value=click_title:4022082021149519:1022-article:1022%3A2309351001684022039810832253:weibodetail:1644855075:4022082021149519:1644855075\" title=\"310\u4e07\u5f20\u201c\u957f\u5b89\u901a\u201d\u5361\u53bb\u5411\u6210\u8c1c \u81f3\u5c11\u6d89\u53ca5580\u4e07\u5143\" href=\"http:\/\/weibo.com\/ttarticle\/p\/show?id=2309351001684022039810832253\" action-type=\"feed_list_url\" target=\"_blank\" ><i class=\"W_ficon ficon_cd_longwb\">&#xb0;<\/i>310\u4e07\u5f20\u201c\u957f\u5b89\u901a\u201d\u5361\u53bb\u5411\u6210\u8c1c \u81f3\u5c11\u6d89\u53ca5580\u4e07\u5143<\/a>'
#
# print(a)