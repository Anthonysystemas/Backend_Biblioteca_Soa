from pydantic import BaseModel, EmailStr, field_validator

# ===== Input DTOs =====
class UpdateProfileIn(BaseModel):
    full_name: str
    email: EmailStr

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('El nombre completo debe tener al menos 2 caracteres')
        return v.strip()


# ===== Output DTOs =====
class UpdateProfileOut(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    message: str


class UserProfileOut(BaseModel):
    user_id: int
    full_name: str
    email: EmailStr
    is_active: bool


class DeactivateAccountOut(BaseModel):
    message: str
