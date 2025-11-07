from typing import Optional
from flask_jwt_extended import create_access_token, create_refresh_token
from app.common.security import verify_password, hash_password
from app.common.models import User
from app.extensions import db
from .dtos import LoginIn, LoginOut, MeOut, RefreshOut, RegisterIn, RegisterOut


def login(data: LoginIn) -> Optional[LoginOut]:
    user = User.query.filter_by(email=data.email, is_active=True).first()
    if not user or not verify_password(data.password, user.password_hash):
        return None

    claims = {"roles": ["reader"]}  
    access = create_access_token(identity=user.id, additional_claims=claims)
    refresh = create_refresh_token(identity=user.id)
    return LoginOut(access_token=access, refresh_token=refresh)


def me(user_id: int) -> MeOut:
    user = User.query.get(user_id)
    email = user.email if user else "unknown@example.com"
    return MeOut(user_id=user_id, email=email)


def refresh(user_id: int) -> RefreshOut:
    claims = {"roles": ["reader"]}
    new_access = create_access_token(identity=user_id, additional_claims=claims)
    return RefreshOut(access_token=new_access)


def register(data: RegisterIn) -> Optional[RegisterOut]:
    # Verificar si el email ya existe
    existing_user = User.query.filter_by(email=data.email).first()
    if existing_user:
        return None

    # Crear nuevo usuario
    new_user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
        is_active=True
    )

    db.session.add(new_user)
    db.session.commit()

    return RegisterOut(
        user_id=new_user.id,
        email=new_user.email,
        full_name=new_user.full_name,
        message="Usuario registrado exitosamente"
    )
