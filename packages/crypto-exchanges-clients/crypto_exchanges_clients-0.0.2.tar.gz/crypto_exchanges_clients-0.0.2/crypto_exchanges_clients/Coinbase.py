import asyncio
from typing import Optional

from .BaseExchange import BaseExchange
from .utils import get_current_ts


class Coinbase(BaseExchange):

    exchange = 'coinbase'

    def __init__(self) -> None:
        super().__init__('https://api.exchange.coinbase.com')

    def _convert_token_to_symbol(self, token: str) -> str:
        return f'{token}-USD'

    @staticmethod
    def _calc_quote_asset_volume(volume: float, high_price: float, low_price: float):
        return volume * (high_price + low_price) / 2

    async def get_token_listing_timestamp(self, token: str) -> Optional[int]:
        limit = 300
        interval = 86400000
        symbol = self._convert_token_to_symbol(token)
        end_time = get_current_ts()
        listing_time = None
        for _ in range(12):
            params = {
                'granularity': 86400,
                'start': end_time - limit * interval,
                'end': end_time,
            }
            resp = await self._request('GET', f'/products/{symbol}/candles', params)
            if isinstance(resp, dict):
                return None
            data = resp[::-1]
            if not data:
                return listing_time
            listing_time = data[0][0] * 1000
            end_time = listing_time - interval
            await asyncio.sleep(0.1)
