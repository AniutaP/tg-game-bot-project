import asyncio
from asyncio import Task
from typing import Optional
from app.store.tg_api.tg.api import TgClient
from app.store.store import Store


class Poller:
    def __init__(self, store: Store, token: str, queue: asyncio.Queue = None):
        self.queue = queue
        self.token = token
        self._task: Optional[Task] = None
        self.store = store

    async def _worker(self):
        offset = 0
        while True:
            res = await self.store.tg_api.get_updates_in_objects(offset=offset, timeout=60)
            for u in res.result:
                offset = u.update_id + 1
                self.queue.put_nowait(u)

    async def start(self):
        self._task = asyncio.create_task(self._worker())

    async def stop(self):
        self._task.cancel()
