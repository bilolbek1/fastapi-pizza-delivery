from fastapi import APIRouter, status
from database import Session, engine
from schemas import SignUpModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash



auth_router = APIRouter(
    prefix='/auth'
)



session = Session(bind=engine)




@auth_router.get('/')
async def hello():
    return {'messgae': "Hello Auth routes"}



@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Bu email bilan ro'yxatdan o'tib bo'lingan")

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="Bu username bilan ro'yxatdan ot'ib bo'lingan")

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active

    )

    session.add(new_user)

    session.commit()



    data={
        "id": new_user.id,
        "username":new_user.username,
        "email": new_user.email,
        "password": new_user.password,
        "is_staff": new_user.is_staff,
        "is_active": new_user.is_active
    }

    response={
        "success": True,
        "status": status.HTTP_200_OK,
        "message": "Siz muvaffaqiyatli ro'yxatdan o'tdingiz",
        "data": data
    }
    return response

























































































