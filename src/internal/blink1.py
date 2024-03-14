import aiohttp
from aiohttp import BasicAuth

from config import settings


async def blink1_red():
    async with aiohttp.ClientSession() as session:
        auth = BasicAuth(settings.NGROK_USER.get_secret_value(), settings.NGROK_PASS.get_secret_value())
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + 'blink', auth=auth)


async def blink1_yellow():
    async with aiohttp.ClientSession() as session:
        auth = BasicAuth(settings.NGROK_USER.get_secret_value(), settings.NGROK_PASS.get_secret_value())
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + 'blink/yellow', auth=auth)


async def blink1_magenta():
    async with aiohttp.ClientSession() as session:
        auth = BasicAuth(settings.NGROK_USER.get_secret_value(), settings.NGROK_PASS.get_secret_value())
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + 'blink/magenta', auth=auth)


async def blink1_green():
    async with aiohttp.ClientSession() as session:
        auth = BasicAuth(settings.NGROK_USER.get_secret_value(), settings.NGROK_PASS.get_secret_value())
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + 'blink/magenta', auth=auth)
