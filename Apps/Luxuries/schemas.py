from pydantic import BaseModel
from typing import Optional

class LuxuryItemCreate(BaseModel):
    ProductsName: str
    moto: str
    categoria: str
    Quantity: int
    Price: float
    color: str
    Description: str
    image_url: Optional[str] = None


class LuxuryItemUpdate(BaseModel):
    ProductsName: Optional[str] = None
    moto: Optional[str] = None
    categoria: Optional[str] = None
    Quantity: Optional[int] = None
    Price: Optional[float] = None
    color: Optional[str] = None
    Description: Optional[str] = None
    image_url: Optional[str] = None

class LuxuryItem(LuxuryItemCreate):
    idProducts: int
