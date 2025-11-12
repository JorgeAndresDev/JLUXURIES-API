from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# 🔑 Variables globales
SECRET_KEY = "clave_super_secreta_123"  # cámbiala en producción
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# 🧂 Configuración del contexto de hash
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- HASHING ---
def hash_password(password: str) -> str:
    """Devuelve la contraseña encriptada con bcrypt."""
    return pwd_context.hash(password)

def verificar_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)

# --- TOKEN JWT ---
def crear_token(data: dict, expires_delta: timedelta = None) -> str:
    """Crea un JWT con expiración."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
