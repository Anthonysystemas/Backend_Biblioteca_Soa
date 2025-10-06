from ..common.models import Reservation, ReservationStatus
from ..extensions import db
from .tasks import hold_copy_async

def create_reservation(user_id: int, book_id: int) -> int:
    r = Reservation(user_id=user_id, book_id=book_id, status=ReservationStatus.PENDING)
    db.session.add(r)
    db.session.commit()
    hold_copy_async.delay(r.id)
    return r.id
