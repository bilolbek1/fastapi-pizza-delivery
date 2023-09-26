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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    return {"message": "It is orders page"}




@order_router.post('/make', status_code=status.HTTP_201_CREATED)
async def order_make(order: OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        quantity=order.quantity
    )

    new_order.user = user
    session.add(new_order)
    session.commit()

    data = {
        "id":new_order.id,
        "user_id": new_order.user_id,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status,
        "pizza_size": new_order.pizza_size
    }

    response = {
        "success": True,
        "message": "Order has been created",
        "data":data
    }

    return jsonable_encoder(response)




@order_router.get('/list')
async def order_list(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()
        custom_data = [
            {
                "id": i.id,
                "user_id": i.user_id,
                "quantity": i.quantity,
                "order_status": i.order_status,
                "pizza_size": i.pizza_size
            }
            for i in orders
        ]

        return jsonable_encoder(custom_data)

    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="User not allowed to carry out request")




@order_router.get('/detail/{id}')
async def order_detail(id:int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()

        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not allowed to carry out request")




@order_router.get('/user/orders')
async def user_s_order(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")


    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()


    return jsonable_encoder(user.order)




@order_router.get("/user/orders/{id}")
async def user_s_order_id(id:int, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")


    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    order = user.order

    for i in order:
        if i.id==id:
            return jsonable_encoder(i)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="This order i none")




@order_router.put('/update/{id}')
async def user_order_update(id:int, order:OrderModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    update_order = session.query(Order).filter(Order.id == id).first()

    if update_order.user == user:
        update_order.quantity = order.quantity
        update_order.order_status = order.order_status
        update_order.pizza_size = order.pizza_size

        session.commit()

        data = {
            "id": order.id,
            "quantity": order.quantity,
            "user_id": order.user_id,
            "order_status": order.order_status,
            "pizza_size": order.pizza_size
        }

        return jsonable_encoder(data)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="It is not your order")




@order_router.delete('/delete/{id}')
async def user_order_delete(id:int, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    delete_order = session.query(Order).filter(Order.id == id).first()

    if delete_order.user == user:
        session.delete(delete_order)

        session.commit()

        return jsonable_encoder(delete_order)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="It is not your order")























































































