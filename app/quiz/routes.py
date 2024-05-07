import typing

from app.quiz.views import (
    QuestionAddView,
    QuestionListView,
)

if typing.TYPE_CHECKING:
    from app.web.app import Application


__all__ = ("register_urls",)


def register_urls(app: "Application"):
    app.router.add_view("/quiz.add_question", QuestionAddView)
    app.router.add_view("/quiz.list_questions", QuestionListView)
