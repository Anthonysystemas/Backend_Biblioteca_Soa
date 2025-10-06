from flask import Flask
from .extensions import db, jwt
from .config import Config
from .auth.routes import bp as auth_bp
from .catalog.routes import bp as catalog_bp
from .reservations.routes import bp as res_bp
from .common.models import create_all_tables

def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    db.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(catalog_bp, url_prefix="/catalog")
    app.register_blueprint(res_bp, url_prefix="/reservations")

    # Auto create tables (for demo/dev; replace with Alembic in prod)
    with app.app_context():
        create_all_tables()

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
