from pydantic import BaseModel, Field, validator
from typing import Optional

class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    stock: int

class OrderCreateSchema(BaseModel):
    customer_name: str = Field(..., min_length=2, max_length=50)
    product_id: int
    quantity: int = Field(..., gt=0, le=10) # Max 10 items per order
    shipping_address: str = Field(..., min_length=10)

    @validator('customer_name')
    def name_must_be_alpha(cls, v):
        if not all(x.isalpha() or x.isspace() for x in v):
            raise ValueError('Name must only contain letters and spaces')
        return v