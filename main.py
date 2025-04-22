# import traceback

from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import asyncio
import re
from plugins.MessageForwarding.utils.inquire import BotInquire
from plugins.MessageForwarding.utils.bot_commands import handler as util_handler
# import pkg.platform.types as platform_types
from pkg.platform.types import *
import json
import os
import importlib

from pkg.provider import entities as llm_entities
from pkg.core import app


from plugins.MessageForwarding.utils.mode_classical import WillingManager
from random import random


from plugins.MessageForwarding.utils.asyautotask import AsyAutoTask
from datetime import datetime


# 注册插件
@register(name="MessageForwarding", description="Message forwarding", version="0.1", author="阿东不懂事")
class MessageForwarding(BasePlugin):
    ap: app.Application

    # bot_inq = BotInquire()

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.ap = app.Application()
        self.bot_inq = BotInquire()
        self.asyautotask = AsyAutoTask(host)
        self.tasks = []
        self.willing_msg = WillingManager()
        self.fixed_forwarder = ['wxid_xd12odto989122']
        self.fixed_forwarding_group = ['48371594138@chatroom']

        # self.task_file = os.path.join(os.path.dirname(__file__), 'tasks.json')  # 统一文件名
        # self.check_timer_task = asyncio.create_task(self.asyautotask.load_tasks())
        # self.asyautotask_start = await self.asyautotask.start()


        # pass

    # 异步初始化
    async def initialize(self):

        await self.asyautotask.start()

        await self.willing_msg.ensure_started()

        # print(self.host.get_platform_adapters())

        # async def send_message():
        #     print("send message start waiting")
        #     await asyncio.sleep(90)
        #
        #     try:
        #         await self.host.send_active_message(
        #             adapter=self.host.get_platform_adapters()[0],
        #             target_type="group",
        #             target_id="48371594138@chatroom",
        #             message=platform_message.MessageChain([
        #                 platform_message.At(target='wxid_xd12odto989122'),
        #                 platform_message.Plain(text='haha')
        #                 # platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')
        #
        #             ])
        #         )
        #     except Exception as e:
        #         return e
        #     print("send message end")
        #
        # asyncio.get_running_loop().create_task(send_message())

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        await self.message_evnt(ctx)
        ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        await self.message_evnt(ctx)

            # 阻止该事件默认行为（向接口获取回复）
        ctx.prevent_default()

    def is_mentioned_bot_in_message(self, ctx: EventContext) -> bool:

        if "小白" in [i for i in ctx.event.query.message_chain if not isinstance(i, platform_message.At)][0].text:
            return True
        elif isinstance(ctx.event.query.message_chain, At):
            return True
        return False


    async def message_evnt(self,ctx: EventContext):
        message_chains = ctx.event.query.message_chain
        user_msg = None
        target_type = ctx.event.launcher_type
        target_id = ctx.event.launcher_id
        # user_msg_list = []
        for msg_chain in message_chains:
            if isinstance(msg_chain, At):
                pass
            elif isinstance(msg_chain, Image):
                pass
            elif isinstance(msg_chain, Quote):
                qu_msg = msg_chain.origin
                print(qu_msg)
            elif isinstance(msg_chain, Plain):
                user_msg = msg_chain.text
            elif isinstance(msg_chain, Voice):
                pass
        if user_msg is not None:
            msg_list = user_msg.split(' ')
            msg = msg_list[0]
            data = None
            if len(msg_list) > 1:
                data = msg_list[1:]

            is_mentioned = self.is_mentioned_bot_in_message(ctx)
            # 计算回复意愿
            current_willing = self.willing_msg.get_willing(ctx)
            self.willing_msg.set_willing(ctx.event.sender_id, current_willing)
            print(target_type)
            print(target_id)
            if target_type == 'group':
                reply_probability = await self.willing_msg.change_reply_willing_received(
                    ctx=ctx,
                    is_mentioned_bot=is_mentioned,
                )
            else:
                reply_probability = 1
                await ctx.send_message(
                    target_type="group",
                    target_id=self.fixed_forwarding_group[0],
                    message=platform_message.MessageChain([
                        platform_message.Plain(text=f'个人，{ctx.event.sender_id}'),
                        platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')

                    ])

                )
            print(f'[概率:{reply_probability * 100:.1f}%]')

            if msg == "hello":  # 如果消息为hello

                # 输出调试信息
                self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))
                await ctx.send_message(
                    target_type=target_type,
                    target_id=target_id,
                    message=platform_message.MessageChain([
                        platform_message.Plain(text=target_type),
                        # platform_message.MiniPrograms(xml_data='''
                        #             \n<msg>\n\t<appmsg appid="" sdkver="0">\n\t\t<title>一起来面试鸭刷题，轻松拿 Offer！</title>\n\t\t<des />\n\t\t<username />\n\t\t<action>view</action>\n\t\t<type>33</type>\n\t\t<showtype>0</showtype>\n\t\t<content />\n\t\t<url>https://mp.weixin.qq.com/mp/waerrpage?appid=wxf64deb2dd310480f&amp;type=upgrade&amp;upgradetype=3#wechat_redirect</url>\n\t\t<lowurl />\n\t\t<forwardflag>0</forwardflag>\n\t\t<dataurl />\n\t\t<lowdataurl />\n\t\t<contentattr>0</contentattr>\n\t\t<streamvideo>\n\t\t\t<streamvideourl />\n\t\t\t<streamvideototaltime>0</streamvideototaltime>\n\t\t\t<streamvideotitle />\n\t\t\t<streamvideowording />\n\t\t\t<streamvideoweburl />\n\t\t\t<streamvideothumburl />\n\t\t\t<streamvideoaduxinfo />\n\t\t\t<streamvideopublishid />\n\t\t</streamvideo>\n\t\t<canvasPageItem>\n\t\t\t<canvasPageXml><![CDATA[]]></canvasPageXml>\n\t\t</canvasPageItem>\n\t\t<appattach>\n\t\t\t<attachid />\n\t\t\t<cdnthumburl>3057020100044b304902010002045c005a0002032f54690204c59a99db020467d82a4b042435616633626534302d383538632d343239382d393239642d6266646335353739383335390204051408030201000405004c4e6100</cdnthumburl>\n\t\t\t<cdnthumbmd5>166d1656b15310044706ba0ce6fec683</cdnthumbmd5>\n\t\t\t<cdnthumblength>21798</cdnthumblength>\n\t\t\t<cdnthumbheight>576</cdnthumbheight>\n\t\t\t<cdnthumbwidth>720</cdnthumbwidth>\n\t\t\t<cdnthumbaeskey>d4606697183b997d3126dab9b08a7ab8</cdnthumbaeskey>\n\t\t\t<aeskey>d4606697183b997d3126dab9b08a7ab8</aeskey>\n\t\t\t<encryver>1</encryver>\n\t\t\t<fileext />\n\t\t\t<islargefilemsg>0</islargefilemsg>\n\t\t</appattach>\n\t\t<extinfo />\n\t\t<androidsource>0</androidsource>\n\t\t<sourceusername>gh_2320846df89c@app</sourceusername>\n\t\t<sourcedisplayname>面试鸭</sourcedisplayname>\n\t\t<commenturl />\n\t\t<thumburl />\n\t\t<mediatagname />\n\t\t<messageaction><![CDATA[]]></messageaction>\n\t\t<messageext><![CDATA[]]></messageext>\n\t\t<emoticongift>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticongift>\n\t\t<emoticonshared>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticonshared>\n\t\t<designershared>\n\t\t\t<designeruin>0</designeruin>\n\t\t\t<designername>null</designername>\n\t\t\t<designerrediretcturl><![CDATA[null]]></designerrediretcturl>\n\t\t</designershared>\n\t\t<emotionpageshared>\n\t\t\t<tid>0</tid>\n\t\t\t<title>null</title>\n\t\t\t<desc>null</desc>\n\t\t\t<iconUrl><![CDATA[null]]></iconUrl>\n\t\t\t<secondUrl>null</secondUrl>\n\t\t\t<pageType>0</pageType>\n\t\t\t<setKey>null</setKey>\n\t\t</emotionpageshared>\n\t\t<webviewshared>\n\t\t\t<shareUrlOriginal />\n\t\t\t<shareUrlOpen />\n\t\t\t<jsAppId />\n\t\t\t<publisherId>wxapp_wxf64deb2dd310480fpages/index/index.html?shareCode=sri7zm</publisherId>\n\t\t\t<publisherReqId />\n\t\t</webviewshared>\n\t\t<template_id />\n\t\t<md5>166d1656b15310044706ba0ce6fec683</md5>\n\t\t<websearch>\n\t\t\t<rec_category>0</rec_category>\n\t\t\t<channelId>0</channelId>\n\t\t</websearch>\n\t\t<weappinfo>\n\t\t\t<pagepath><![CDATA[pages/index/index.html?shareCode=sri7zm]]></pagepath>\n\t\t\t<username>gh_2320846df89c@app</username>\n\t\t\t<appid>wxf64deb2dd310480f</appid>\n\t\t\t<version>66</version>\n\t\t\t<type>2</type>\n\t\t\t<weappiconurl><![CDATA[http://wx.qlogo.cn/mmhead/BO1qQiajiacVmSj2PibMkJaSnccrgXmue68yhMHwg8EL5U3tCudib8oQEmVXDKkQggC0EUzibXGOacs8/96]]></weappiconurl>\n\t\t\t<shareId><![CDATA[1_wxf64deb2dd310480f_31b3ef85c51a97ecc458be1894334026_1742224528_0]]></shareId>\n\t\t\t<appservicetype>0</appservicetype>\n\t\t\t<secflagforsinglepagemode>0</secflagforsinglepagemode>\n\t\t\t<videopageinfo>\n\t\t\t\t<thumbwidth>720</thumbwidth>\n\t\t\t\t<thumbheight>576</thumbheight>\n\t\t\t\t<fromopensdk>0</fromopensdk>\n\t\t\t</videopageinfo>\n\t\t</weappinfo>\n\t\t<statextstr />\n\t\t<musicShareItem>\n\t\t\t<musicDuration>0</musicDuration>\n\t\t</musicShareItem>\n\t\t<finderLiveProductShare>\n\t\t\t<finderLiveID><![CDATA[]]></finderLiveID>\n\t\t\t<finderUsername><![CDATA[]]></finderUsername>\n\t\t\t<finderObjectID><![CDATA[]]></finderObjectID>\n\t\t\t<finderNonceID><![CDATA[]]></finderNonceID>\n\t\t\t<liveStatus><![CDATA[]]></liveStatus>\n\t\t\t<appId><![CDATA[]]></appId>\n\t\t\t<pagePath><![CDATA[]]></pagePath>\n\t\t\t<productId><![CDATA[]]></productId>\n\t\t\t<coverUrl><![CDATA[]]></coverUrl>\n\t\t\t<productTitle><![CDATA[]]></productTitle>\n\t\t\t<marketPrice><![CDATA[0]]></marketPrice>\n\t\t\t<sellingPrice><![CDATA[0]]></sellingPrice>\n\t\t\t<platformHeadImg><![CDATA[]]></platformHeadImg>\n\t\t\t<platformName><![CDATA[]]></platformName>\n\t\t\t<shopWindowId><![CDATA[]]></shopWindowId>\n\t\t\t<flashSalePrice><![CDATA[0]]></flashSalePrice>\n\t\t\t<flashSaleEndTime><![CDATA[0]]></flashSaleEndTime>\n\t\t\t<ecSource><![CDATA[]]></ecSource>\n\t\t\t<sellingPriceWording><![CDATA[]]></sellingPriceWording>\n\t\t\t<platformIconURL><![CDATA[]]></platformIconURL>\n\t\t\t<firstProductTagURL><![CDATA[]]></firstProductTagURL>\n\t\t\t<firstProductTagAspectRatioString><![CDATA[0.0]]></firstProductTagAspectRatioString>\n\t\t\t<secondProductTagURL><![CDATA[]]></secondProductTagURL>\n\t\t\t<secondProductTagAspectRatioString><![CDATA[0.0]]></secondProductTagAspectRatioString>\n\t\t\t<firstGuaranteeWording><![CDATA[]]></firstGuaranteeWording>\n\t\t\t<secondGuaranteeWording><![CDATA[]]></secondGuaranteeWording>\n\t\t\t<thirdGuaranteeWording><![CDATA[]]></thirdGuaranteeWording>\n\t\t\t<isPriceBeginShow>false</isPriceBeginShow>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t\t<promoterKey><![CDATA[]]></promoterKey>\n\t\t\t<discountWording><![CDATA[]]></discountWording>\n\t\t\t<priceSuffixDescription><![CDATA[]]></priceSuffixDescription>\n\t\t\t<productCardKey><![CDATA[]]></productCardKey>\n\t\t\t<isWxShop><![CDATA[]]></isWxShop>\n\t\t\t<brandIconUrl><![CDATA[]]></brandIconUrl>\n\t\t\t<showBoxItemStringList />\n\t\t</finderLiveProductShare>\n\t\t<finderOrder>\n\t\t\t<appID><![CDATA[]]></appID>\n\t\t\t<orderID><![CDATA[]]></orderID>\n\t\t\t<path><![CDATA[]]></path>\n\t\t\t<priceWording><![CDATA[]]></priceWording>\n\t\t\t<stateWording><![CDATA[]]></stateWording>\n\t\t\t<productImageURL><![CDATA[]]></productImageURL>\n\t\t\t<products><![CDATA[]]></products>\n\t\t\t<productsCount><![CDATA[0]]></productsCount>\n\t\t\t<orderType><![CDATA[0]]></orderType>\n\t\t\t<newPriceWording><![CDATA[]]></newPriceWording>\n\t\t\t<newStateWording><![CDATA[]]></newStateWording>\n\t\t\t<useNewWording><![CDATA[0]]></useNewWording>\n\t\t</finderOrder>\n\t\t<finderShopWindowShare>\n\t\t\t<finderUsername><![CDATA[]]></finderUsername>\n\t\t\t<avatar><![CDATA[]]></avatar>\n\t\t\t<nickname><![CDATA[]]></nickname>\n\t\t\t<commodityInStockCount><![CDATA[]]></commodityInStockCount>\n\t\t\t<appId><![CDATA[]]></appId>\n\t\t\t<path><![CDATA[]]></path>\n\t\t\t<appUsername><![CDATA[]]></appUsername>\n\t\t\t<query><![CDATA[]]></query>\n\t\t\t<liteAppId><![CDATA[]]></liteAppId>\n\t\t\t<liteAppPath><![CDATA[]]></liteAppPath>\n\t\t\t<liteAppQuery><![CDATA[]]></liteAppQuery>\n\t\t\t<platformTagURL><![CDATA[]]></platformTagURL>\n\t\t\t<saleWording><![CDATA[]]></saleWording>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t\t<profileTypeWording><![CDATA[]]></profileTypeWording>\n\t\t\t<saleWordingExtra><![CDATA[]]></saleWordingExtra>\n\t\t\t<isWxShop><![CDATA[]]></isWxShop>\n\t\t\t<platformIconUrl><![CDATA[]]></platformIconUrl>\n\t\t\t<brandIconUrl><![CDATA[]]></brandIconUrl>\n\t\t\t<description><![CDATA[]]></description>\n\t\t\t<backgroundUrl><![CDATA[]]></backgroundUrl>\n\t\t\t<darkModePlatformIconUrl><![CDATA[]]></darkModePlatformIconUrl>\n\t\t\t<reputationInfo>\n\t\t\t\t<hasReputationInfo>0</hasReputationInfo>\n\t\t\t\t<reputationScore>0</reputationScore>\n\t\t\t\t<reputationWording />\n\t\t\t\t<reputationTextColor />\n\t\t\t\t<reputationLevelWording />\n\t\t\t\t<reputationBackgroundColor />\n\t\t\t</reputationInfo>\n\t\t\t<productImageURLList />\n\t\t</finderShopWindowShare>\n\t\t<findernamecard>\n\t\t\t<username />\n\t\t\t<avatar><![CDATA[]]></avatar>\n\t\t\t<nickname />\n\t\t\t<auth_job />\n\t\t\t<auth_icon>0</auth_icon>\n\t\t\t<auth_icon_url />\n\t\t\t<ecSource><![CDATA[]]></ecSource>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t</findernamecard>\n\t\t<finderGuarantee>\n\t\t\t<scene><![CDATA[0]]></scene>\n\t\t</finderGuarantee>\n\t\t<directshare>0</directshare>\n\t\t<gamecenter>\n\t\t\t<namecard>\n\t\t\t\t<iconUrl />\n\t\t\t\t<name />\n\t\t\t\t<desc />\n\t\t\t\t<tail />\n\t\t\t\t<jumpUrl />\n\t\t\t</namecard>\n\t\t</gamecenter>\n\t\t<patMsg>\n\t\t\t<chatUser />\n\t\t\t<records>\n\t\t\t\t<recordNum>0</recordNum>\n\t\t\t</records>\n\t\t</patMsg>\n\t\t<secretmsg>\n\t\t\t<issecretmsg>0</issecretmsg>\n\t\t</secretmsg>\n\t\t<referfromscene>0</referfromscene>\n\t\t<gameshare>\n\t\t\t<liteappext>\n\t\t\t\t<liteappbizdata />\n\t\t\t\t<priority>0</priority>\n\t\t\t</liteappext>\n\t\t\t<appbrandext>\n\t\t\t\t<litegameinfo />\n\t\t\t\t<priority>-1</priority>\n\t\t\t</appbrandext>\n\t\t\t<gameshareid />\n\t\t\t<sharedata />\n\t\t\t<isvideo>0</isvideo>\n\t\t\t<duration>-1</duration>\n\t\t\t<isexposed>0</isexposed>\n\t\t\t<readtext />\n\t\t</gameshare>\n\t\t<mpsharetrace>\n\t\t\t<hasfinderelement>0</hasfinderelement>\n\t\t\t<lastgmsgid />\n\t\t</mpsharetrace>\n\t\t<wxgamecard>\n\t\t\t<framesetname />\n\t\t\t<mbcarddata />\n\t\t\t<minpkgversion />\n\t\t\t<clientextinfo />\n\t\t\t<mbcardheight>0</mbcardheight>\n\t\t\t<isoldversion>0</isoldversion>\n\t\t</wxgamecard>\n\t\t<liteapp>\n\t\t\t<id>null</id>\n\t\t\t<path />\n\t\t\t<query />\n\t\t\t<istransparent>0</istransparent>\n\t\t\t<hideicon>0</hideicon>\n\t\t</liteapp>\n\t\t<finderCollection>\n\t\t\t<feedCount>0</feedCount>\n\t\t\t<collectionTopicType>0</collectionTopicType>\n\t\t\t<paidCollectionType>0</paidCollectionType>\n\t\t\t<price>0</price>\n\t\t\t<title />\n\t\t\t<collectionId>0</collectionId>\n\t\t\t<thumbUrl />\n\t\t\t<collectionDesc />\n\t\t\t<authorUsername />\n\t\t\t<nickname />\n\t\t\t<avatarURL />\n\t\t\t<authIconURL />\n\t\t\t<authIconType>0</authIconType>\n\t\t</finderCollection>\n\t</appmsg>\n\t<fromusername>wxid_xd12odto989122</fromusername>\n\t<scene>0</scene>\n\t<appinfo>\n\t\t<version>1</version>\n\t\t<appname></appname>\n\t</appinfo>\n\t<commenturl></commenturl>\n</msg>\n
                        #             ''')
                        platform_message.WeChatMiniPrograms(mini_app_id='wxf64deb2dd310480f',
                                                            user_name='gh_2320846df89c@app'),
                        platform_message.WeChatLink(link_title='一起吃坑德基啊，哈哈', link_url='https://napcat.apifox.cn/',
                                                    link_thumb_url='https://pics3.baidu.com/feed/0824ab18972bd407a9403f336648d15c0db30943.jpeg@f_auto?token=d26f7f142871542956aaa13799ba1946',
                                                    link_desc='好吃的坑德基'),
                        platform_message.WeChatForwardMiniPrograms(xml_data='''
            <msg>\n\t<appmsg appid=\"\" sdkver=\"0\">\n\t\t<title>群聊的聊天记录</title>\n\t\t<des>     YYL: [图片]\n     YYL: [图片]\n     YYL: [图片]</des>\n\t\t<username />\n\t\t<action>view</action>\n\t\t<type>19</type>\n\t\t<showtype>0</showtype>\n\t\t<content />\n\t\t<url>https://support.weixin.qq.com/cgi-bin/mmsupport-bin/readtemplate?t=page/favorite_record__w_unsupport&amp;from=singlemessage&amp;isappinstalled=0</url>\n\t\t<lowurl />\n\t\t<forwardflag>0</forwardflag>\n\t\t<dataurl />\n\t\t<lowdataurl />\n\t\t<contentattr>0</contentattr>\n\t\t<streamvideo>\n\t\t\t<streamvideourl />\n\t\t\t<streamvideototaltime>0</streamvideototaltime>\n\t\t\t<streamvideotitle />\n\t\t\t<streamvideowording />\n\t\t\t<streamvideoweburl />\n\t\t\t<streamvideothumburl />\n\t\t\t<streamvideoaduxinfo />\n\t\t\t<streamvideopublishid />\n\t\t</streamvideo>\n\t\t<canvasPageItem>\n\t\t\t<canvasPageXml><![CDATA[]]></canvasPageXml>\n\t\t</canvasPageItem>\n\t\t<recorditem>&lt;recordinfo&gt;&lt;title&gt;群聊的聊天记录&lt;/title&gt;&lt;desc&gt;     YYL:&amp;#x20;[图片]&amp;#x0A;     YYL:&amp;#x20;[图片]&amp;#x0A;     YYL:&amp;#x20;[图片]&lt;/desc&gt;&lt;datalist count=\"3\"&gt;&lt;dataitem datatype=\"2\" dataid=\"ce0e45befbb0e3b38bebbed1d56a69c1\" datasourceid=\"991203218749297610\"&gt;&lt;cdnthumburl&gt;3057020100044b30490201000204ab76c7c602032f54690204b69999db020467fd36b3042435363461323166342d376332302d346536372d393161662d6261373865353861643936630204059420010201000405004c55cd00&lt;/cdnthumburl&gt;&lt;cdnthumbkey&gt;3ce117cab5f81dbb55063960ee8881d8&lt;/cdnthumbkey&gt;&lt;thumbfullmd5&gt;93da20911f66968ae750ee483aafe1f4&lt;/thumbfullmd5&gt;&lt;thumbsize&gt;5059&lt;/thumbsize&gt;&lt;cdndataurl&gt;3057020100044b30490201000204ab76c7c602032f54690204b69999db020467fd36b4042434353030313133662d303438332d346233302d616235382d3761613336393732313730650204059820010201000405004c4d3500&lt;/cdndataurl&gt;&lt;cdndatakey&gt;6f298b1772a0550eda99a3495c3bbf4c&lt;/cdndatakey&gt;&lt;fullmd5&gt;59d82243af06e32d3239910b2a7b48d3&lt;/fullmd5&gt;&lt;datasize&gt;573410&lt;/datasize&gt;&lt;head256md5&gt;f81ed3faee772d7b78bebefe82e0a0bc&lt;/head256md5&gt;&lt;thumbhead256md5&gt;bae3df6c65423d9b751be9f127ab8de3&lt;/thumbhead256md5&gt;&lt;sourcename&gt;     YYL&lt;/sourcename&gt;&lt;sourceheadurl&gt;https://wx.qlogo.cn/mmhead/ver_1/s5tPcGWZXiaDHdCoEzGCNakA6hQEiacR6g2ibh4eUA5gu3xLEvJNjibKH2FoHkqfHrQ8HZYicqExwqFRX3M8tBs8KXIxZPMNWwmnIW1Wj6H3jeTwYUiat76wticbCzshIe6lnw6FzjRMcDTOYuSxLhyTxsuUQ/96&lt;/sourceheadurl&gt;&lt;sourcetime&gt;2025-04-15&amp;#x20;00:23:59&lt;/sourcetime&gt;&lt;srcMsgCreateTime&gt;1744647839&lt;/srcMsgCreateTime&gt;&lt;messageuuid&gt;99e0e38d3a6e73b9aeb959356594654a_&lt;/messageuuid&gt;&lt;fromnewmsgid&gt;991203218749297610&lt;/fromnewmsgid&gt;&lt;dataitemsource&gt;&lt;hashusername&gt;6965fd925f3b2d274bedd3f1d9199efe7caec36b2feb4eec763f07f26dff0a69&lt;/hashusername&gt;&lt;/dataitemsource&gt;&lt;/dataitem&gt;&lt;dataitem datatype=\"2\" dataid=\"38b777197059ecd5ac301d4ef2d5ddf7\" datasourceid=\"6722669015891703397\"&gt;&lt;cdnthumburl&gt;3057020100044b30490201000204ab76c7c602032f54690204b69999db020467fd36b4042433613261616264362d366264642d346131622d383430322d6362343239353765653866300204059420010201000405004c511d00&lt;/cdnthumburl&gt;&lt;cdnthumbkey&gt;151fe157de9fc98c288ea4d436968fff&lt;/cdnthumbkey&gt;&lt;thumbfullmd5&gt;caf44746a49604e923200be391796964&lt;/thumbfullmd5&gt;&lt;thumbsize&gt;2936&lt;/thumbsize&gt;&lt;cdndataurl&gt;3057020100044b30490201000204ab76c7c602032f54690204b69999db020467fd36b4042465643864656235302d386164362d346562632d626236312d3762623432313832633061640204059420010201000405004c55cd00&lt;/cdndataurl&gt;&lt;cdndatakey&gt;04dcfc7f3cf2a75c209df335f1d71d79&lt;/cdndatakey&gt;&lt;fullmd5&gt;b74de48f7cdd1b8aac6f088fb58bdd2c&lt;/fullmd5&gt;&lt;datasize&gt;139352&lt;/datasize&gt;&lt;head256md5&gt;da820b8ac528d57e14cf69acc6c3d3d8&lt;/head256md5&gt;&lt;thumbhead256md5&gt;dbf372bbbb6f5a9ad04a07d1f399d0ce&lt;/thumbhead256md5&gt;&lt;sourcename&gt;     YYL&lt;/sourcename&gt;&lt;sourceheadurl&gt;https://wx.qlogo.cn/mmhead/ver_1/s5tPcGWZXiaDHdCoEzGCNakA6hQEiacR6g2ibh4eUA5gu3xLEvJNjibKH2FoHkqfHrQ8HZYicqExwqFRX3M8tBs8KXIxZPMNWwmnIW1Wj6H3jeTwYUiat76wticbCzshIe6lnw6FzjRMcDTOYuSxLhyTxsuUQ/96&lt;/sourceheadurl&gt;&lt;sourcetime&gt;2025-04-15&amp;#x20;00:23:59&lt;/sourcetime&gt;&lt;srcMsgCreateTime&gt;1744647839&lt;/srcMsgCreateTime&gt;&lt;messageuuid&gt;0aadb15eb41936e7f51c11914d80f35b_&lt;/messageuuid&gt;&lt;fromnewmsgid&gt;6722669015891703397&lt;/fromnewmsgid&gt;&lt;dataitemsource&gt;&lt;hashusername&gt;6965fd925f3b2d274bedd3f1d9199efe7caec36b2feb4eec763f07f26dff0a69&lt;/hashusername&gt;&lt;/dataitemsource&gt;&lt;/dataitem&gt;&lt;dataitem datatype=\"2\" dataid=\"cfd952b8e7eb0b6f0b31de0aa9194daa\" datasourceid=\"6642716835806983418\"&gt;&lt;cdnthumburl&gt;3057020100044b30490201000204ab76c7c602032f54690204b69999db020467fd36b4042464646163396131652d623464362d343034312d383664322d3564396633623737383734340204059420010201000405004c53d900&lt;/cdnthumburl&gt;&lt;cdnthumbkey&gt;1c776388315c9a2ff2469d21dafa4946&lt;/cdnthumbkey&gt;&lt;thumbfullmd5&gt;cf40ecb7ee16ff8d32c336a1d1a162fb&lt;/thumbfullmd5&gt;&lt;thumbsize&gt;3202&lt;/thumbsize&gt;&lt;cdndataurl&gt;3057020100044b30490201000204ab76c7c602032f54690204b69999db020467fd36b3042432366437356161392d643539652d346139342d613034312d6436653933633662326534350204059420010201000405004c4e6100&lt;/cdndataurl&gt;&lt;cdndatakey&gt;c880ad0f6bc497b5bd00638aed2357ae&lt;/cdndatakey&gt;&lt;fullmd5&gt;569cfa8c57d760f9ecec8efc90c63cfa&lt;/fullmd5&gt;&lt;datasize&gt;187595&lt;/datasize&gt;&lt;head256md5&gt;da820b8ac528d57e14cf69acc6c3d3d8&lt;/head256md5&gt;&lt;thumbhead256md5&gt;dbf372bbbb6f5a9ad04a07d1f399d0ce&lt;/thumbhead256md5&gt;&lt;sourcename&gt;     YYL&lt;/sourcename&gt;&lt;sourceheadurl&gt;https://wx.qlogo.cn/mmhead/ver_1/s5tPcGWZXiaDHdCoEzGCNakA6hQEiacR6g2ibh4eUA5gu3xLEvJNjibKH2FoHkqfHrQ8HZYicqExwqFRX3M8tBs8KXIxZPMNWwmnIW1Wj6H3jeTwYUiat76wticbCzshIe6lnw6FzjRMcDTOYuSxLhyTxsuUQ/96&lt;/sourceheadurl&gt;&lt;sourcetime&gt;2025-04-15&amp;#x20;00:23:59&lt;/sourcetime&gt;&lt;srcMsgCreateTime&gt;1744647839&lt;/srcMsgCreateTime&gt;&lt;messageuuid&gt;32867fe6193ec630aabb11dbebe71bf7_&lt;/messageuuid&gt;&lt;fromnewmsgid&gt;6642716835806983418&lt;/fromnewmsgid&gt;&lt;dataitemsource&gt;&lt;hashusername&gt;6965fd925f3b2d274bedd3f1d9199efe7caec36b2feb4eec763f07f26dff0a69&lt;/hashusername&gt;&lt;/dataitemsource&gt;&lt;/dataitem&gt;&lt;/datalist&gt;&lt;favcreatetime&gt;1744647859497&lt;/favcreatetime&gt;&lt;/recordinfo&gt;</recorditem>\n\t\t<appattach>\n\t\t\t<attachid />\n\t\t\t<cdnthumburl>3057020100044b304902010002045c005a0002032f54690204929999db020467fd36b4042461316564396137332d356135612d343461322d383866392d3132333134636631643935370204051408030201000405004c4dfd00</cdnthumburl>\n\t\t\t<cdnthumbmd5>93da20911f66968ae750ee483aafe1f4</cdnthumbmd5>\n\t\t\t<cdnthumblength>5059</cdnthumblength>\n\t\t\t<cdnthumbheight>180</cdnthumbheight>\n\t\t\t<cdnthumbwidth>180</cdnthumbwidth>\n\t\t\t<cdnthumbaeskey>cb0a8afa30318b68d22cd65c5398a238</cdnthumbaeskey>\n\t\t\t<aeskey>cb0a8afa30318b68d22cd65c5398a238</aeskey>\n\t\t\t<encryver>1</encryver>\n\t\t\t<fileext />\n\t\t\t<islargefilemsg>0</islargefilemsg>\n\t\t</appattach>\n\t\t<extinfo />\n\t\t<androidsource>0</androidsource>\n\t\t<thumburl />\n\t\t<mediatagname />\n\t\t<messageaction><![CDATA[]]></messageaction>\n\t\t<messageext><![CDATA[]]></messageext>\n\t\t<emoticongift>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticongift>\n\t\t<emoticonshared>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticonshared>\n\t\t<designershared>\n\t\t\t<designeruin>0</designeruin>\n\t\t\t<designername>null</designername>\n\t\t\t<designerrediretcturl><![CDATA[null]]></designerrediretcturl>\n\t\t</designershared>\n\t\t<emotionpageshared>\n\t\t\t<tid>0</tid>\n\t\t\t<title>null</title>\n\t\t\t<desc>null</desc>\n\t\t\t<iconUrl><![CDATA[null]]></iconUrl>\n\t\t\t<secondUrl />\n\t\t\t<pageType>0</pageType>\n\t\t\t<setKey>null</setKey>\n\t\t</emotionpageshared>\n\t\t<webviewshared>\n\t\t\t<shareUrlOriginal />\n\t\t\t<shareUrlOpen />\n\t\t\t<jsAppId />\n\t\t\t<publisherId />\n\t\t\t<publisherReqId />\n\t\t</webviewshared>\n\t\t<template_id />\n\t\t<md5>93da20911f66968ae750ee483aafe1f4</md5>\n\t\t<websearch />\n\t\t<weappinfo>\n\t\t\t<username />\n\t\t\t<appid />\n\t\t\t<appservicetype>0</appservicetype>\n\t\t\t<secflagforsinglepagemode>0</secflagforsinglepagemode>\n\t\t\t<videopageinfo>\n\t\t\t\t<thumbwidth>180</thumbwidth>\n\t\t\t\t<thumbheight>180</thumbheight>\n\t\t\t\t<fromopensdk>0</fromopensdk>\n\t\t\t</videopageinfo>\n\t\t</weappinfo>\n\t\t<statextstr />\n\t\t<musicShareItem>\n\t\t\t<musicDuration>0</musicDuration>\n\t\t</musicShareItem>\n\t\t<finderLiveProductShare>\n\t\t\t<finderLiveID><![CDATA[]]></finderLiveID>\n\t\t\t<finderUsername><![CDATA[]]></finderUsername>\n\t\t\t<finderObjectID><![CDATA[]]></finderObjectID>\n\t\t\t<finderNonceID><![CDATA[]]></finderNonceID>\n\t\t\t<liveStatus><![CDATA[]]></liveStatus>\n\t\t\t<appId><![CDATA[]]></appId>\n\t\t\t<pagePath><![CDATA[]]></pagePath>\n\t\t\t<productId><![CDATA[]]></productId>\n\t\t\t<coverUrl><![CDATA[]]></coverUrl>\n\t\t\t<productTitle><![CDATA[]]></productTitle>\n\t\t\t<marketPrice><![CDATA[0]]></marketPrice>\n\t\t\t<sellingPrice><![CDATA[0]]></sellingPrice>\n\t\t\t<platformHeadImg><![CDATA[]]></platformHeadImg>\n\t\t\t<platformName><![CDATA[]]></platformName>\n\t\t\t<shopWindowId><![CDATA[]]></shopWindowId>\n\t\t\t<flashSalePrice><![CDATA[0]]></flashSalePrice>\n\t\t\t<flashSaleEndTime><![CDATA[0]]></flashSaleEndTime>\n\t\t\t<ecSource><![CDATA[]]></ecSource>\n\t\t\t<sellingPriceWording><![CDATA[]]></sellingPriceWording>\n\t\t\t<platformIconURL><![CDATA[]]></platformIconURL>\n\t\t\t<firstProductTagURL><![CDATA[]]></firstProductTagURL>\n\t\t\t<firstProductTagAspectRatioString><![CDATA[0.0]]></firstProductTagAspectRatioString>\n\t\t\t<secondProductTagURL><![CDATA[]]></secondProductTagURL>\n\t\t\t<secondProductTagAspectRatioString><![CDATA[0.0]]></secondProductTagAspectRatioString>\n\t\t\t<firstGuaranteeWording><![CDATA[]]></firstGuaranteeWording>\n\t\t\t<secondGuaranteeWording><![CDATA[]]></secondGuaranteeWording>\n\t\t\t<thirdGuaranteeWording><![CDATA[]]></thirdGuaranteeWording>\n\t\t\t<isPriceBeginShow>false</isPriceBeginShow>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t\t<promoterKey><![CDATA[]]></promoterKey>\n\t\t\t<discountWording><![CDATA[]]></discountWording>\n\t\t\t<priceSuffixDescription><![CDATA[]]></priceSuffixDescription>\n\t\t\t<productCardKey><![CDATA[]]></productCardKey>\n\t\t\t<isWxShop><![CDATA[]]></isWxShop>\n\t\t\t<brandIconUrl><![CDATA[]]></brandIconUrl>\n\t\t\t<showBoxItemStringList />\n\t\t</finderLiveProductShare>\n\t\t<finderOrder>\n\t\t\t<appID><![CDATA[]]></appID>\n\t\t\t<orderID><![CDATA[]]></orderID>\n\t\t\t<path><![CDATA[]]></path>\n\t\t\t<priceWording><![CDATA[]]></priceWording>\n\t\t\t<stateWording><![CDATA[]]></stateWording>\n\t\t\t<productImageURL><![CDATA[]]></productImageURL>\n\t\t\t<products><![CDATA[]]></products>\n\t\t\t<productsCount><![CDATA[0]]></productsCount>\n\t\t\t<orderType><![CDATA[0]]></orderType>\n\t\t\t<newPriceWording><![CDATA[]]></newPriceWording>\n\t\t\t<newStateWording><![CDATA[]]></newStateWording>\n\t\t\t<useNewWording><![CDATA[0]]></useNewWording>\n\t\t</finderOrder>\n\t\t<finderShopWindowShare>\n\t\t\t<finderUsername><![CDATA[]]></finderUsername>\n\t\t\t<avatar><![CDATA[]]></avatar>\n\t\t\t<nickname><![CDATA[]]></nickname>\n\t\t\t<commodityInStockCount><![CDATA[]]></commodityInStockCount>\n\t\t\t<appId><![CDATA[]]></appId>\n\t\t\t<path><![CDATA[]]></path>\n\t\t\t<appUsername><![CDATA[]]></appUsername>\n\t\t\t<query><![CDATA[]]></query>\n\t\t\t<liteAppId><![CDATA[]]></liteAppId>\n\t\t\t<liteAppPath><![CDATA[]]></liteAppPath>\n\t\t\t<liteAppQuery><![CDATA[]]></liteAppQuery>\n\t\t\t<platformTagURL><![CDATA[]]></platformTagURL>\n\t\t\t<saleWording><![CDATA[]]></saleWording>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t\t<profileTypeWording><![CDATA[]]></profileTypeWording>\n\t\t\t<saleWordingExtra><![CDATA[]]></saleWordingExtra>\n\t\t\t<isWxShop><![CDATA[]]></isWxShop>\n\t\t\t<platformIconUrl><![CDATA[]]></platformIconUrl>\n\t\t\t<brandIconUrl><![CDATA[]]></brandIconUrl>\n\t\t\t<description><![CDATA[]]></description>\n\t\t\t<backgroundUrl><![CDATA[]]></backgroundUrl>\n\t\t\t<darkModePlatformIconUrl><![CDATA[]]></darkModePlatformIconUrl>\n\t\t\t<reputationInfo>\n\t\t\t\t<hasReputationInfo>0</hasReputationInfo>\n\t\t\t\t<reputationScore>0</reputationScore>\n\t\t\t\t<reputationWording />\n\t\t\t\t<reputationTextColor />\n\t\t\t\t<reputationLevelWording />\n\t\t\t\t<reputationBackgroundColor />\n\t\t\t</reputationInfo>\n\t\t\t<productImageURLList />\n\t\t</finderShopWindowShare>\n\t\t<findernamecard>\n\t\t\t<username />\n\t\t\t<avatar><![CDATA[]]></avatar>\n\t\t\t<nickname />\n\t\t\t<auth_job />\n\t\t\t<auth_icon>0</auth_icon>\n\t\t\t<auth_icon_url />\n\t\t\t<ecSource><![CDATA[]]></ecSource>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t</findernamecard>\n\t\t<finderGuarantee>\n\t\t\t<scene><![CDATA[0]]></scene>\n\t\t</finderGuarantee>\n\t\t<directshare>0</directshare>\n\t\t<gamecenter>\n\t\t\t<namecard>\n\t\t\t\t<iconUrl />\n\t\t\t\t<name />\n\t\t\t\t<desc />\n\t\t\t\t<tail />\n\t\t\t\t<jumpUrl />\n\t\t\t</namecard>\n\t\t</gamecenter>\n\t\t<patMsg>\n\t\t\t<chatUser />\n\t\t\t<records>\n\t\t\t\t<recordNum>0</recordNum>\n\t\t\t</records>\n\t\t</patMsg>\n\t\t<secretmsg>\n\t\t\t<issecretmsg>0</issecretmsg>\n\t\t</secretmsg>\n\t\t<referfromscene>0</referfromscene>\n\t\t<gameshare>\n\t\t\t<liteappext>\n\t\t\t\t<liteappbizdata />\n\t\t\t\t<priority>0</priority>\n\t\t\t</liteappext>\n\t\t\t<appbrandext>\n\t\t\t\t<litegameinfo />\n\t\t\t\t<priority>-1</priority>\n\t\t\t</appbrandext>\n\t\t\t<gameshareid />\n\t\t\t<sharedata />\n\t\t\t<isvideo>0</isvideo>\n\t\t\t<duration>0</duration>\n\t\t\t<isexposed>0</isexposed>\n\t\t\t<readtext />\n\t\t</gameshare>\n\t\t<mpsharetrace>\n\t\t\t<hasfinderelement>0</hasfinderelement>\n\t\t\t<lastgmsgid />\n\t\t</mpsharetrace>\n\t\t<wxgamecard>\n\t\t\t<framesetname />\n\t\t\t<mbcarddata />\n\t\t\t<minpkgversion />\n\t\t\t<clientextinfo />\n\t\t\t<mbcardheight>0</mbcardheight>\n\t\t\t<isoldversion>0</isoldversion>\n\t\t</wxgamecard>\n\t\t<liteapp>\n\t\t\t<id>null</id>\n\t\t\t<path />\n\t\t\t<query />\n\t\t\t<istransparent>0</istransparent>\n\t\t\t<hideicon>0</hideicon>\n\t\t</liteapp>\n\t\t<opensdk_share_is_modified>0</opensdk_share_is_modified>\n\t</appmsg>\n\t<fromusername>wxid_xd12odto989122</fromusername>\n\t<scene>0</scene>\n\t<appinfo>\n\t\t<version>1</version>\n\t\t<appname></appname>\n\t</appinfo>\n\t<commenturl></commenturl>\n</msg>\n

                                '''),
                        # platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')
                    ])

                )


            elif msg == '菜单':
                await ctx.reply(platform_message.MessageChain([platform_message.Plain(f'看妹妹\n天气\n早报\n吸猫\n')]))

            elif msg == '定时':
                task_name = data[0]
                hour, minute = map(int, data[-1].split("-"))
                now_time = datetime.now()
                adapter = 'gewechat'
                task_time = now_time.replace(hour=hour, minute=minute).strftime("%Y-%m-%d %H-%M-%S")
                target_type = ctx.event.launcher_type
                target_id = ctx.event.launcher_id

                await self.asyautotask.add_task(ctx, task_name, task_time, target_type, target_id, adapter)
            elif msg == '查询任务':
                await self.asyautotask.get_pending_tasks(ctx)
            else:
                if data:
                    await util_handler.handle(msg, ctx, data)
                else:
                    await util_handler.handle(msg, ctx)

            model_info = await self.ap.model_mgr.get_model_by_name(self.ap.provider_cfg.data['model'])
            print(model_info)
            error_date = 'f请判断用户要你设定的时间是否正确。' \
                         '1.如果有具体时间请遵循一下规则：' \
                         '正确应该是一年只有12月，' \
                         '一个月只有28(平年)，29(闰年)，30(小月)，31(大月)天,' \
                         '一天只有24小时，' \
                         '一小时只有60分钟，' \
                         '一分钟只有60秒。' \
                         '2.如果是在某年某月某天之后请推算时间' \
                         '提醒或者定时不应该在当前时间之前,' \
                         '如果没有具体的小时有大概时间点也算正确，' \
                         f'用户消息：{user_msg},' \
                         f'当前时间：{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}' \
                         f'只用返回‘是’或‘否’'
            pd_proempt = f'判断用户是否要你去定时执行什么或者提醒做什么，' \
                         f'用户消息中有具体某个时间或者时间点，' \
                         f'只用返回‘是’或‘否’问题:{user_msg}'
            message = [llm_entities.Message(role="user", content=pd_proempt)]
            pd_resp = await model_info.requester.call(None, model=model_info, messages=message)
            print(pd_resp.content)
            if pd_resp.content == '是':
                message = [llm_entities.Message(role="user", content=error_date)]
                date_pd_resp = await model_info.requester.call(None, model=model_info, messages=message)
                print(date_pd_resp)
                if date_pd_resp.content == '是':

                    now_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
                    return_data = '''{
                  "reminder_id": "eye-care-001",
                  "title": "公园眼保健操",
                  "description": "每天中午12点去公园做10分钟眼保健操",
                  "time": "12:00:00",
                  "timezone": "Asia/Shanghai",
                  "repeat": {
                    "type": "daily"
                  },
                  "reminder_methods": [
                    {
                      "type": "gewe",
                      "message": "该去公园做眼保健操啦！🌳👀"
                    }
                  ],
                }'''

                    prompt = f'请将用户输入的问题：{user_msg}。提取问题中的详细事件、时间、要求、人物。' \
                             f'时间为24小时制。' \
                             f'如果有多少年、多少月，多少天之后就按照当前时间推算。' \
                             f'如果没有具体的小时或者分钟，请大概生成一个合理的时间。' \
                             f'如果是在某年某月某天之后请推算时间' \
                             f'例如：提醒我每天中午去公园做眼保健操' \
                             f'返回示例：' \
                             f'{return_data}' \
                             f'' \
                             f'现在时间为{now_time}，' \
                             f'只返回json,不用返回其他内容'
                    user_prompt = {
                        "task": prompt,
                        "output_format": 'json',
                    }
                    user_prompt = json.dumps(user_prompt, ensure_ascii=False).strip()
                    message = [llm_entities.Message(role="user", content=user_prompt)]
                    resp = await model_info.requester.call(None, model=model_info, messages=message)
                    print(resp.content)
                    match = re.search(r'{[\s\S]*}', resp.content)
                    if match:
                        json_str = match.group(0)
                    else:
                        json_str = {'mesg': 'error'}
                    # data = json.loads(json_str)

                    zhuti = json.loads(json_str)
                    selp_time = len(zhuti) * 0.5
                    await asyncio.sleep(selp_time)
                    await ctx.reply(MessageChain([Plain(str(zhuti))]))
                else:
                    data_prompt = '请人性化的告诉用户，用户消息中要设定的提醒时间是有问题的，问题在哪。' \
                                  '例如：提醒我2024年13月33日8时起床。' \
                                  '返回示例：现在都2025年了，况且一年哪来的13个月，一个月哪来的33天啊...' \
                                  '一年只有12月，' \
                                  '一个月只有28(平年)，29(闰年)，30(小月)，31(大月)天,' \
                                  '一天只有24小时，' \
                                  '一小时只有60分钟，' \
                                  '一分钟只有60秒，' \
                                  '提醒或者定时不应该在当前时间之前' \
                                  f'用户消息：{user_msg}' \
                                  f'当前时间：{datetime.now().strftime("%Y-%m-%d %H-%M-%S")}'
                    message = [llm_entities.Message(role="user", content=data_prompt)]
                    pd_resp = await model_info.requester.call(None, model=model_info, messages=message)
                    await ctx.reply(MessageChain([Plain(str(pd_resp.content))]))
            elif random() < reply_probability:
                message = [llm_entities.Message(role="user", content=user_msg)]
                pd_resp = await model_info.requester.call(None, model=model_info, messages=message)
                await ctx.reply(MessageChain([Plain(str(pd_resp.content))]))
                # pass







    # 插件卸载时触发
    def __del__(self):
        pass


