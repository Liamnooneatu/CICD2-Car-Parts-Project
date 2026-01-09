from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, StringConstraints, ConfigDict



class Part(BaseModel):
    Part_id: int = Field(..., ge=1)
    name: str = Field(..., min_length=1)
    price: float = Field(..., ge=0)
    stock: int = Field(..., ge=0)
    model_car: str = Field(..., min_length=1)
    year: int = Field(..., ge=1900, le=2100)
