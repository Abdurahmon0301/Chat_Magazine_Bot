from pydantic import BaseModel
from typing import List, Optional


class Product(BaseModel):
    id: str
    title: str
    price: float
    currency: str = "UZS"
    description: Optional[str] = None
    image_url: Optional[str] = None


class Category(BaseModel):
    slug: str
    title: str
    products: List[Product] = []
