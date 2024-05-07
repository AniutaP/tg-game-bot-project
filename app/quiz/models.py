from sqlalchemy.orm import relationship
from app.store.database.sqlalchemy_base import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean


class QuestionModel(BaseModel):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    answers = relationship("AnswerModel")

    def __repr__(self):
        return f"<QuestionModel(id='{self.id}', title='{self.title}')>"


class AnswerModel(BaseModel):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    scores = Column(Integer, nullable=False)
    question_id = Column(ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f"<AnswerModel(id='{self.id}', title='{self.title}', scores='{self.scores}')>"
