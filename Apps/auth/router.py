from fastapi import APIRouter, Depends, Form
from Apps.auth.services import obtener_usuario_actual
from Apps.auth.services import login_service

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", summary="Iniciar sesión y obtener token")
def login(email: str = Form(...), password: str = Form(...)):
    return login_service(email, password)

@router.get("/clientes")
def get_all_clientes(usuario: str = Depends(obtener_usuario_actual)):
    return {"mensaje": f"Bienvenido {usuario}"}
