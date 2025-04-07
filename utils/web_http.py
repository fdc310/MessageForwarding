import httpx
import requests
import asyncio


async def asy_http(url: str, data: dict = None):

    try:

        async with httpx.AsyncClient() as client:
            if data:
                resp = await client.get(url, params=data)
            else:
                resp = await client.get(url)

            if resp.status_code == 200:
                resp_data = resp.json()
                return resp_data
            else:
                return {"msg": "error", "data": "获取失败"}
    except httpx.RequestError as e:
        return (f'一会儿再来吧')
    except Exception as e:
        print(f'错误{e}')


def web_http(api: str, data: dict = None):
    try:
        if data:
            resp_data = requests.get(api, params=data)
        else:
            resp_data = requests.get(api)
        if resp_data.status_code == 200:
            return resp_data
        else:
            return None
    except requests.RequestException as e:
        return f'一会再来吧'
    except Exception as e:
        return f'错误{e}'