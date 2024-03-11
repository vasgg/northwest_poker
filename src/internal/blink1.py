import aiohttp

from src.config import settings


async def blink1_red():
    async with aiohttp.ClientSession() as session:
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + 'blink')


async def blink1_yellow():
    async with aiohttp.ClientSession() as session:
        ngrok_url = settings.NGROK_URL.get_secret_value()
        await session.get(ngrok_url + 'blink/yellow')
