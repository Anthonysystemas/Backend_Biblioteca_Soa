from infrastructure.celery_app import celery

@celery.task(
    name="reservations.hold_copy_async",
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    max_retries=3,
)
def hold_copy_async(self, reservation_id: int):
    from app.extensions import db
    from app.common.models import Reservation, ReservationStatus, Book

    try:
        with db.session.begin():
            r = db.session.get(Reservation, reservation_id)
            if not r or r.status != ReservationStatus.PENDING:
                return {"status": "ignored", "id": reservation_id}

            book = db.session.get(Book, r.book_id)
            if not book or (book.available_copies or 0) <= 0:
                r.status = ReservationStatus.CANCELLED
                return {"status": "cancelled_no_stock", "id": reservation_id}

            book.available_copies -= 1
            r.status = ReservationStatus.HELD

        return {"status": "held", "id": reservation_id, "book_id": r.book_id}
    except Exception as e:
        return {"status": "error", "id": reservation_id, "error": str(e)}
