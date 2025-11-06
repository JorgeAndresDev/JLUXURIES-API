from datetime import timedelta
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from Apps.auth.auth import ALGORITHM, SECRET_KEY, crear_token, verificar_password
from Conexion.conexion import conexiondb

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def login_service(email: str, password: str):
    connection = conexiondb()
    try:
        with connection.cursor(dictionary=True) as cursor:
            cursor.execute("SELECT * FROM cliente WHERE email = %s", (email,))
            user = cursor.fetchone()
            if not user:
                raise HTTPException(status_code=400, detail="Usuario no encontrado")

            if not verificar_password(password, user["password"]):
                raise HTTPException(status_code=400, detail="Contraseña incorrecta")

            access_token_expires = timedelta(minutes=60)
            access_token = crear_token(data={"sub": user["email"]}, expires_delta=access_token_expires)

            return {"access_token": access_token, "token_type": "bearer"}
    finally:
        connection.close()


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Token expirado o inválido")
