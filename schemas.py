from marshmallow import Schema, fields

class UserRegisterSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class NoteCreateSchema(Schema):
    title = fields.String(required=True)
    body = fields.String(load_default="")

class NoteOutSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    body = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()