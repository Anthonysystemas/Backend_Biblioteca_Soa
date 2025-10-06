from pydantic import BaseModel, EmailStr

# ===== In =====
class LoginIn(BaseModel):
    email: EmailStr
    password: str

# ===== Out =====
class LoginOut(BaseModel):
    access_token: str
    refresh_token: str

class MeOut(BaseModel):
    user_id: int
    email: EmailStr

class RefreshOut(BaseModel):
    access_token: str
