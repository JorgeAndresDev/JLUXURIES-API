from fastapi import APIRouter, HTTPException
from Apps.clients.schemas import client
from Apps.clients.services import delete_client_service, get_all_cliente_service, get_client_service, register_client_service, update_client_service

router = APIRouter(prefix="/client", tags=["client"])

@router.post("/create", summary="Registrar nuevo cliente")
def create_client(clientes: client):
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

@router.put("/update_client/{id_cliente}", summary="Actualizar cliente por ID")
def update_client(id_cliente: int, Cliente: client):
    try:
        Cliente.id_cliente = id_cliente  
        result = update_client_service(Cliente)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_client/{id_cliente}", summary="Eliminar cliente por ID")
async def delete_cart(id_cliente: int):
    try:
        response = delete_client_service(id_cliente)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))