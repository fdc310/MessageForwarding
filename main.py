# import traceback

from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import asyncio
import pkg.platform.types as platform_types


# 注册插件
@register(name="MessageForwarding", description="Message forwarding", version="0.1", author="阿东不懂事")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):

        print(self.host.get_platform_adapters())

        async def send_message():
            print("send message start waiting")
            await asyncio.sleep(90)

            try:
                await self.host.send_active_message(
                    adapter=self.host.get_platform_adapters()[0],
                    target_type="group",
                    target_id="48371594138@chatroom",
                    message=platform_types.MessageChain([
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
            message=platform_types.MessageChain([
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
        msg = [i for i in ctx.event.query.message_chain][0].text
        print(msg, type(msg))
        # msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == "hello":  # 如果消息为hello

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))
            await ctx.host.send_active_message(
                adapter=self.host.get_platform_adapters()[0],
                target_type="group",
                target_id="48371594138@chatroom",
                message=platform_types.MessageChain([
                    platform_message.At(target='wxid_xd12odto989122'),
                    platform_message.Plain(text='群聊'),
                    # platform_message.Image(url='https://c.53326.com/d/file/lan20210602/tspho3sxi0s.jpg')

                ])

            )



            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
