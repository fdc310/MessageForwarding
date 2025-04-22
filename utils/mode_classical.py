import asyncio
from typing import Dict
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext


class WillingManager:
    def __init__(self):
        self.chat_reply_willing: Dict[str, float] = {}  # 存储每个聊天流的回复意愿
        self._decay_task = None
        self._started = False
        self.response_willing_amplifier: float = 1.0  # 回复意愿放大系数
        self.response_interested_rate_amplifier: float = 1.0  # 回复兴趣度放大系数
        self.down_frequency_rate: float = 3  # 降低回复频率的群组回复意愿降低系数

    async def _decay_reply_willing(self):
        """定期衰减回复意愿"""
        while True:
            await asyncio.sleep(1)
            for chat_id in self.chat_reply_willing:
                self.chat_reply_willing[chat_id] = max(0, self.chat_reply_willing[chat_id] * 0.9)

    def get_willing(self, ctx: EventContext) -> float:
        """获取指定聊天流的回复意愿"""
        # 指定聊天用户或者群聊的回复意愿
        if ctx:
            return self.chat_reply_willing.get(ctx.event.sender_id, 0)
        return 0

    def set_willing(self, chat_id: str, willing: float):
        """设置指定聊天流的回复意愿"""
        self.chat_reply_willing[chat_id] = willing

    async def change_reply_willing_received(
        self,
        ctx: EventContext,
        is_mentioned_bot: bool = False,
        config=None,
        is_emoji: bool = False,
        interested_rate: float = 0,
        sender_id: str = None,
    ) -> float:
        """改变指定聊天流的回复意愿并返回回复概率"""
        chat_id = ctx.event.sender_id
        current_willing = self.chat_reply_willing.get(chat_id, 0)

        interested_rate = interested_rate * self.response_interested_rate_amplifier

        if interested_rate > 0.4:
            current_willing += interested_rate - 0.3

        if is_mentioned_bot and current_willing < 1.0:
            current_willing += 1
        elif is_mentioned_bot:
            current_willing += 0.05

        # if is_emoji:
        #     current_willing *= global_config.emoji_response_penalty

        self.chat_reply_willing[chat_id] = min(current_willing, 3.0)

        reply_probability = min(max((current_willing - 0.5), 0.01) * self.response_willing_amplifier * 2, 1)

        # # 检查群组权限（如果是群聊）
        # if ctx.launcher_type == 'group' and config:
        #     if chat_id not in config.talk_allowed_groups:
        #         current_willing = 0
        #         reply_probability = 0
        #
        #     if chat_id in config.talk_frequency_down_groups:
        #         reply_probability = reply_probability / config.down_frequency_rate

        return reply_probability

    def change_reply_willing_sent(self, ctx: EventContext):
        """发送消息后降低聊天流的回复意愿"""
        if ctx:
            chat_id = ctx.event.sender_id
            current_willing = self.chat_reply_willing.get(chat_id, 0)
            self.chat_reply_willing[chat_id] = max(0, current_willing - 1.8)

    def change_reply_willing_not_sent(self, ctx: EventContext):
        """未发送消息后降低聊天流的回复意愿"""
        if ctx:
            chat_id = ctx.event.sender_id
            current_willing = self.chat_reply_willing.get(chat_id, 0)
            self.chat_reply_willing[chat_id] = max(0, current_willing - 0)

    def change_reply_willing_after_sent(self, ctx: EventContext):
        """发送消息后提高聊天流的回复意愿"""
        if ctx:
            chat_id = ctx.event.sender_id
            current_willing = self.chat_reply_willing.get(chat_id, 0)
            if current_willing < 1:
                self.chat_reply_willing[chat_id] = min(1, current_willing + 0.4)

    async def ensure_started(self):
        """确保衰减任务已启动"""
        if not self._started:
            if self._decay_task is None:
                self._decay_task = asyncio.create_task(self._decay_reply_willing())
            self._started = True


# 创建全局实例
willing_manager = WillingManager()
