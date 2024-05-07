from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound, HTTPBadRequest
from aiohttp_apispec import querystring_schema, request_schema, response_schema
from app.quiz.models import AnswerModel
from app.quiz.schemes import (
    ListQuestionSchema,
    QuestionSchema,
)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import json_response


class QuestionAddView(AuthRequiredMixin, View):
    @request_schema(QuestionSchema)
    @response_schema(QuestionSchema)
    async def post(self):
        title = self.data["title"]
        answers = [
            AnswerModel(
                title=answer['title'],
                scores=answer['scores']
            ) for answer in self.data['answers']
        ]
        check_question_title = await self.store.quizzes.get_question_by_title(title=title)
        if check_question_title is not None:
            raise HTTPConflict
        if len(answers) < 1:
            raise HTTPBadRequest
        question = await self.store.quizzes.create_question(title=title, answers=answers)

        return json_response(data=QuestionSchema().dump(question))


class QuestionListView(AuthRequiredMixin, View):
    @response_schema(ListQuestionSchema)
    async def get(self):
        question_title = self.request.query.get('title')
        if question_title is not None:
            questions = await self.store.quizzes.list_questions(question_title)
        else:
            questions = await self.store.quizzes.list_questions()
        rows_questions = [QuestionSchema().dump(question) for question in questions]
        return json_response(data={'questions': rows_questions})
