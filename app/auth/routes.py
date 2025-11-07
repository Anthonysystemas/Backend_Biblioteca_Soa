# app/auth/routes.py
from flask import Blueprint, request
from pydantic import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_required
from .dtos import LoginIn, RegisterIn
from .service import login as login_uc, me as me_uc, refresh as refresh_uc, register as register_uc

bp = Blueprint("auth", __name__)

@bp.post("/login")
def login():
    """Autenticación con email/password → access & refresh tokens"""
    try:
        data = LoginIn(**(request.get_json() or {}))
    except ValidationError as e:
        return {"code": "VALIDATION_ERROR", "errors": e.errors()}, 422

    out = login_uc(data)
    if not out:
        return {"code": "UNAUTHORIZED", "message": "Credenciales inválidas"}, 401
    return out.model_dump(), 200


@bp.post("/register")
def register():
    """Registro de nuevo usuario con nombre completo, email y contraseña"""
    try:
        data = RegisterIn.model_validate(request.get_json() or {})
    except ValidationError as e:
        errors = []
        for error in e.errors():
            errors.append({
                "field": ".".join(str(x) for x in error["loc"]),
                "message": error["msg"]
            })
        return {"code": "VALIDATION_ERROR", "errors": errors}, 422

    out = register_uc(data)
    if not out:
        return {"code": "EMAIL_EXISTS", "message": "El email ya está registrado"}, 409
    return out.model_dump(), 201


@bp.get("/me")
@jwt_required()
def me():
    """Datos básicos del usuario autenticado"""
    uid = get_jwt_identity()
    out = me_uc(uid)
    return out.model_dump(), 200


@bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    """Emite un nuevo access token usando el refresh token válido"""
    uid = get_jwt_identity()
    out = refresh_uc(uid)
    return out.model_dump(), 200
