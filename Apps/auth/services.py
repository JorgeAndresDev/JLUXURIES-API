from datetime import timedelta
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from Apps.auth.auth import ALGORITHM, SECRET_KEY, crear_token, verificar_password, hash_password
from Conexion.conexion import conexiondb
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from Apps.auth.auth import (
    crear_token,
    verificar_password,
    hash_password,
    get_current_user
)


security = HTTPBearer()

# obtener_usuario_actual removed in favor of auth.get_current_user


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
                "usuario": {
                    "id_cliente": user["id_cliente"],
                    "email": user["email"],
                    "nombre": user["nombre"],
                    "telefono": user.get("telefono"),
                    "direccion": user.get("direccion"),
                    "role": user.get("role")
                }
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
def registrar_cliente(nombre: str, email: str, password: str, telefono: str = None, direccion: str = None):
    connection = conexiondb()
    try:
        with connection.cursor() as cursor:
            hashed = hash_password(password)
            cursor.execute(
                "INSERT INTO clientes (nombre, email, password, telefono, direccion, role) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, email, hashed, telefono, direccion, 'client')
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



from Apps.auth.auth import get_current_admin

def obtener_todos_los_clientes_service(usuario: dict = Depends(get_current_admin)):
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


