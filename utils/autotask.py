from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext

import time
from datetime import datetime
import random
import os
import asyncio
import json
import importlib
from concurrent.futures import ThreadPoolExecutor
from pkg.platform.types import *



class AutoTask(BasePlugin):

    def __init__(self, host: APIHost):
        self.host = host
        self.tasks = []
        self.task_file = os.path.join(os.path.dirname(__file__), 'tasks.json')  # 统一文件名


    async def check_timer(self):
        # 定时检器
        while True:
            try:
                await asyncio.sleep(60)
                await self.update_task()
            except Exception as e:
                print(f"{e}")


    def seve_tasks(self,):
        # 保存任务
        try:
            tasks_json = []
            for task in self.tasks:
                task_json = {
                    'time': str(task.get('time', '')),
                    'script': task.get('script', None),
                    'target_id': task.get('target_id', 0),
                    "target_type": task.get('target_type', 'person'),
                    'adapter': task.get('adapter'),
                    'name': task.get('name', ''),
                    'func': task.get('func', 'None'),
                    'create_time': task.get('create_time', None),
                    'last_time': task.get('last_time', None),
                    "is_at": task.get('is_at', None)

                }
                tasks_json.append(task_json)
            with open(self.task_file, 'w') as f:
                json.dump(tasks_json, f)

        except Exception as e:
            print(f'{e}')


    async def load_tasks(self):
        # 检查任务
        try:
            if not os.path.exists(self.task_file):
                self.tasks = []
                return

            with open(self.task_file, 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                if not isinstance(tasks_data, list):
                    self.tasks = []
                    return
                self.tasks = []
                for task_data in tasks_data:
                    task = {
                         'time': str(task.get('time', '')),
                    'script': task.get('script', None),
                    'target_id': task.get('target_id', 0),
                    "target_type": task.get('target_type', 'person'),
                    'adapter': task.get('adapter'),
                    'name': task.get('name', ''),
                    'func': task.get('func', 'None'),
                    'create_time': task.get('create_time', None),
                    'last_time': datetime.fromisoformat(
                            task_data.get("last_time", "")) if task_data.get("last_time") else None,
                    "is_at": task.get('is_at', None)

                    }
                    self.tasks.append(task)
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            self.tasks = []
        except Exception as e:
            print(f"加载定时任务失败: {str(e)}")
            self.tasks = []


    async def add_task(self, ctx: EventContext, task_name: str, task_time: str, target_type: str, target_id: str, adapter: str,
                       func: str = None, is_at: str = None):

        # 添加任务
        for task in self.tasks:
            if task['name'] == task_name and task['time'] == task_time:
                await ctx.reply(MessageChain([Plain(f'定时任务{task_name}已存在！')]))

        new_task = {
            'time': task_time,
            'script': task_name,
            'target_id': target_id,
            "target_type": target_type,
            'adapter': adapter,
            'name': task_name,
            'func': func,
            'create_time': self.get_timer_str(),
            'last_time': None,
            "is_at": is_at
        }

        self.tasks.append(new_task)
        self.seve_tasks()
        await ctx.reply(MessageChain([Plain(f'定时任务{task_name}添加成功！')]))


    async def del_task(self, ctx: EventContext, task_name):
        # 删除任务

        for task in self.tasks:
            if task["name"] == task_name:
                self.tasks.remove(task)
                self.seve_tasks()
                await ctx.reply(MessageChain([Plain(f"定时任务 {task_name} 已删除!")]))
                # return

        await ctx.reply(MessageChain([Plain(f"定时任务 {task_name} 不存在!")]))
        pass


    async def update_task(self):
        # new_timer = self.get_timer_str()
        # new_timer = datetime.strftime(new_timer, "%Y-%m-%d %H-%M-%S")
        # task_time = ''
        for task in self.tasks:
            task_time = task['time']
            try:
                if self.get_timer_str() == datetime.strptime(task_time, "%Y-%m-%d %H-%M-%S"):
                    last_triggered = task.get('last_timer')
                    if last_triggered:
                        task['last_tmie'] = self.get_timer_str()
                        self.seve_tasks()
                        await self.execute_task(task)
            except Exception as e:
                print(f'{e}')
        # 更新任务


    async def execute_task(self, task):
        '''
        task: 任务
        '''
        # 执行任务
        script_name = task['script']
        target_id = task['id']
        target_type = task['type']
        task_name = task['name']
        adapter = task['adapter']
        func_name = task['func']
        cls = 'plugins.MessageForwarding.utils.inquire.BotInquire'
        try:
            # 动态导入外部模块
            module = importlib.import_module(cls)
            # 获取函数对象
            func = getattr(module, func_name, None)
            if func_name is None:
                await self.host.send_active_message(adapter=adapter,
                                                    target_type=target_type,
                                                    target_id=target_id,
                                                    message=MessageChain([
                                                        Plain(script_name)
                                                    ]))
            else:

                # 检查是否为异步函数
                if asyncio.iscoroutinefunction(func):
                    msg = await func()

                else:
                    loop = asyncio.get_running_loop()
                    with ThreadPoolExecutor() as pool:
                        msg = await loop.run_in_executor(pool, func)
                await self.host.send_active_message(adapter=adapter,
                                        target_type=target_type,
                                        target_id=target_id,
                                        message=MessageChain([
                                            Plain(msg)
                                        ]))
            # return msg

        except Exception as e:
            return (f'{e}')

        pass

    async def radom_time_task(self, start_hour: int = 0, end_hour: int = 24):
        # 获取随机间断时间
        try:
            radom_hour = random.randint(8, 10)
            radom_min = random.randint(1, 60)
            return {"hour": radom_hour, 'min': radom_min}
        except Exception as e:
            return {}


    def get_timer_str(self):
        # 获取当前时间
        return datetime.now().strftime("%Y-%m-%d %H-%M-%S")