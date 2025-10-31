from pydantic import BaseModel

class clientCreate(BaseModel):
    id_cliente: int
    nombre: str

class clientUpdate(BaseModel):
    id_cliente: int
    nombre: str

class clientDelete(BaseModel):
    id_cliente: int

class clientGet(BaseModel):
    id_cliente: int
    