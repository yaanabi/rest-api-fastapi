from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class ProductBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    category_id: int


class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None

class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

class CategoryBase(BaseModel):
    name: str

class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    products: List[Product] = []

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    name: Optional[str] = None