# import traceback

from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import asyncio
import re
from plugins.MessageForwarding.utils.inquire import BotInquire
# import pkg.platform.types as platform_types
from pkg.platform.types import *
import json
import os
import importlib

from pkg.provider import entities as llm_entities
from pkg.core import app




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
        # self.task_file = os.path.join(os.path.dirname(__file__), 'tasks.json')  # 统一文件名
        # self.check_timer_task = asyncio.create_task(self.asyautotask.load_tasks())
        # self.asyautotask_start = await self.asyautotask.start()


        # pass

    # 异步初始化
    async def initialize(self):

        await self.asyautotask.start()

        # print(self.host.get_platform_adapters())

        async def send_message():
            print("send message start waiting")
            await asyncio.sleep(90)

            try:
                await self.host.send_active_message(
                    adapter=self.host.get_platform_adapters()[0],
                    target_type="group",
                    target_id="48371594138@chatroom",
                    message=platform_message.MessageChain([
                        platform_message.At(target='wxid_xd12odto989122'),
                        platform_message.Plain(text='haha')
                        # platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')

                    ])
                )
            except Exception as e:
                return e
            print("send message end")

        asyncio.get_running_loop().create_task(send_message())

    # 当收到个人消息时触发
    @handler(PersonNormalMessageReceived)
    async def person_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 PersonNormalMessageReceived 的对象
        # if msg == "hello":  # 如果消息为hello
        #
        #     # 输出调试信息
        #     self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))
        #
        #
        #
        #
        #     # 回复消息 "hello, <发送者id>!"
        #     # ctx.add_return("reply", ["hello, {}!".format(ctx.event.sender_id)])
        #
        #     # 阻止该事件默认行为（向接口获取回复）
        #     ctx.prevent_default()
        self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))

        print(ctx.host.get_platform_adapters())
        print(ctx.event.launcher_type)
        la_type = ctx.event.launcher_type
        await ctx.host.send_active_message(
            adapter=self.host.get_platform_adapters()[0],
            target_type="group",
            target_id="48371594138@chatroom",
            message=platform_message.MessageChain([
                # platform_message.At(target='wxid_xd12odto989122'),
                platform_message.Plain(text='个人')
                # platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')

            ])

        )
        # ctx.add_return("reply", ["hello, everyone!"])

        ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupMessageReceived)
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        # print(ctx.event.text_message)
        all_msg = [i for i in ctx.event.query.message_chain if not isinstance(i, platform_message.At)][0].text
        # print(msg, type(msg))
        msg_list = all_msg.split()
        msg = msg_list[0]
        data = None
        if len(msg_list) > 1:
            data = msg_list[1:]
        # msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == "hello":  # 如果消息为hello

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))
            await ctx.host.send_active_message(
                adapter=self.host.get_platform_adapters()[0],
                target_type="group",
                target_id="48371594138@chatroom",
                message=platform_message.MessageChain([
                    platform_message.At(target='wxid_xd12odto989122'),
                    platform_message.Plain(text='群聊'),
                    # platform_message.MiniPrograms(xml_data='''
                    #             \n<msg>\n\t<appmsg appid="" sdkver="0">\n\t\t<title>一起来面试鸭刷题，轻松拿 Offer！</title>\n\t\t<des />\n\t\t<username />\n\t\t<action>view</action>\n\t\t<type>33</type>\n\t\t<showtype>0</showtype>\n\t\t<content />\n\t\t<url>https://mp.weixin.qq.com/mp/waerrpage?appid=wxf64deb2dd310480f&amp;type=upgrade&amp;upgradetype=3#wechat_redirect</url>\n\t\t<lowurl />\n\t\t<forwardflag>0</forwardflag>\n\t\t<dataurl />\n\t\t<lowdataurl />\n\t\t<contentattr>0</contentattr>\n\t\t<streamvideo>\n\t\t\t<streamvideourl />\n\t\t\t<streamvideototaltime>0</streamvideototaltime>\n\t\t\t<streamvideotitle />\n\t\t\t<streamvideowording />\n\t\t\t<streamvideoweburl />\n\t\t\t<streamvideothumburl />\n\t\t\t<streamvideoaduxinfo />\n\t\t\t<streamvideopublishid />\n\t\t</streamvideo>\n\t\t<canvasPageItem>\n\t\t\t<canvasPageXml><![CDATA[]]></canvasPageXml>\n\t\t</canvasPageItem>\n\t\t<appattach>\n\t\t\t<attachid />\n\t\t\t<cdnthumburl>3057020100044b304902010002045c005a0002032f54690204c59a99db020467d82a4b042435616633626534302d383538632d343239382d393239642d6266646335353739383335390204051408030201000405004c4e6100</cdnthumburl>\n\t\t\t<cdnthumbmd5>166d1656b15310044706ba0ce6fec683</cdnthumbmd5>\n\t\t\t<cdnthumblength>21798</cdnthumblength>\n\t\t\t<cdnthumbheight>576</cdnthumbheight>\n\t\t\t<cdnthumbwidth>720</cdnthumbwidth>\n\t\t\t<cdnthumbaeskey>d4606697183b997d3126dab9b08a7ab8</cdnthumbaeskey>\n\t\t\t<aeskey>d4606697183b997d3126dab9b08a7ab8</aeskey>\n\t\t\t<encryver>1</encryver>\n\t\t\t<fileext />\n\t\t\t<islargefilemsg>0</islargefilemsg>\n\t\t</appattach>\n\t\t<extinfo />\n\t\t<androidsource>0</androidsource>\n\t\t<sourceusername>gh_2320846df89c@app</sourceusername>\n\t\t<sourcedisplayname>面试鸭</sourcedisplayname>\n\t\t<commenturl />\n\t\t<thumburl />\n\t\t<mediatagname />\n\t\t<messageaction><![CDATA[]]></messageaction>\n\t\t<messageext><![CDATA[]]></messageext>\n\t\t<emoticongift>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticongift>\n\t\t<emoticonshared>\n\t\t\t<packageflag>0</packageflag>\n\t\t\t<packageid />\n\t\t</emoticonshared>\n\t\t<designershared>\n\t\t\t<designeruin>0</designeruin>\n\t\t\t<designername>null</designername>\n\t\t\t<designerrediretcturl><![CDATA[null]]></designerrediretcturl>\n\t\t</designershared>\n\t\t<emotionpageshared>\n\t\t\t<tid>0</tid>\n\t\t\t<title>null</title>\n\t\t\t<desc>null</desc>\n\t\t\t<iconUrl><![CDATA[null]]></iconUrl>\n\t\t\t<secondUrl>null</secondUrl>\n\t\t\t<pageType>0</pageType>\n\t\t\t<setKey>null</setKey>\n\t\t</emotionpageshared>\n\t\t<webviewshared>\n\t\t\t<shareUrlOriginal />\n\t\t\t<shareUrlOpen />\n\t\t\t<jsAppId />\n\t\t\t<publisherId>wxapp_wxf64deb2dd310480fpages/index/index.html?shareCode=sri7zm</publisherId>\n\t\t\t<publisherReqId />\n\t\t</webviewshared>\n\t\t<template_id />\n\t\t<md5>166d1656b15310044706ba0ce6fec683</md5>\n\t\t<websearch>\n\t\t\t<rec_category>0</rec_category>\n\t\t\t<channelId>0</channelId>\n\t\t</websearch>\n\t\t<weappinfo>\n\t\t\t<pagepath><![CDATA[pages/index/index.html?shareCode=sri7zm]]></pagepath>\n\t\t\t<username>gh_2320846df89c@app</username>\n\t\t\t<appid>wxf64deb2dd310480f</appid>\n\t\t\t<version>66</version>\n\t\t\t<type>2</type>\n\t\t\t<weappiconurl><![CDATA[http://wx.qlogo.cn/mmhead/BO1qQiajiacVmSj2PibMkJaSnccrgXmue68yhMHwg8EL5U3tCudib8oQEmVXDKkQggC0EUzibXGOacs8/96]]></weappiconurl>\n\t\t\t<shareId><![CDATA[1_wxf64deb2dd310480f_31b3ef85c51a97ecc458be1894334026_1742224528_0]]></shareId>\n\t\t\t<appservicetype>0</appservicetype>\n\t\t\t<secflagforsinglepagemode>0</secflagforsinglepagemode>\n\t\t\t<videopageinfo>\n\t\t\t\t<thumbwidth>720</thumbwidth>\n\t\t\t\t<thumbheight>576</thumbheight>\n\t\t\t\t<fromopensdk>0</fromopensdk>\n\t\t\t</videopageinfo>\n\t\t</weappinfo>\n\t\t<statextstr />\n\t\t<musicShareItem>\n\t\t\t<musicDuration>0</musicDuration>\n\t\t</musicShareItem>\n\t\t<finderLiveProductShare>\n\t\t\t<finderLiveID><![CDATA[]]></finderLiveID>\n\t\t\t<finderUsername><![CDATA[]]></finderUsername>\n\t\t\t<finderObjectID><![CDATA[]]></finderObjectID>\n\t\t\t<finderNonceID><![CDATA[]]></finderNonceID>\n\t\t\t<liveStatus><![CDATA[]]></liveStatus>\n\t\t\t<appId><![CDATA[]]></appId>\n\t\t\t<pagePath><![CDATA[]]></pagePath>\n\t\t\t<productId><![CDATA[]]></productId>\n\t\t\t<coverUrl><![CDATA[]]></coverUrl>\n\t\t\t<productTitle><![CDATA[]]></productTitle>\n\t\t\t<marketPrice><![CDATA[0]]></marketPrice>\n\t\t\t<sellingPrice><![CDATA[0]]></sellingPrice>\n\t\t\t<platformHeadImg><![CDATA[]]></platformHeadImg>\n\t\t\t<platformName><![CDATA[]]></platformName>\n\t\t\t<shopWindowId><![CDATA[]]></shopWindowId>\n\t\t\t<flashSalePrice><![CDATA[0]]></flashSalePrice>\n\t\t\t<flashSaleEndTime><![CDATA[0]]></flashSaleEndTime>\n\t\t\t<ecSource><![CDATA[]]></ecSource>\n\t\t\t<sellingPriceWording><![CDATA[]]></sellingPriceWording>\n\t\t\t<platformIconURL><![CDATA[]]></platformIconURL>\n\t\t\t<firstProductTagURL><![CDATA[]]></firstProductTagURL>\n\t\t\t<firstProductTagAspectRatioString><![CDATA[0.0]]></firstProductTagAspectRatioString>\n\t\t\t<secondProductTagURL><![CDATA[]]></secondProductTagURL>\n\t\t\t<secondProductTagAspectRatioString><![CDATA[0.0]]></secondProductTagAspectRatioString>\n\t\t\t<firstGuaranteeWording><![CDATA[]]></firstGuaranteeWording>\n\t\t\t<secondGuaranteeWording><![CDATA[]]></secondGuaranteeWording>\n\t\t\t<thirdGuaranteeWording><![CDATA[]]></thirdGuaranteeWording>\n\t\t\t<isPriceBeginShow>false</isPriceBeginShow>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t\t<promoterKey><![CDATA[]]></promoterKey>\n\t\t\t<discountWording><![CDATA[]]></discountWording>\n\t\t\t<priceSuffixDescription><![CDATA[]]></priceSuffixDescription>\n\t\t\t<productCardKey><![CDATA[]]></productCardKey>\n\t\t\t<isWxShop><![CDATA[]]></isWxShop>\n\t\t\t<brandIconUrl><![CDATA[]]></brandIconUrl>\n\t\t\t<showBoxItemStringList />\n\t\t</finderLiveProductShare>\n\t\t<finderOrder>\n\t\t\t<appID><![CDATA[]]></appID>\n\t\t\t<orderID><![CDATA[]]></orderID>\n\t\t\t<path><![CDATA[]]></path>\n\t\t\t<priceWording><![CDATA[]]></priceWording>\n\t\t\t<stateWording><![CDATA[]]></stateWording>\n\t\t\t<productImageURL><![CDATA[]]></productImageURL>\n\t\t\t<products><![CDATA[]]></products>\n\t\t\t<productsCount><![CDATA[0]]></productsCount>\n\t\t\t<orderType><![CDATA[0]]></orderType>\n\t\t\t<newPriceWording><![CDATA[]]></newPriceWording>\n\t\t\t<newStateWording><![CDATA[]]></newStateWording>\n\t\t\t<useNewWording><![CDATA[0]]></useNewWording>\n\t\t</finderOrder>\n\t\t<finderShopWindowShare>\n\t\t\t<finderUsername><![CDATA[]]></finderUsername>\n\t\t\t<avatar><![CDATA[]]></avatar>\n\t\t\t<nickname><![CDATA[]]></nickname>\n\t\t\t<commodityInStockCount><![CDATA[]]></commodityInStockCount>\n\t\t\t<appId><![CDATA[]]></appId>\n\t\t\t<path><![CDATA[]]></path>\n\t\t\t<appUsername><![CDATA[]]></appUsername>\n\t\t\t<query><![CDATA[]]></query>\n\t\t\t<liteAppId><![CDATA[]]></liteAppId>\n\t\t\t<liteAppPath><![CDATA[]]></liteAppPath>\n\t\t\t<liteAppQuery><![CDATA[]]></liteAppQuery>\n\t\t\t<platformTagURL><![CDATA[]]></platformTagURL>\n\t\t\t<saleWording><![CDATA[]]></saleWording>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t\t<profileTypeWording><![CDATA[]]></profileTypeWording>\n\t\t\t<saleWordingExtra><![CDATA[]]></saleWordingExtra>\n\t\t\t<isWxShop><![CDATA[]]></isWxShop>\n\t\t\t<platformIconUrl><![CDATA[]]></platformIconUrl>\n\t\t\t<brandIconUrl><![CDATA[]]></brandIconUrl>\n\t\t\t<description><![CDATA[]]></description>\n\t\t\t<backgroundUrl><![CDATA[]]></backgroundUrl>\n\t\t\t<darkModePlatformIconUrl><![CDATA[]]></darkModePlatformIconUrl>\n\t\t\t<reputationInfo>\n\t\t\t\t<hasReputationInfo>0</hasReputationInfo>\n\t\t\t\t<reputationScore>0</reputationScore>\n\t\t\t\t<reputationWording />\n\t\t\t\t<reputationTextColor />\n\t\t\t\t<reputationLevelWording />\n\t\t\t\t<reputationBackgroundColor />\n\t\t\t</reputationInfo>\n\t\t\t<productImageURLList />\n\t\t</finderShopWindowShare>\n\t\t<findernamecard>\n\t\t\t<username />\n\t\t\t<avatar><![CDATA[]]></avatar>\n\t\t\t<nickname />\n\t\t\t<auth_job />\n\t\t\t<auth_icon>0</auth_icon>\n\t\t\t<auth_icon_url />\n\t\t\t<ecSource><![CDATA[]]></ecSource>\n\t\t\t<lastGMsgID><![CDATA[]]></lastGMsgID>\n\t\t</findernamecard>\n\t\t<finderGuarantee>\n\t\t\t<scene><![CDATA[0]]></scene>\n\t\t</finderGuarantee>\n\t\t<directshare>0</directshare>\n\t\t<gamecenter>\n\t\t\t<namecard>\n\t\t\t\t<iconUrl />\n\t\t\t\t<name />\n\t\t\t\t<desc />\n\t\t\t\t<tail />\n\t\t\t\t<jumpUrl />\n\t\t\t</namecard>\n\t\t</gamecenter>\n\t\t<patMsg>\n\t\t\t<chatUser />\n\t\t\t<records>\n\t\t\t\t<recordNum>0</recordNum>\n\t\t\t</records>\n\t\t</patMsg>\n\t\t<secretmsg>\n\t\t\t<issecretmsg>0</issecretmsg>\n\t\t</secretmsg>\n\t\t<referfromscene>0</referfromscene>\n\t\t<gameshare>\n\t\t\t<liteappext>\n\t\t\t\t<liteappbizdata />\n\t\t\t\t<priority>0</priority>\n\t\t\t</liteappext>\n\t\t\t<appbrandext>\n\t\t\t\t<litegameinfo />\n\t\t\t\t<priority>-1</priority>\n\t\t\t</appbrandext>\n\t\t\t<gameshareid />\n\t\t\t<sharedata />\n\t\t\t<isvideo>0</isvideo>\n\t\t\t<duration>-1</duration>\n\t\t\t<isexposed>0</isexposed>\n\t\t\t<readtext />\n\t\t</gameshare>\n\t\t<mpsharetrace>\n\t\t\t<hasfinderelement>0</hasfinderelement>\n\t\t\t<lastgmsgid />\n\t\t</mpsharetrace>\n\t\t<wxgamecard>\n\t\t\t<framesetname />\n\t\t\t<mbcarddata />\n\t\t\t<minpkgversion />\n\t\t\t<clientextinfo />\n\t\t\t<mbcardheight>0</mbcardheight>\n\t\t\t<isoldversion>0</isoldversion>\n\t\t</wxgamecard>\n\t\t<liteapp>\n\t\t\t<id>null</id>\n\t\t\t<path />\n\t\t\t<query />\n\t\t\t<istransparent>0</istransparent>\n\t\t\t<hideicon>0</hideicon>\n\t\t</liteapp>\n\t\t<finderCollection>\n\t\t\t<feedCount>0</feedCount>\n\t\t\t<collectionTopicType>0</collectionTopicType>\n\t\t\t<paidCollectionType>0</paidCollectionType>\n\t\t\t<price>0</price>\n\t\t\t<title />\n\t\t\t<collectionId>0</collectionId>\n\t\t\t<thumbUrl />\n\t\t\t<collectionDesc />\n\t\t\t<authorUsername />\n\t\t\t<nickname />\n\t\t\t<avatarURL />\n\t\t\t<authIconURL />\n\t\t\t<authIconType>0</authIconType>\n\t\t</finderCollection>\n\t</appmsg>\n\t<fromusername>wxid_xd12odto989122</fromusername>\n\t<scene>0</scene>\n\t<appinfo>\n\t\t<version>1</version>\n\t\t<appname></appname>\n\t</appinfo>\n\t<commenturl></commenturl>\n</msg>\n
                    #             ''')
                    platform_message.MiniPrograms(mini_app_id='wxf64deb2dd310480f', user_name='gh_2320846df89c@app'),
                    platform_message.Link(link_title='一起吃坑德基啊，哈哈', link_url='https://napcat.apifox.cn/',
                                          link_thumb_url='https://pics3.baidu.com/feed/0824ab18972bd407a9403f336648d15c0db30943.jpeg@f_auto?token=d26f7f142871542956aaa13799ba1946',
                                          link_desc='好吃的坑德基')
                    # platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')

                ])

            )



            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()
        elif msg == '菜单':
            await ctx.reply(platform_message.MessageChain([platform_message.Plain(f'看妹妹\n天气\n早报\n吸猫\n')]))
        elif msg == '看妹妹':
            ret_msg = await self.bot_inq.fetch_woman_image()
            await ctx.reply(platform_message.MessageChain([platform_message.Image(url=ret_msg)]))
        elif msg == '早报':
            ret_msg = await self.bot_inq.get_anime_img()
            await ctx.reply(platform_message.MessageChain([platform_message.Image(url=ret_msg)]))
        elif msg == '天气':
            ret_msg = await self.bot_inq.get_weater(data[0])
            await ctx.reply(platform_message.MessageChain([platform_message.Plain(ret_msg)]))

        elif msg == '吸猫':
            ret_msg = await self.bot_inq.get_cat_img()
            await ctx.reply(platform_message.MessageChain([platform_message.Image(url=ret_msg)]))
        elif msg == '定时':
            task_name = data[0]
            hour, minute = map(int, data[-1].split("-"))
            now_time = datetime.now()
            adapter = 'gewechat'
            task_time = now_time.replace(hour=hour, minute=minute).strftime("%Y-%m-%d %H-%M-%S")
            target_type = ctx.event.launcher_type
            target_id = ctx.event.launcher_id
            # await self.asyautotask.start()

            await self.asyautotask.add_task(ctx, task_name, task_time, target_type, target_id, adapter)
        elif msg == '查询任务':
            # await self.asyautotask.start()
            await self.asyautotask.get_pending_tasks(ctx)
        model_info = await self.ap.model_mgr.get_model_by_name(self.ap.provider_cfg.data['model'])
        print(model_info)

        pd_proempt = f'判断用户输入的问题是否是要求你做一件具体的事情，只用返回‘是’或‘否’问题:{all_msg}'
        message = [llm_entities.Message(role="user", content=pd_proempt)]
        pd_resp = await model_info.requester.call(None, model=model_info, messages=message)
        print(pd_resp.content)
        if pd_resp.content == '是':


            now_time = datetime.now().strftime("%Y-%m-%d %H-%M-%S")

            prompt = f'请将用户输入的问题：{all_msg}。提取问题中事件，时间，要求，人物，时间为24小时制，现在时间为{now_time}，只返回json,不用返回其他内容'
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
            message = [llm_entities.Message(role="user", content=all_msg)]
            pd_resp = await model_info.requester.call(None, model=model_info, messages=message)
            await ctx.reply(MessageChain([Plain(str(pd_resp.content))]))






    # def _convert_message(self, message, sender_id):
    #     parts = []
    #     last_end = 0
    #     Inimage = False
    #     image_pattern = re.compile(r'!\[.*?\]\((https?://\S+)\)')  # 定义图像链接的正则表达式
    #     # 检查消息中是否包含at指令
    #     # if "atper_on" in message:
    #     #     parts.append(platform_message.At(target=sender_id))  # 在消息开头加上At(sender_id)
    #     #     message = message.replace("atper_on", "")  # 从消息中移除"send_on"
    #     for match in image_pattern.finditer(message):  # 查找所有匹配的图像链接
    #         Inimage = True
    #         start, end = match.span()  # 获取匹配的起止位置
    #         if start > last_end:  # 如果有文本在图像之前
    #             parts.append(platform_message.Plain(message[last_end:start]))  # 添加纯文本部分
    #         image_url = match.group(1)  # 提取图像 URL
    #         parts.append(platform_message.Image(url=image_url))  # 添加图像消息
    #         last_end = end  # 更新最后结束位置
    #     if last_end + 1 < len(message) and Inimage:  # 如果还有剩余文本
    #         print(f'1in={last_end + 1 < len(message)}')
    #         parts.append(platform_message.Plain(message[last_end:]))  # 添加剩余的纯文本
    #     Inimage = False
    #     return parts if parts else parts.append(platform_message.Plain(message))  # 返回构建好的消息列表，如果没有部分则返回纯文本消息

    # 插件卸载时触发
    def __del__(self):
        pass
