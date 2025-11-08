from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..extensions import db
from ..common.models import Reservation, ReservationStatus, Book
from .service import create_reservation

bp = Blueprint("reservations", __name__)

@bp.post("/")
@jwt_required()
def create():
    uid = int(get_jwt_identity())
    payload = request.get_json() or {}
    book_id = payload.get("book_id")
    if not book_id:
        return {"msg": "book_id es requerido"}, 400
    rid = create_reservation(uid, book_id)
    return {"reservation_id": rid}, 202

@bp.post("/<int:rid>/confirm")
@jwt_required()
def confirm(rid: int):
    r = Reservation.query.get_or_404(rid)
    if r.status != ReservationStatus.HELD:
        return {"msg": f"No se puede confirmar desde {r.status}"}, 409
    r.status = ReservationStatus.CONFIRMED
    db.session.commit()
    return {"status": r.status}, 200

@bp.post("/<int:rid>/cancel")
@jwt_required()
def cancel(rid: int):
    r = Reservation.query.get_or_404(rid)
    if r.status == ReservationStatus.HELD:
        book = Book.query.get(r.book_id)
        if book:
            book.available_copies += 1
    r.status = ReservationStatus.CANCELLED
    db.session.commit()
    return {"status": r.status}, 200
