from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, response_schema
from aiohttp_session import new_session
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response
from app.admin.schemes import AdminSchema
from app.web.app import View
from app.web.utils import hash_password


class AdminLoginView(View):
    @request_schema(AdminSchema)
    @response_schema(AdminSchema, 200)
    async def post(self):
        data = self.data
        admin_auth = await self.store.admins.get_by_email(data["email"])
        if not admin_auth:
            raise HTTPForbidden
        if hash_password(data["password"]) != admin_auth.password:
            raise HTTPForbidden
        raw_admin = AdminSchema().dump(admin_auth)
        session = await new_session(request=self.request)
        session["admin"] = raw_admin
        return json_response(data=raw_admin)


class AdminCurrentView(AuthRequiredMixin, View):
    @response_schema(AdminSchema, 200)
    async def get(self):
        return json_response(data=AdminSchema().dump(self.request.admin))
