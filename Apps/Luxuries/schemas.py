from pydantic import BaseModel

class LuxuryItemCreate(BaseModel):
    ProductsName: str
    Quantity: int
    Price: float
    color: str

class LuxuryItemUpdate(BaseModel):
    idProducts: int
    ProductsName: str
    Quantity: int
    Price: float
    color: str

class LuxuryItem(LuxuryItemCreate):
    idProducts: int
