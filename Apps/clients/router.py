from fastapi import APIRouter, HTTPException
from Apps.clients.schemas import clientCreate
from Apps.clients.services import get_all_cliente_service, get_client_service, register_client_service

router = APIRouter(prefix="/client", tags=["client"])

@router.post("/create", summary="Registrar nuevo cliente")
def create_client(clientes: clientCreate):
    try:
        client_id = register_client_service(clientes)
        return {"message": "Cliente creado exitosamente", "id_cliente": client_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_client/{id_cliente}", summary="Obtener cliente por ID")
def get_client(id_cliente: int):
    client = get_client_service(id_cliente)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.get("/get_all_client", summary="Obtener todos los clientes")
def get_all_client():
    carts = get_all_cliente_service()
    if carts is None or len(carts) == 0:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    return carts