import asyncio
from typing import AsyncIterator, Dict, Generic, TypeVar

T = TypeVar("T")


class PubSubQueue(Generic[T]):
    suscriptions: Dict[str, asyncio.Queue[T]] = {}

    async def pub(self, *, topic: str, item: T) -> None:
        if topic in self.suscriptions:
            await self.suscriptions[topic].put(item)

    async def sub(self, *, topic: str) -> AsyncIterator[T]:
        if topic not in self.suscriptions:
            self.suscriptions[topic] = asyncio.Queue()
        while True:
            yield await self.suscriptions[topic].get()
