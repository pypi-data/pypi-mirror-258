import asyncio
from typing import Optional

from .BaseExchange import BaseExchange
from .utils import get_current_ts


class Bitget(BaseExchange):

    exchange = 'bitget'

    klines_limit = 200

    def __init__(self) -> None:
        super().__init__('https://api.bitget.com')

    def _convert_token_to_symbol(self, token: str) -> str:
        return f'{token}USDT_SPBL'

    async def get_token_listing_timestamp(self, token: str) -> Optional[int]:

        end_time = get_current_ts()
        listing_time = None
        for _ in range(12):
            params = {
                'period': '1day',
                'endTime': end_time,
                'limit': self.klines_limit,
                'symbol': self._convert_token_to_symbol(token)
            }
            resp = await self._request('GET', '/api/spot/v1/market/history-candles', params)
            data = resp['data']
            if not data:
                return await self._get_precise_listing_time(token, listing_time)
            listing_time = int(data[0]['ts'])
            end_time = listing_time
            await asyncio.sleep(0.1)

    async def _get_precise_listing_time(self, token: str, listing_time: int) -> Optional[int]:
        if not listing_time:
            return None
        interval = 86400000
        params = {
            'period': '1h',
            'endTime': listing_time + interval,
            'limit': self.klines_limit,
            'symbol': self._convert_token_to_symbol(token)
        }
        resp = await self._request('GET', '/api/spot/v1/market/history-candles', params)
        data = resp['data']
        if not data:
            return listing_time
        return int(data[0]['ts'])
