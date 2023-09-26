from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
import datetime



auth_router = APIRouter(
    prefix='/auth'
)



session = Session(bind=engine)




@auth_router.get('/')
async def hello(Auyhorize: AuthJWT=Depends()):
    try:
        Auyhorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid token')
    return {'messgae': "Hello this is auth routes page"}



@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the email already exists")

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with the username already exists")

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
        "message": "you have successfully registered",
        "data": data
    }
    return response




@auth_router.post('/login', status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT=Depends()):

    # db_user = session.query(User).filter(User.username == user.username).first()


    db_user = session.query(User).filter(
        or_(User.username == user.username_or_email,
            User.email == user.username_or_email
            )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_limit_time = datetime.timedelta(minutes=60)
        refresh_limit_time = datetime.timedelta(days=5)

        access_token = Authorize.create_access_token(subject=db_user.username,
                                                     expires_time=access_limit_time)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username,
                                                       expires_time=refresh_limit_time)


        token = {
            "access_token": access_token,
            "refrsh_token": refresh_token
        }

        response = {
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "you have successfully logged in",
            "token": token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid username or password")





@auth_router.get('/login/refresh')
async def refresh(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()

        db_user = session.query(User).filter(User.username == current_user).first()

        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="This user not found")

        access_limit_time = datetime.timedelta(minutes=60)
        new_access_token = Authorize.create_access_token(subject=db_user.username,
                                                         expires_time=access_limit_time)

        response = {
            "success": True,
            "status": 200,
            "message": "Get new access token",
            "token": new_access_token
        }

        return response

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid refresh token")















































































