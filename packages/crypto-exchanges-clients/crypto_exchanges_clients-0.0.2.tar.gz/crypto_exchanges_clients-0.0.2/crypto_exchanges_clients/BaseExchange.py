from typing import Optional
import aiohttp


class BaseExchange:

    exchange = ''

    def __init__(self, url):
        self._url = url

    def _get_url(self, url_postfix: str) -> str:
        return f'{self._url}{url_postfix}'

    def _convert_token_to_symbol(self, token: str) -> str:
        return f'{token}USDT'

    async def _request(self, method: str, url_postfix: str, params: dict = None) -> dict:
        if not params:
            params = {}
        async with aiohttp.ClientSession() as session:
            async with session.request(method.upper(), self._get_url(url_postfix), params=params) as resp:
                return await resp.json()

    async def get_token_listing_timestamp(self, token: str) -> Optional[int]:
        pass
