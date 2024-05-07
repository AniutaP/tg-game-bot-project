from aiohttp.web import (
    Application as AiohttpApplication,
    Request as AiohttpRequest,
    View as AiohttpView,
)

from app.admin.models import AdminModel
from app.store.store import Store
from app.store.database.database import Database
from app.store.store import setup_store
from app.web.config import setup_config, Config
from app.web.mw import setup_middlewares
from app.web.routes import setup_routes
from app.web.logger import setup_logging
from aiohttp_session import setup as session_setup
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_apispec import setup_aiohttp_apispec


__all__ = ("Application",
           "Request",
           "View",
           "setup_app",)


class Application(AiohttpApplication):
    config: Config | None = None
    store: Store | None = None
    database: Database | None = None


class Request(AiohttpRequest):
    admin: AdminModel | None = None

    @property
    def app(self) -> Application:
        return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def database(self) -> Database:
        return self.request.app.database

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})


app = Application()


def setup_app(config_path: str) -> Application:
    setup_logging(app)
    setup_config(app, config_path)
    session_setup(app, EncryptedCookieStorage(app.config.session.key))
    setup_routes(app)
    setup_aiohttp_apispec(
        app, title="Tg Quiz Bot", url="/docs/json", swagger_path="/docs"
    )
    setup_middlewares(app)
    setup_store(app)
    return app
