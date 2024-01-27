import asyncio
import sys


class Counter:
    def __init__(self, name: str, maximum_value: int | None = None):
        self._lock = asyncio.Lock()
        self.name = name
        self.maximum_value = maximum_value
        self.current_value = 0

    async def inc(self, count=1):
        async with self._lock:
            self.current_value += count

    def is_max(self):
        if self.maximum_value is None:
            return False
        return self.current_value >= self.maximum_value

    def __str__(self):
        maximum_value = '' if self.maximum_value is None else f'/{self.maximum_value}'
        return f'{self.name}: [{self.current_value}{maximum_value}]'


async def output_counters(counters: list[Counter]):
    while True:  # noqa: WPS457
        messages = [str(counter) for counter in counters if not counter.is_max()]
        sys.stdout.write('; '.join(messages) + '\n')  # noqa: WPS336
        await asyncio.sleep(0.5)
