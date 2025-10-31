from fastapi import APIRouter, HTTPException

from Apps.Luxuries.schemas import LuxuryItem, LuxuryItemCreate, LuxuryItemUpdate
from Apps.Luxuries.services import delete_luxury_service, get_item_service, get_luxuries_service, register_luxury_service, update_luxury_service


router = APIRouter(prefix="/luxuries", tags=["Luxuries"])

@router.get("/get_luxuries")
async def get_luxuries():
    try:
        luxuries = get_luxuries_service()
        return luxuries
    except Exception as e:
        # Manejar errores y devolver una respuesta de error 500
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/register_luxury", response_model=LuxuryItem)
async def register_luxury(luxury: LuxuryItemCreate):
    try:
        new_id = register_luxury_service(luxury)
        return LuxuryItem(idProducts=new_id, **luxury.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put('/update_luxury')
async def update_luxury(luxury: LuxuryItemUpdate):
    try:
        response = update_luxury_service(luxury)
        if not response:
            raise HTTPException(status_code=404, detail="Item no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete_item/{idProducts}")
async def delete_luxury(idProducts: int):
    try:
        response = delete_luxury_service(idProducts)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/get_all_item", summary="Obtener todos los items")
def get_all_client():
    item = get_item_service()
    if item is None or len(item) == 0:
        raise HTTPException(status_code=404, detail="No hay items registrados")
    return item