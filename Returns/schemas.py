# app/schemas.py
from pydantic import BaseModel, constr, conint

class Return(BaseModel):
    Return_id: int
    ProductName: constr(min_length=2, max_length=50)
    model_car: constr(min_length=2, max_length=50)
    
#If you checkout u will be given a reutn_id if needed to return product and then if u register for a return u will be given instructions on what to do.