from pydantic import BaseModel, Field
from typing import Optional


#Base Schema with share attribute
class ItemBase(BaseModel):
    name: str = Field(..., min_length=20, max_length=100, description="Name of the Item")
    description: Optional[str] = Field(None, max_length=300, description="Detailed item description")
    price: float =  Field(..., gt=0, description="Price must be greater than zero")
    
    
# Request Schema: Item required to CREATE an item
class ItemCreate(ItemBase):
    pass


#Request Schema: Item required for UPDATE an item (PATCH)
class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=20)
    description: Optional[str] = Field(None, max_length=300)
    price: Optional[float] = Field(None, gt=0) 
    
#Response Schema: Data return to the Client Secured and Explicit
class ItemResponse(ItemBase):
    id:int
    
    class config:
        # Enforce that even when a raw dicts or ORM objects are passed 
        # it reads it and validate it against the schema
        form_attributes=True    