from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from schemas import OrderModel, OrderStatusModel




order_router = APIRouter(
    prefix='/order'
)

@order_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Yaroqli access token kiritilmadi")
    return {'messgae': "Hello Order routers"}