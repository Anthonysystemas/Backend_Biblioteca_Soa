import os
from passlib.context import CryptContext

# Configuración de la aplicación
SECRET_KEY = os.getenv("SECRET_KEY", "BiBlIoTeCa-2025-SeCreT-KeY-$uP3r-S3cUrE-@#$%^&*()")
TOKEN_EXPIRE_HOURS = 24
ALGORITHM = "HS256"

# Configuración de encriptación de passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuración de archivos
USERS_FILE = "users.json"