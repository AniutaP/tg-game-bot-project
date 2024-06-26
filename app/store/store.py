import typing
from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.admin.accessor import AdminAccessor
        from app.users.accessor import UserAccessor
        from app.store.bot.base import TgBot
        from app.store.quiz.accessor import QuizAccessor
        from app.store.tg_api.tg.api import TgClient

        self.user = UserAccessor(self)
        self.quizzes = QuizAccessor(app)
        self.admins = AdminAccessor(app)
        self.bots_manager = TgBot(app, 2)
        self.tg_api = TgClient(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
