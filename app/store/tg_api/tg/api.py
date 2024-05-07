import typing
from typing import Optional
import aiohttp
from aiohttp import ClientSession, TCPConnector
from app.base.base_accessor import BaseAccessor
from app.store.tg_api.tg.dcs import GetUpdatesResponse, SendMessageResponse, UpdateObj, Message, MessageFrom, Chat

if typing.TYPE_CHECKING:
    from app.web.app import Application


class TgClient(BaseAccessor):
    def __init__(self, app: "Application", *args, **kwargs):
        super().__init__(app, *args, **kwargs)
        self.token = self.app.config.bot.token
        self.session: ClientSession | None = None
        self.key: str | None = None
        self.bot = None

    async def connect(self, app: "Application") -> None:
        self.session = ClientSession(connector=TCPConnector(verify_ssl=False))
        self.bot = app.store.bots_manager
        self.logger.info("start polling")
        await self.bot.start()
        await self.run_echo()

    async def disconnect(self, app: "Application") -> None:
        if self.session:
            await self.session.close()

        if self.bot:
            await self.bot.stop()

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    async def get_me(self) -> dict:
        url = self.get_url("getMe")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                return await resp.json()

    async def get_updates(self, offset: Optional[int] = None, timeout: int = 0) -> dict:
        url = self.get_url("getUpdates")
        params = {}
        if offset:
            params['offset'] = offset
        if timeout:
            params['timeout'] = timeout
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as resp:
                return await resp.json()

    async def get_updates_in_objects(self, offset: Optional[int] = None, timeout: int = 0) -> GetUpdatesResponse:
        res_dict = await self.get_updates(offset=offset, timeout=timeout)
        updates = [
            UpdateObj(
                update_id=item['update_id'],
                message=Message(
                    message_id=item['message']['message_id'],
                    from_=MessageFrom(
                        id=item['message']['from']['id'],
                        first_name=item['message']['from']['first_name'],
                        is_bot=item['message']['from']['is_bot'],
                        username=item['message']['from']['username']),
                    chat=Chat(id=item['message']['chat']['id'],
                              type=item['message']['chat']['type']),
                    text=item['message']['text'])) for item in res_dict['result']]
        return GetUpdatesResponse(ok=res_dict['ok'], result=updates)

    async def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url("sendMessage")
        payload = {
            'chat_id': chat_id,
            'text': text
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=payload) as resp:
                res_dict = await resp.json()
                res_dict_message = res_dict['result']
                message = Message(
                    message_id=res_dict_message['message_id'],
                    from_=MessageFrom(
                        id=res_dict_message['from']['id'],
                        first_name=res_dict_message['from']['first_name'],
                        is_bot=res_dict_message['from']['is_bot'],
                        username=res_dict_message['from']['username']),
                    chat=Chat(id=res_dict_message['chat']['id'],
                              type=res_dict_message['chat']['type'])
                )
                return SendMessageResponse(ok=res_dict['ok'], result=message)

    async def run_echo(self):
        offset = 0
        while True:
            res = await self.get_updates_in_objects(offset=offset, timeout=60)
            for item in res.result:
                offset = item.update_id + 1
                await self.send_message(item.message.chat.id, item.message.text)
                print(f'{item.message.chat.id}, {item.message.from_}')
