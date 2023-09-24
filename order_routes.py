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




@order_router.get('/list')
async def order_list(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Yaroqsiz access token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()
        for i in orders:
            response={
                "id": i.id,
                "user_id": i.user_id,
                "quantity": i.quantity,
                "product_id": i.product_id,
                "order_status": i.order_status
            }

            return jsonable_encoder(response)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Bu sahifa faqat super userlar uchun")








































































































