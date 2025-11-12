from fastapi import APIRouter, Depends, Form
from Apps.auth.services import (
    obtener_todos_los_clientes_service,
    obtener_usuario_actual,
    login_service,
    registrar_cliente
)

router = APIRouter(prefix="/auth", tags=["auth"])

# --- LOGIN ---
@router.post("/login", summary="Iniciar sesión y obtener token")
def login(email: str = Form(...), password: str = Form(...)):
    return login_service(email, password)

# --- REGISTRO ---
@router.post("/register", summary="Registrar un nuevo cliente")
def register(
    nombre: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    """
    Registra un nuevo cliente con nombre, email y contraseña encriptada.
    """
    return registrar_cliente(nombre, email, password)

# --- OBTENER CLIENTES (protegido con JWT) ---
@router.get("/clientes", summary="Listar todos los clientes (requiere token)")
def listar_clientes(usuario: str = Depends(obtener_usuario_actual)):
    return obtener_todos_los_clientes_service(usuario)
