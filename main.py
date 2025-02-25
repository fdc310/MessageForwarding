from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import pkg.platform.types as platform_types

# 注册插件
@register(name="MessageForwarding", description="Message forwarding", version="0.1", author="阿东不懂事")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        pass

    # 异步初始化
    async def initialize(self):
        pass

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
        # self.ap.logger.debug(f"{ctx.event.sender_id}")
        # self.ap.logger.debug(f"{ctx.prevent_default()}")
        # print(type(msg))
        # msg = str(msg)
        print(ctx.host.get_platform_adapters())
        print(ctx.event.launcher_type)
        la_type = ctx.event.launcher_type


        await ctx.host.send_active_message(adapter=ctx.host.get_platform_adapters()[1],
                                target_id='wxid_xd12odto989122',
                               target_type=ctx.event.launcher_type,
                               message=platform_types.MessageChain([
                                             platform_types.Plain(f"你有新的消息来自{ctx.event.sender_id},他说{msg}")]
                                         )
                               )
        await ctx.host.send_active_message(adapter=ctx.host.get_platform_adapters()[0],
                                         target_id='898246617',
                                         target_type='person',
                                         message=platform_types.MessageChain([
                                             platform_types.Plain(f"你有新的消息来自{ctx.event.sender_id},他说{msg}")]
                                         )
                                         )
        ctx.prevent_default()

    # 当收到群消息时触发
    @handler(GroupNormalMessageReceived)
    async def group_normal_message_received(self, ctx: EventContext):
        msg = ctx.event.text_message  # 这里的 event 即为 GroupNormalMessageReceived 的对象
        if msg == "hello":  # 如果消息为hello

            # 输出调试信息
            self.ap.logger.debug("hello, {}".format(ctx.event.sender_id))

            # 回复消息 "hello, everyone!"
            ctx.add_return("reply", ["hello, everyone!"])

            # 阻止该事件默认行为（向接口获取回复）
            ctx.prevent_default()

    # 插件卸载时触发
    def __del__(self):
        pass
