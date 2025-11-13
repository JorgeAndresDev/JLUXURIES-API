from datetime import timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from Apps.auth.auth import ALGORITHM, SECRET_KEY, crear_token, verificar_password, hash_password
from Conexion.conexion import conexiondb
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", scheme_name="JWT")
security = HTTPBearer()

def obtener_usuario_actual(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")


# --- LOGIN ---
def login_service(email: str, password: str):
    connection = conexiondb()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
            user = cursor.fetchone()

            # ✅ Validar si el usuario existe
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no encontrado"
                )

            # ✅ Validar contraseña
            if not verificar_password(password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Contraseña incorrecta"
                )

            # ✅ Crear el token JWT
            access_token_expires = timedelta(minutes=60)
            access_token = crear_token(
                data={"sub": user["email"]},
                expires_delta=access_token_expires
            )

            return {
                "access_token": access_token,
                "token_type": "bearer",
                "usuario": user["nombre"]
            }

    except HTTPException:
        # Re-lanzamos excepciones controladas
        raise
    except Exception as e:
        # Cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Error interno: {e}")
    finally:
        connection.close()


# --- REGISTRO ---
def registrar_cliente(nombre: str, email: str, password: str):
    connection = conexiondb()
    try:
        with connection.cursor() as cursor:
            hashed = hash_password(password)
            cursor.execute(
                "INSERT INTO clientes (nombre, email, password) VALUES (%s, %s, %s)",
                (nombre, email, hashed)
            )
            connection.commit()
        return {"message": "Cliente registrado correctamente"}
    finally:
        connection.close()

def obtener_todos_los_clientes():
    connection = conexiondb()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT id_cliente, nombre, email, fecha_registro FROM clientes")
            clientes = cursor.fetchall()
            return clientes
    finally:
        connection.close()



def obtener_todos_los_clientes_service(usuario: str = Depends(obtener_usuario_actual)):
    """
    Devuelve todos los clientes registrados (protegido con token)
    """
    try:
        conexion = conexiondb()
        cursor = conexion.cursor(dictionary=True)
        cursor.execute("SELECT id_cliente, nombre, email FROM clientes")
        clientes = cursor.fetchall()
        conexion.close()
        return {"mensaje": "Clientes obtenidos correctamente", "clientes": clientes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener clientes: {e}")


