from pydantic import BaseModel, validator
from typing import Optional

class SignUpModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                "username": "Johndoe",
                "email": "john@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True
            }
        }



class Settings(BaseModel):
    authjwt_secret_key: str = '026d4ba87f0894157b41e1ff68d7eb53d9e8a4e9a2b5fd8d9de8cf0ab98fabe0'




class LoginModel(BaseModel):
    username_or_email: str
    password: str



class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_status: Optional[str] = 'PENDING'
    pizza_size: Optional[str] = 'SAMLL'
    user_id: Optional[int]

    class Config:
        orm_mode = True
        arbitrary_types_allowed = {
            "example": {
                "quantity": 2
            }
        }



class OrderStatusModel(BaseModel):
    order_status: Optional[str] = 'PENDING'

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                "order_status": "PENDING"
            }
        }






























































