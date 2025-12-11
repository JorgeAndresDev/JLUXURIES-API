from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import JWTError, jwt
from passlib.context import CryptContext

# --- CONFIGURACIÓN ---
SECRET_KEY = "clave_super_secreta_123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# --- HASH ---
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verificar_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# --- CREAR TOKEN ---
def crear_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --- DECODIFICAR TOKEN ---
from Conexion.conexion import conexiondb

# --- DECODIFICAR TOKEN ---
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    cred_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise cred_exception
        
        # Fetch user from DB to get role and id
        connection = conexiondb()
        if not connection:
             raise HTTPException(status_code=500, detail="Database connection error")
        
        try:
            with connection.cursor(dictionary=True) as cursor:
                cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
                user = cursor.fetchone()
                if user is None:
                    raise cred_exception
                return user
        finally:
            connection.close()

    except JWTError:
        raise cred_exception

def get_current_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permisos de administrador"
        )
    return current_user
