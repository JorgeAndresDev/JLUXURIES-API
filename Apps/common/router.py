from fastapi import APIRouter, Depends, Query
from typing import List
from Apps.common.schemas import AuditLogWithUser
from Apps.common.services import get_all_logs_service, get_logs_by_user_service
from Apps.auth.auth import get_current_admin, get_current_user


router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"]
)


@router.get("/", response_model=List[AuditLogWithUser])
def get_all_audit_logs(
    limit: int = Query(default=100, ge=1, le=500),
    current_admin: dict = Depends(get_current_admin)
):
    """
    Obtiene todos los logs de auditoría del sistema.
    
    **Requiere:** Token de administrador
    
    **Parámetros:**
    - limit: Cantidad máxima de logs a retornar (1-500, default: 100)
    
    **Retorna:** Lista de logs con información del usuario
    """
    logs = get_all_logs_service(limit=limit)
    return logs


@router.get("/user/{user_id}", response_model=List[AuditLogWithUser])
def get_user_audit_logs(
    user_id: int,
    limit: int = Query(default=50, ge=1, le=200),
    current_user: dict = Depends(get_current_user)
):
    """
    Obtiene los logs de auditoría de un usuario específico.
    
    **Requiere:** Token de usuario autenticado
    
    **Parámetros:**
    - user_id: ID del usuario
    - limit: Cantidad máxima de logs a retornar (1-200, default: 50)
    
    **Retorna:** Lista de logs del usuario especificado
    """
    logs = get_logs_by_user_service(user_id=user_id, limit=limit)
    return logs
