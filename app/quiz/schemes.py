from marshmallow import Schema, fields


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    scores = fields.Int(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    answers = fields.Nested(AnswerSchema, many=True, required=True)


class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)
