from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note
from extensions import db
from note_service import NoteService

ns = Namespace("notes", description="Notes operations")

note_in = ns.model("NoteIn", {
    "title": fields.String(required=True, example="Buy milk"),
    "body": fields.String(example="2 bottles of almond milk")
})

note_out = ns.model("NoteOut", {
    "id": fields.Integer,
    "title": fields.String,
    "body": fields.String,
    "created_at": fields.DateTime,
    "updated_at": fields.DateTime
})

pagination = ns.model("Pagination", {
    "items": fields.List(fields.Nested(note_out)),
    "page": fields.Integer,
    "pages": fields.Integer,
    "total": fields.Integer
})

@ns.route("")
class NoteList(Resource):
    @jwt_required()
    @ns.marshal_with(pagination)
    @ns.doc(params={"q": "keyword", "page": "page number", "per_page": "page size"})
    def get(self):
        user_id = get_jwt_identity()
        q = request.args.get("q")
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))
        p = NoteService.list_notes(user_id, q, page, per_page)
        return {"items": p.items, "page": p.page, "pages": p.pages, "total": p.total}

    @jwt_required()
    @ns.expect(note_in)
    @ns.marshal_with(note_out, code=201)
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        note = NoteService.create_note(user_id, data["title"], data.get("body", ""))
        return note, 201

@ns.route("/<int:note_id>")
class NoteDetail(Resource):
    @jwt_required()
    @ns.marshal_with(note_out)
    def get(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            ns.abort(404, "Note not found")
        return note

    @jwt_required()
    @ns.expect(note_in)
    @ns.marshal_with(note_out)
    def put(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            ns.abort(404, "Note not found")
        data = request.get_json() or {}
        note = NoteService.update_note(note, data["title"], data.get("body", ""))
        return note

    @jwt_required()
    def delete(self, note_id):
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            ns.abort(404, "Note not found")
        NoteService.delete_note(note)
        return {"message": "deleted"}