import os
import typing
from dataclasses import dataclass
import yaml
from dotenv import load_dotenv

if typing.TYPE_CHECKING:
    from app.web.app import Application


load_dotenv()
bot_token = os.getenv('bot_token')


@dataclass
class SessionConfig:
    key: str


@dataclass
class AdminConfig:
    email: str
    password: str


@dataclass
class BotConfig:
    token: str
    group_id: int


@dataclass
class DatabaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "anna"
    password: str = "creator"
    database: str = "TgBotAiohttp"

    @property
    def url_create(self):
        return f'postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'


@dataclass
class Config:
    admin: AdminConfig
    session: SessionConfig | None = None
    bot: BotConfig | None = None
    database: DatabaseConfig | None = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(
            key=raw_config["session"]["key"],
        ),
        admin=AdminConfig(
            email=raw_config["admin"]["email"],
            password=raw_config["admin"]["password"],
        ),
        bot=BotConfig(
            token=bot_token,
            group_id=raw_config["bot"]["group_id"],
        ),
        database=DatabaseConfig(**raw_config["database"]),
    )
