import datetime


async def convert_time(timestamp):
    timestamp_seconds = timestamp / 1000
    dt = datetime.datetime.fromtimestamp(timestamp_seconds, tz=datetime.timezone.utc)
    return (dt.strftime("%Y-%m-%d %H:%M:%S %Z"))


