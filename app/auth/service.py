from typing import Optional
from datetime import datetime, timedelta
import secrets
from flask_jwt_extended import create_access_token, create_refresh_token
from app.common.security import verify_password, hash_password
from app.common.models import User, PasswordResetToken
from app.extensions import db
from .dtos import (
    LoginIn, LoginOut, MeOut, RefreshOut, RegisterIn, RegisterOut,
    ForgotPasswordIn, ForgotPasswordOut, ResetPasswordIn, ResetPasswordOut
)


def login(data: LoginIn) -> Optional[LoginOut]:
    user = User.query.filter_by(email=data.email, is_active=True).first()
    if not user or not verify_password(data.password, user.password_hash):
        return None

    claims = {"roles": ["reader"]}
    access = create_access_token(identity=str(user.id), additional_claims=claims)
    refresh = create_refresh_token(identity=str(user.id))
    return LoginOut(access_token=access, refresh_token=refresh)


def me(user_id: int) -> MeOut:
    user = User.query.get(user_id)
    email = user.email if user else "unknown@example.com"
    return MeOut(user_id=user_id, email=email)


def refresh(user_id: int) -> RefreshOut:
    claims = {"roles": ["reader"]}
    new_access = create_access_token(identity=str(user_id), additional_claims=claims)
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


def forgot_password(data: ForgotPasswordIn) -> Optional[ForgotPasswordOut]:
    # Buscar usuario por email
    user = User.query.filter_by(email=data.email, is_active=True).first()
    if not user:
        # Por seguridad, no revelamos si el email existe o no
        # Pero retornamos None para manejarlo diferente
        return None

    # Generar token seguro
    token = secrets.token_urlsafe(32)

    # Expiración: 1 hora desde ahora
    expires_at = datetime.utcnow() + timedelta(hours=1)

    # Invalidar tokens anteriores del mismo usuario
    PasswordResetToken.query.filter_by(user_id=user.id, used=False).update({"used": True})

    # Crear nuevo token
    reset_token = PasswordResetToken(
        user_id=user.id,
        token=token,
        expires_at=expires_at
    )

    db.session.add(reset_token)
    db.session.commit()

   
    return ForgotPasswordOut(
        message="Token de recuperación generado exitosamente",
        token=token
    )


def reset_password(data: ResetPasswordIn) -> Optional[ResetPasswordOut]:
    # Buscar el token
    reset_token = PasswordResetToken.query.filter_by(
        token=data.token,
        used=False
    ).first()

    if not reset_token:
        return None

    # Verificar si el token expiró
    if reset_token.expires_at < datetime.utcnow():
        return None

    # Obtener el usuario
    user = User.query.get(reset_token.user_id)
    if not user or not user.is_active:
        return None

    # Actualizar contraseña
    user.password_hash = hash_password(data.new_password)

    # Marcar token como usado
    reset_token.used = True

    db.session.commit()

    return ResetPasswordOut(
        message="Contraseña actualizada exitosamente"
    )
