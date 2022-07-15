from typing import List, Union

from pydantic import BaseModel


class VUZBase(BaseModel):    
    name: str
    avg_rate_free: float
    avg_rate_paid: float
    count_free_place: float
    count_paid_place: float
    city: str

class VUZCreate(VUZBase):
    pass

class VUZ(VUZBase):  
    id: int 

    class Config:
        orm_mode = True
