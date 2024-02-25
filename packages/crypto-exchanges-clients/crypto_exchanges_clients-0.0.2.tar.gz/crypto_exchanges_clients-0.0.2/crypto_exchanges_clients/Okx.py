from typing import Optional

from .BaseExchange import BaseExchange


class Okx(BaseExchange):

    inst_type = 'SPOT'
    exchange = 'okx'
    klines_limit = 100

    def __init__(self) -> None:
        super().__init__('https://www.okx.com')

    def _convert_token_to_symbol(self, token: str) -> str:
        return f'{token.upper()}-USDT'

    async def get_token_listing_timestamp(self, token: str) -> Optional[int]:
        params = {
            'instType': self.inst_type,
            'instId': self._convert_token_to_symbol(token)
        }
        resp = await self._request('GET', '/api/v5/public/instruments', params)
        data = resp.get('data', [])
        if data:
            return int(data[0]['listTime'])
