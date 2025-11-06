from pydantic import BaseModel

class client(BaseModel):
    id_cliente: int
    nombre: str
