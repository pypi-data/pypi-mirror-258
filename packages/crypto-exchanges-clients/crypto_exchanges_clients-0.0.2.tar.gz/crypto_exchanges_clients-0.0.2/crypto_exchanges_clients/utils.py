from datetime import datetime, timezone, timedelta
from typing import Union
from time import time


def convert_open_ts_to_close_ts(ts: int, interval: int) -> int:
    return int(ts) + interval - 1


def convert_ts_to_str_date(ts: Union[str, int]) -> str:
    date = datetime.fromtimestamp(int(ts)/1000, tz=timezone.utc)
    return date.strftime('%Y-%m-%d')


def convert_ts_to_start_of_day(ts: Union[str, int], add_days=0) -> int:
    dt = datetime.fromtimestamp(int(ts)/1000, tz=timezone.utc)
    dt = datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=timezone.utc) + timedelta(days=add_days,)
    return int(dt.timestamp() * 1000)


def get_current_ts() -> int:
    return int(time() * 1000)


def convert_ts_to_datetime(ts: Union[str, int]) -> datetime:
    return datetime.fromtimestamp(int(ts)/1000, tz=timezone.utc)


def convert_ts_to_datetime_start_of_day(ts: Union[str, int]) -> datetime:
    dt = datetime.fromtimestamp(int(ts) / 1000, tz=timezone.utc)
    return datetime(year=dt.year, month=dt.month, day=dt.day, tzinfo=timezone.utc)


def convert_datetime_to_ts(dt: datetime) -> int:
    return int(dt.timestamp()*1000)


def convert_str_date_to_ts(date: str) -> int:
    return convert_datetime_to_ts(datetime.strptime(date, '%Y-%m-%d').replace(tzinfo=timezone.utc))
