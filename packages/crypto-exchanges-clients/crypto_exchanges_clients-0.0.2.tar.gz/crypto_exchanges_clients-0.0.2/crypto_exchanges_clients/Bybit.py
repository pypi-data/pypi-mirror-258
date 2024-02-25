from typing import Optional

from .BaseExchange import BaseExchange
from .utils import get_current_ts, convert_ts_to_start_of_day


class Bybit(BaseExchange):

    exchange = 'bybit'

    klines_limit = 1000

    def __init__(self) -> None:
        super().__init__('https://api.bybit.com')

    async def get_token_listing_timestamp(self, token: str) -> Optional[int]:
        one_day_interval = 86400000
        end_date = convert_ts_to_start_of_day(get_current_ts())
        start_date = end_date - self.klines_limit * one_day_interval
        params = {
            'category': 'spot',
            'interval': 'D',
            'start': start_date,
            'end': end_date,
            'limit': self.klines_limit,
            'symbol': self._convert_token_to_symbol(token)
        }
        resp = await self._request('GET', '/v5/market/kline', params)
        data = resp.get('result', {}).get('list', [])[::-1]
        return int(data[0][0])
