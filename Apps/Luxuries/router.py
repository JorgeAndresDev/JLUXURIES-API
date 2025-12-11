from fastapi import APIRouter, HTTPException, Depends, Request
from Apps.auth.auth import get_current_admin
from Apps.common.audit import log_action

from Apps.Luxuries.schemas import LuxuryItem, LuxuryItemCreate, LuxuryItemUpdate
from Apps.Luxuries.services import delete_luxury_service, get_item_service, get_luxuries_service, register_luxury_service, update_luxury_service


router = APIRouter(prefix="/luxuries", tags=["Luxuries"])

@router.get("/get_luxuries")
async def get_luxuries():
    try:
        luxuries = get_luxuries_service()
        return luxuries
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/register_luxury", response_model=LuxuryItem)
async def register_luxury(luxury: LuxuryItemCreate, request: Request, current_user: dict = Depends(get_current_admin)):
    try:
        new_id = register_luxury_service(luxury)
        log_action(
            user_id=current_user["id_cliente"],
            action="CREATE_PRODUCT",
            details=f"Created product {luxury.ProductsName}",
            ip_address=request.client.host
        )
        return LuxuryItem(idProducts=new_id, **luxury.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/update_luxury/{idProducts}')
async def update_luxury(idProducts: int, luxury: LuxuryItemUpdate, request: Request, current_user: dict = Depends(get_current_admin)):
    try:
        response = update_luxury_service(idProducts, luxury)
        if not response:
            raise HTTPException(status_code=404, detail="Item no encontrado")
        log_action(
            user_id=current_user["id_cliente"],
            action="UPDATE_PRODUCT",
            details=f"Updated product {idProducts}",
            ip_address=request.client.host
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete_item/{idProducts}")
async def delete_luxury(idProducts: int, request: Request, current_user: dict = Depends(get_current_admin)):
    try:
        response = delete_luxury_service(idProducts)
        log_action(
            user_id=current_user["id_cliente"],
            action="DELETE_PRODUCT",
            details=f"Deleted product {idProducts}",
            ip_address=request.client.host
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_item/{idProducts}", summary="Obtener item")
def get_item(idProducts: int):
    item = get_item_service(idProducts)  # Ya recibe el int directamente
    if item is None:  # Simplificar la validación
        raise HTTPException(status_code=404, detail="Item no encontrado")
    return item