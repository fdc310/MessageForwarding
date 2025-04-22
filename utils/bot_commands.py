from plugins.MessageForwarding.utils.inquire import BotInquire
from pkg.platform.types import *


class CommandHandler:
    def __init__(self):
        self.commands = {}

    def command(self, name):
        def decorator(func):
            self.commands[name] = func
            return func
        return decorator

    async def handle(self, msg, ctx, *args):
        handler = self.commands.get(msg)
        if handler:
            await handler(ctx, *args)
        else:
            await ctx.reply("未知命令")

# 全局命令处理器
handler = CommandHandler()

botinq = BotInquire()


@handler.command("天气")
async def weather_command(ctx, city: str = '重庆'):
    weather_info = await botinq.get_weater(city)
    await ctx.reply(MessageChain([Plain(weather_info)]))


@handler.command("看妹妹")
async def woman_image_command(ctx):
    image_url = await botinq.fetch_woman_image()
    if image_url:
        await ctx.reply(platform_message.MessageChain([platform_message.Image(url=image_url)]))
    else:
        await ctx.reply("获取图片失败")




@handler.command("早报")
async def anime_img_command(ctx):
    image_url = await botinq.get_anime_img()
    import requests
    from PIL import Image
    from io import BytesIO

    def get_image_size_metadata(url):
        try:
            # 只获取前1024字节通常足够读取图片头信息
            response = requests.get(url, stream=True)
            response.raw.decode_content = True
            img = Image.open(response.raw)
            return img.size
        except Exception as e:
            print(f"通过元数据获取尺寸失败: {e}")
            return None


    if image_url:
        size = get_image_size_metadata(image_url)
        if size:
            print(size)
        print(f'{image_url}/{size[0]}x{size[1]}')
        await ctx.reply(platform_message.MessageChain([platform_message.Image(url=f'{image_url}')]))
    else:
        await ctx.reply("获取早报失败")



@handler.command("吸猫")
async def cat_img_command(ctx):
    image_url = await botinq.get_cat_img()
    if image_url:
        await ctx.reply(platform_message.MessageChain([platform_message.Image(url=image_url)]))
    else:
        await ctx.reply("获取猫咪图片失败")
