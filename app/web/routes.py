from aiohttp.web_app import Application

__all__ = ("setup_routes",)


def setup_routes(application: Application):
    import app.users.routes
    import app.admin.routes
    import app.quiz.routes

    app.admin.routes.register_urls(application)
    app.users.routes.register_urls(application)
    app.quiz.routes.register_urls(application)
