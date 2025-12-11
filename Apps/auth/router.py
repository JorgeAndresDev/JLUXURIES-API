from Apps.auth.schemas import LoginRequest, RegisterRequest
from fastapi import APIRouter, Depends, Form
from Apps.auth.services import (
    obtener_todos_los_clientes_service,
    login_service,
    registrar_cliente
)
from Apps.auth.auth import get_current_user, get_current_admin


router = APIRouter(prefix="/auth", tags=["auth"])

# --- LOGIN ---
@router.post("/login")
def login(data: LoginRequest):
    return login_service(data.email, data.password)
# --- REGISTRO ---


@router.post("/register", summary="Registrar un nuevo cliente")
def register(data: RegisterRequest):
    return registrar_cliente(data.nombre, data.email, data.password, data.telefono, data.direccion)


# --- OBTENER CLIENTES ---
@router.get("/clientes", summary="Listar todos los clientes (requiere token admin)")
def listar_clientes(usuario: dict = Depends(get_current_admin)):
    return obtener_todos_los_clientes_service(usuario)

# --- RUTA PROTEGIDA /me ---
@router.get("/me")
async def me(current_user = Depends(get_current_user)):
    return current_user
