from typing import Optional
from app.common.models import User
from app.extensions import db
from .dtos import UpdateProfileIn, UpdateProfileOut, UserProfileOut, DeactivateAccountOut


def update_profile(user_id: int, data: UpdateProfileIn) -> Optional[UpdateProfileOut]:
    """
    Actualiza el perfil del usuario autenticado

    Args:
        user_id: ID del usuario autenticado
        data: Datos para actualizar (nombre y email)

    Returns:
        UpdateProfileOut si fue exitoso, None si el usuario no existe o el email ya está en uso
    """
    # Buscar usuario actual
    user = User.query.get(user_id)
    if not user or not user.is_active:
        return None

    # Verificar si el nuevo email ya está en uso por otro usuario
    if data.email != user.email:
        existing_user = User.query.filter_by(email=data.email).first()
        if existing_user and existing_user.id != user_id:
            return None  # Email ya existe

    # Actualizar datos
    user.full_name = data.full_name
    user.email = data.email

    db.session.commit()

    return UpdateProfileOut(
        user_id=user.id,
        full_name=user.full_name,
        email=user.email,
        message="Perfil actualizado exitosamente"
    )


def get_user_profile(user_id: int) -> Optional[UserProfileOut]:
    """
    Obtiene el perfil de un usuario por su ID

    Args:
        user_id: ID del usuario a consultar

    Returns:
        UserProfileOut con los datos del usuario, None si no existe
    """
    user = User.query.get(user_id)
    if not user:
        return None

    return UserProfileOut(
        user_id=user.id,
        full_name=user.full_name or "Sin nombre",
        email=user.email,
        is_active=user.is_active
    )


def deactivate_account(user_id: int) -> Optional[DeactivateAccountOut]:
    """
    Desactiva la cuenta del usuario autenticado

    Args:
        user_id: ID del usuario autenticado

    Returns:
        DeactivateAccountOut si fue exitoso, None si el usuario no existe
    """
    user = User.query.get(user_id)
    if not user:
        return None

    # Marcar como inactivo
    user.is_active = False

    db.session.commit()

    return DeactivateAccountOut(
        message="Cuenta desactivada exitosamente"
    )
