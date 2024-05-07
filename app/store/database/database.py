from typing import TYPE_CHECKING, Any
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker, create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from app.quiz.models import QuestionModel
from app.store.database.sqlalchemy_base import BaseModel
import app.admin.models as admin_model
if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application") -> None:
        self.app = app
        self.engine: AsyncEngine | None = None
        self._db: type[DeclarativeBase] = BaseModel
        self.session: async_sessionmaker[AsyncSession] | None = None

    async def connect(self, *args: Any, **kwargs: Any) -> None:
        self.engine = create_async_engine(self.app.config.database.url_create, echo=True)
        self.session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        if self.engine:
            session = self.session()
            await session.execute(delete(admin_model.AdminModel))
            await session.execute(delete(QuestionModel))
            await session.commit()

            await self.engine.dispose()
