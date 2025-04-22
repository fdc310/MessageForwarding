from plugins.MessageForwarding.utils.web_http import web_http, asy_http
import asyncio



class BotInquire:

    def __init__(self):
        pass


    async def get_weater(self, city: str = '重庆'):
        api_url = 'https://api.vvhan.com/api/weather'
        req_data = {'city': city}
        resp_data = await asy_http(api_url, req_data)
        if resp_data.get("success"):
            weather_data = resp_data['data']
            weather_info = (
                f"城市: {resp_data['city']}\n"
                f"日期: {weather_data['date']}\n"
                f"星期: {weather_data['week']}\n"
                f"天气: {weather_data['type']}\n"
                f"温度范围: {weather_data['low']} - {weather_data['high']}\n"
                f"风向: {weather_data['fengxiang']}\n"
                f"风力: {weather_data['fengli']}\n"
                f"空气质量: {resp_data['air']['aqi_name']} (AQI: {resp_data['air']['aqi']})\n"
                f"提示: {resp_data['tip']}"
            )
        # print(resp_data)
            return weather_info


    async def fetch_woman_image(self):
        api_url = 'https://3650000.xyz/api/?type=json&mode=3,5,7,8'
        try:
            resp_data = await asy_http(api_url)
            if resp_data.get('code') == 200:
                image_url = resp_data['url']
            else:
                return None
            return image_url
        except Exception as e:
            return (f'错误{e}')


    async def get_anime_img(self):
        api_url = 'https://api.03c3.cn/api/zb'
        resp_data = web_http(api_url)
        if resp_data.status_code == 200:
            return api_url
        else:
            print(f"获取图片失败，状态码：{resp_data.status_code}")
            return None


    async def get_cat_img(self):
        api_url = 'https://api.thecatapi.com/v1/images/search?limit=1'
        try:
            resp_data = web_http(api_url)
            if resp_data:
                url_data = resp_data.json()
                image_url = url_data[0]['url']
                return image_url
            else:
                return None
        except Exception as e:
            return e

    async def get_douyin_hotlist(self):
        api_url = 'https://api.vvhan.com/api/hotlist/douyinHot'
        try:
            resp_data = await asy_http(api_url)
            if resp_data:
                return resp_data
            else:
                return None
        except Exception as e:
            return e



if __name__ == '__main__':
    botinq = BotInquire()
    data = asyncio.run(botinq.get_douyin_hotlist())
    print(
        data
    )