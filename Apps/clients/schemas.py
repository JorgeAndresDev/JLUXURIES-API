from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    client = "client"
    admin = "admin"

class client(BaseModel):
    id_cliente: Optional[int] = None
    nombre: str
    email: str
    password: str
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    role: RoleEnum = RoleEnum.client

class ClientUpdate(BaseModel):
    id_cliente: Optional[int] = None
    nombre: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    role: Optional[RoleEnum] = None
