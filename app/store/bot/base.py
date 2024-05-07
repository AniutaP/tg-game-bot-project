import asyncio
from app.base.base_accessor import BaseAccessor
from app.store.bot.poller import Poller
from app.store.bot.worker import Worker
import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TgBot(BaseAccessor):
    def __init__(self, app: "Application", n: int, *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.token = self.app.config.bot.token
        self.queue = asyncio.Queue()
        self.poller = Poller(self.token, self.queue)
        self.worker = Worker(self.token, self.queue, n)

    async def start(self):
        await self.poller.start()
        await self.worker.start()

    async def stop(self):
        await self.poller.stop()
        await self.worker.stop()
