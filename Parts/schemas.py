# app/schemas.py
from pydantic import BaseModel, constr, conint

class Part(BaseModel):
    Part_id: int
    name: constr(min_length=2, max_length=50)
    model_car: constr(min_length=2, max_length=50)
    year: conint(gt=18)
