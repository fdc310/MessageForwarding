from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext

import asyncio
from datetime import datetime, timedelta
import aiofiles
import json
import os
import importlib
from pkg.platform.types import *


class AsyAutoTask(BasePlugin):
    def __init__(self, host: APIHost):
        self.host = host
        self.tasks = []
        self.tasks_file = os.path.join(os.path.dirname(__file__),'tasks.json')
        self._runing = False
        self._task_handles = {}  # 存储运行中的任务句柄

        # 初始化时加载任务
        asyncio.create_task(self.load_tasks())


    async def start(self):
        '''启动调度任务'''
        if not self._runing:
            self._runing = True
            await self.schedule_all_task()


    async def stop(self):
        self._runing = False
        for handle in self._task_handles.values():
            handle.cancel()
        self._task_handles.clear()  # 清理所有句柄


    async def schedule_task(self, task: dict):
        '''调度单个任务'''
        try:
            task_name = task['name']

            # 取消已有任务
            if task_name in self._task_handles:
                self._task_handles[task_name].cancel()

            if ':' in task['time']:
                hour, minute, sec = map(int, task['time'].split(':'))
                await self._schedule_daily_task(task, hour=hour,minute=minute,sec=sec)
            else:
                await self._schedule_one_time_task(task)
        except Exception as e:
            print(f'调度单个任务出错{e}')


    async def schedule_all_task(self):
        """
        调度全部任务
        """
        try:

            for task in self.tasks:
                await self.schedule_task(task)
        except Exception as e:
            print(f'd调度全部任务出错{e}')


    async def _schedule_daily_task(self, task: dict, hour: int, minute: int, sec: int):
        '''
        安排每日重复任务
        '''
        async def daily_wrapper():
            while self._runing:
                now_time = datetime.now()
                task_time = now_time.replace(hour=hour, minute=minute, second=sec, microsecond=0)

                if now_time > task_time:  # 判断是否过了当前时间
                    task_time += timedelta(days=1)  # 过去了就进行加一天

                wait_second = (task_time - now_time).total_seconds()  # 计算任务距离当前时间（秒）
                await asyncio.sleep(wait_second)

                # 二次检测
                if self._runing:
                    await self.execute_task(task)
                    task['last_time'] = datetime.now().isoformat()
                    await self.save_tasks()

        self._task_handles[task['name']] = asyncio.create_task(daily_wrapper())  # 将任务添加

    async def _schedule_one_time_task(self, task):
        '''安排单次任务'''
        async def one_time_wrapper():
            print(123)
            try:
                task_time = datetime.strptime(task['time'], "%Y-%m-%d %H-%M-%S")
                now_time = datetime.now()

                if task_time <= now_time:
                    print(f'任务时间小于现在时间')
                    return
                wait_second = (task_time - now_time).total_seconds()
                print(f'任务还有{wait_second}')

                await asyncio.sleep(wait_second)
                if self._runing:
                    await self.execute_task(task)
                    self.tasks.remove(task)
                    task['last_time'] = datetime.now().isoformat()
                    await self.save_tasks()
            except Exception as e:
                print(f'任务错误{e}')

        try:

            self._task_handles[task['name']] = asyncio.get_running_loop().create_task(one_time_wrapper())  # 将任务添加
        except Exception as e:
            print(f'单次{e}')

    async def execute_task(self, task):

        # 更安全的adapter获取方式
        adapter = next(
            (a for a in self.host.get_platform_adapters()
             if a.name == task['adapter']),
            None
        )
        if not adapter:
            raise ValueError(f"找不到适配器: {task['adapter']}")
        func_name = task['func']
        cls = 'plugins.MessageForwarding.utils.inquire.BotInquire'
        try:
            if task['func']:
                # module_path, func_name = task['func'].rsplit('.', 1)
                module = importlib.import_module(cls)
                func = getattr(module, func_name)

                result = await func() if asyncio.iscoroutinefunction(func) else func()

                if result:
                    await self.host.send_active_message(
                        adapter= adapter,
                        target_type=task['target_type'],
                        target_id=task['target_id'],
                        message=MessageChain([Plain(str(result))])
                    )
            else:
                await self.host.send_active_message(
                    adapter=adapter,
                    target_type=task['target_type'],
                    target_id=task['target_id'],
                    message=MessageChain([Plain(task['script'])])
                )
        except Exception as e:
            print(f'执行任务触发错误{e}')

    async def add_task(self, ctx: EventContext, task_name, task_time, target_type: str, target_id: str, adapter: str,
                       func: str = None, is_at: str = None):
        """

        """
        try:
            if any([i['name'] == task_name for i in self.tasks]):  # 用于判断给定的可迭代对象（如列表、元组或字典）中是否至少有一个元素为 True。
                await ctx.reply(MessageChain([Plain(f'任务{task_name}已存在')]))
                return
            new_task = {
            'time': task_time,
            'script': task_name,
            'target_id': target_id,
            "target_type": target_type,
            'adapter': adapter,
            'name': task_name,
            'func': func,
            'create_time': datetime.now().isoformat(),
            'last_time': None,
            "is_at": is_at
            }
            self.tasks.append(new_task)
            await self.save_tasks()
            await self.schedule_task(new_task)
            await ctx.reply(MessageChain([Plain(f'任务{task_name}添加成功')]))
        except Exception as e:
            print(f'添加任务出错{e}')


    async def del_task(self,ctx:EventContext, task_name):
        task = next((i for i in self.tasks if i['name'] == task_name), None)
        if not task:
            await ctx.reply(MessageChain([Plain(f'任务{task_name}不存在或已执行')]))
            return
        if task_name in self._task_handles:
            self._task_handles[task_name].cancel()
            del self._task_handles[task_name]
        self.tasks = [i for i in self.tasks if i['name'] != task_name]
        await self.save_tasks()
        await ctx.reply(MessageChain([Plain(f'任务{task_name}已删除')]))


    async def save_tasks(self):
        try:
            async with aiofiles.open(self.tasks_file, 'w') as f:
                await f.write(json.dumps(
                    [t for t in self.tasks if 'schedule_job' not in t],
                    ensure_ascii=False,
                    indent=2
                ))
        except Exception as e:
            print(f'保存任务错误{e}')
        pass


    async def load_tasks(self):
        '''异步加载任务'''
        try:
            if os.path.exists(self.tasks_file):
                with open(self.tasks_file,"r") as f:
                    self.tasks = json.load(f)
                    await self.schedule_all_task()  # 载入全部任务
        except Exception as e:
            print(f'加载任务出错{e}')


    async def get_pending_tasks(self, ctx: EventContext):
        try:
            now_time = datetime.now()
            pending_tasks = []

            for task in self.tasks:
                if ':' in task['time']:
                    hour, minute, sec = map(int, task['time'].split(":"))
                    task_time = now_time.replace(hour=hour, minute=minute, second=sec, microsecond=0)
                    if task_time > now_time:
                        task_time += timedelta(days=1)
                else:
                    task_time = datetime.strptime(task['time'], "%Y-%m-%d %H-%M-%S")
                    # if now_time > task_time:
                    #     continue
                last_run = datetime.fromisoformat(task['last_time']) if task['last_time'] else None
                if not last_run:
                    # if last_run < now_time:
                    pending_tasks.append(
                        {
                            "name": task['name'],
                            'scheduled_time': task_time.isoformat(),
                            'target': f'{task["target_type"]}:{task["target_id"]}',
                            'remaining': f'{last_run}'

                        }
                    )


            if not pending_tasks:
                await ctx.reply(MessageChain([Plain(f'无待执行任务')]))
                return
            msg = ['待执行列表：']
            for idx, task in enumerate(pending_tasks, 1):
                msg.append(
                    f"{idx}.{task['name']}"
                    f"执行时间：{task['scheduled_time']}"
                    f"剩余时间：{task['remaining']}"
                    f"目标：{task['target']}"
                )
            await ctx.reply(MessageChain([Plain(str(msg))]))

        except Exception as e:
            print(f'查询任务出错{e}')

    # 对于每分钟执行的密集任务，改用这种更高效的方式
    async def high_frequency_task(self, task):
        while True:
            await asyncio.sleep(60)  # 每分钟
            await self.execute_task(task)