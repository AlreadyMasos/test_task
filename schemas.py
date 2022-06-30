from marshmallow import Schema, validate, fields


class BookSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=[
        validate.Length(max=100)
    ])
    author = fields.String(validate=[
        validate.Length(max=100)
    ])