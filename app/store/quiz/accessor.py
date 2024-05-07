from collections.abc import Iterable, Sequence
from sqlalchemy import select, insert, and_
from sqlalchemy.orm import selectinload
from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    AnswerModel,
    QuestionModel,
)


class QuizAccessor(BaseAccessor):

    async def create_question(
        self, title: str, answers: Iterable[AnswerModel]
    ) -> QuestionModel:
        async with self.app.database.session() as session:
            query_insert_question = insert(QuestionModel).values(title=title)
            await session.execute(query_insert_question)

            select_current_question = select(QuestionModel).where(QuestionModel.title == title)
            current_question_raw = await session.execute(select_current_question)
            current_question = current_question_raw.scalar()
            query_insert_answers = insert(AnswerModel).values(
                [
                    {
                        "title": answer.title,
                        "scores": answer.scores,
                        "question_id": current_question.id,
                    }
                    for answer in answers
                ]
            )

            await session.execute(query_insert_answers)
            await session.commit()
            query_get_current_question_with_answers = select(QuestionModel).where(QuestionModel.title == title)
            res = await session.execute(
                query_get_current_question_with_answers.options(selectinload(QuestionModel.answers))
            )
            question = res.scalar()

            return question

    async def get_question_by_title(self, title: str) -> QuestionModel | None:
        async with self.app.database.session() as session:
            query = select(QuestionModel).where(QuestionModel.title == title)
            res = await session.execute(query)
            question = res.scalar()
            if question is not None:
                return question
            return None

    async def list_questions(self) -> Sequence[QuestionModel]:
        async with self.app.database.session() as session:
            query = select(QuestionModel)
            res = await session.execute(query.options(selectinload(QuestionModel.answers)))
            questions = res.scalars().all()
            return questions
