from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List

'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

ShopName='PyShop'

class User(BaseModel):
    id: int = Field(..., description="Unique identifier for user")
    name: str = Field(..., description="Name of user")
    email: EmailStr = Field(..., description="Users email address")

    @field_validator('id')
    def check_non_negative(cls, v):
        if v < 0:
            raise ValueError('id cannot be negative')
        return v

class Item(BaseModel):
    item_id: int = Field(..., description="The unique ID of the item")
    name: str = Field(..., description="The name of the item")
    brand: str = Field(..., description="The brand of the item")
    price: float = Field(..., description="The price of the item, must be non-negative")
    quantity: int = Field(..., description="The quantity of the item, must be non-negative")

    @field_validator('item_id', 'price', 'quantity')
    def check_non_negative(cls, v, info):
        if v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v

class Basket(BaseModel):
    id: int = Field(..., description="Unique identifier for basket")
    user_id: int = Field(..., description="Basket owner id")
    items: List[Item] = Field(default_factory=list, description="List of Items in Basket")

    @field_validator('id', 'user_id')
    def check_non_negative(cls, v, info):
        if v < 0:
            raise ValueError(f"{info.field_name} cannot be negative")
        return v