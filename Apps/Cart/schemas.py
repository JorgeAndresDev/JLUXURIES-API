from pydantic import BaseModel
from typing import Optional

class CartItemCreate(BaseModel):
    id_cliente: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    estado: str = 'activo'

class CartItemUpdate(BaseModel):
    id_carrito: int
    cantidad: int
    precio_unitario: float
    estado: str = 'activo'

class CartItem(BaseModel):
    id_carrito: int
    id_cliente: int
    id_producto: int
    cantidad: int
    precio_unitario: float
    subtotal: float
    estado: str