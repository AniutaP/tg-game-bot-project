from typing import TYPE_CHECKING
from app.admin.models import AdminModel
from app.base.base_accessor import BaseAccessor
from app.web.utils import hash_password
from sqlalchemy import select, insert

if TYPE_CHECKING:
    from app.web.app import Application


class AdminAccessor(BaseAccessor):
    async def connect(self, app: "Application") -> None:
        admin = await self.get_by_email(email=self.app.config.admin.email)
        if not admin:
            await self.create_admin(email=self.app.config.admin.email, password=self.app.config.admin.password)

    async def get_by_email(self, email: str) -> AdminModel | None:
        async with self.app.database.session() as session:
            query = select(AdminModel).where(AdminModel.email == email)
            res = await session.execute(query)
            admin = res.scalar()
            if admin is not None:
                return admin
            return None

    async def create_admin(self, email: str, password: str) -> AdminModel:
        async with self.app.database.session() as session:
            encoded_password = hash_password(password)
            query = insert(AdminModel).values(email=email, password=encoded_password)
            res = await session.execute(query)
            admin = res.scalar()
            await session.commit()
        return admin
