from typing import Optional

from .BaseExchange import BaseExchange


class Binance(BaseExchange):

    exchange = 'binance'

    def __init__(self) -> None:
        super().__init__('https://api.binance.com')

    async def get_token_listing_timestamp(self, token: str) -> Optional[int]:
        params = {
            'interval': '1m',
            'startTime': 0,
            'limit': 1,
            'symbol': self._convert_token_to_symbol(token)
        }
        data = await self._request('GET', '/api/v3/klines', params)
        if isinstance(data, dict) and data.get('code', 0) != 0:
            return None
        if data:
            return int(data[0][0])
