from fastapi import APIRouter, HTTPException

from Apps.Cart.schemas import CartItemCreate, CartItemUpdate
from Apps.Cart.services import delete_cart_service, get_cart_service, register_cart_service, update_cart_service


router = APIRouter(prefix="/Cart", tags=["Cart"])

@router.post("/create")
def create_cart_item(carrito: CartItemCreate):
    try:
        cart_id = register_cart_service(carrito)
        return {"message": "Carrito creado exitosamente", "id_carrito": cart_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_cart", summary="Obtener todos los carritos")
def get_cart():
    carts = get_cart_service()
    if carts is None or len(carts) == 0:
        raise HTTPException(status_code=404, detail="No hay carritos registrados")
    return carts

@router.put("/update_cart", summary="Actualizar carrito existente")
def update_cart(cart: CartItemUpdate):
    result = update_cart_service(cart)
    if "Error" in result.get("mensaje", ""):
        raise HTTPException(status_code=400, detail=result["mensaje"])
    return result

@router.delete("/delete_cart/{id_carrito}", summary="Eliminar carrito por ID")
async def delete_cart(id_carrito: int):
    try:
        response = delete_cart_service(id_carrito)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
