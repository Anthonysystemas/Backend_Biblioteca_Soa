from app import create_app
from app.extensions import db
from app.common.models import User, Book
from app.common.security import hash_password

app = create_app()

with app.app_context():
    if not User.query.filter_by(email="test@example.com").first():
        u = User(email="test@example.com", password_hash=hash_password("secret"))
        db.session.add(u)
    if not Book.query.first():
        books = [
            Book(isbn="9780135166307", title="Clean Architecture", author="Robert C. Martin", available_copies=3),
            Book(isbn="9781492051367", title="Fluent Python", author="Luciano Ramalho", available_copies=2),
            Book(isbn="9780596007973", title="Head First Design Patterns", author="Eric Freeman", available_copies=1),
        ]
        db.session.add_all(books)
    db.session.commit()
    print("Seed completed: user test@example.com / secret, and sample books created.")
