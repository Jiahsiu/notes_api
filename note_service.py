from typing import Optional
from models import Note
from extensions import db

class NoteService:
    @staticmethod
    def list_notes(user_id: int, q: Optional[str] = None, page: int = 1, per_page: int = 10):
        query = Note.query.filter_by(user_id=user_id)
        if q:
            like = f"%{q}%"
            query = query.filter((Note.title.ilike(like)) | (Note.body.ilike(like)))
        return query.order_by(Note.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def create_note(user_id: int, title: str, body: str = "") -> Note:
        note = Note(user_id=user_id, title=title, body=body)
        db.session.add(note)
        db.session.commit()
        return note

    @staticmethod
    def update_note(note: Note, title: str, body: str) -> Note:
        note.title = title
        note.body = body
        db.session.commit()
        return note

    @staticmethod
    def delete_note(note: Note) -> None:
        db.session.delete(note)
        db.session.commit()