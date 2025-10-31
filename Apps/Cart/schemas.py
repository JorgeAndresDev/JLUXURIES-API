from pydantic import BaseModel

class CartItemCreate(BaseModel):
    id_carrito: int
    id_cliente: int
    id_producto: int
    cantidad: int
    subtotal: float
    estado: str

class CartItemUpdate(BaseModel):
    id_producto: int
    cantidad: int
    subtotal: float
    estado: str

class CartItemDelete(BaseModel):
    id_carrito: int
    id_producto: int

class CartItemGet(BaseModel):
    id_carrito: int