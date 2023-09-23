from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException

from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine



order_router = APIRouter(
    prefix='/order'
)


session=Session(bind=engine)



@order_router.get('/')
async def hello(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Yaroqli access token kiritilmadi")

    return {"message": "Bu orders sahifasi"}




@order_router.post('/make', status_code=status.HTTP_201_CREATED)
async def order_make(order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Yaroqsiz access token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        quantity=order.quantity
    )

    new_order.user = user
    session.add(new_order)
    session.commit()

    data = {
        'success': True,
        'message': "Buyurtma yaratildi."
    }

    return jsonable_encoder(data)









































































































