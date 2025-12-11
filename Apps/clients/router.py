from fastapi import APIRouter, HTTPException, Depends, Request
from Apps.clients.schemas import client, ClientUpdate
from Apps.clients.services import (
    delete_client_service,
    get_all_cliente_service,
    get_client_service,
    register_client_service,
    update_client_service
)
from Apps.auth.auth import get_current_admin
from Apps.common.audit import log_action


router = APIRouter(prefix="/client", tags=["client"])

@router.post("/create", summary="Registrar nuevo cliente (requiere token)")
def create_client(clientes: client, request: Request, current_user: dict = Depends(get_current_admin)):
    try:
        client_id = register_client_service(clientes)
        log_action(
            user_id=current_user["id_cliente"],
            action="CREATE_CLIENT",
            details=f"Created client {clientes.email}",
            ip_address=request.client.host
        )
        return {"message": "Cliente creado exitosamente", "id_cliente": client_id, "usuario": current_user["email"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_client/{id_cliente}", summary="Obtener cliente por ID (requiere token)")
def get_client(id_cliente: int, current_user: dict = Depends(get_current_admin)):
    client = get_client_service(id_cliente)
    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return client

@router.get("/get_all_client", summary="Obtener todos los clientes (requiere token)")
def get_all_client(current_user: dict = Depends(get_current_admin)):
    carts = get_all_cliente_service()
    if carts is None or len(carts) == 0:
        raise HTTPException(status_code=404, detail="No hay clientes registrados")
    return carts

@router.put("/update_client/{id_cliente}", summary="Actualizar cliente por ID (requiere token)")
def update_client(id_cliente: int, Cliente: ClientUpdate, request: Request, current_user: dict = Depends(get_current_admin)):
    try:
        Cliente.id_cliente = id_cliente  
        result = update_client_service(Cliente)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        log_action(
            user_id=current_user["id_cliente"],
            action="UPDATE_CLIENT",
            details=f"Updated client {id_cliente}",
            ip_address=request.client.host
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete_client/{id_cliente}", summary="Eliminar cliente por ID (requiere token)")
def delete_client(id_cliente: int, request: Request, current_user: dict = Depends(get_current_admin)):
    try:
        response = delete_client_service(id_cliente)
        log_action(
            user_id=current_user["id_cliente"],
            action="DELETE_CLIENT",
            details=f"Deleted client {id_cliente}",
            ip_address=request.client.host
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

