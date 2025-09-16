from pydantic import BaseModel,EmailStr
from typing import Optional


class Role(BaseModel):
   role:str

class UserLogin(BaseModel):
  username:str
  password: str

class UserRegister(UserLogin):
  email:EmailStr


class UserOut(BaseModel):
  username:str
  email:EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None


class Product(BaseModel):
   name:str
   price:float
   quantity_available:int

class AddToCart(BaseModel):
   name:str
   quantity:int
  