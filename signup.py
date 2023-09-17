from fastapi import APIRouter, status
from models import User
from schemes import SignUpModel
from database import session, engine
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash


session = session(bind=engine)

auth_router = APIRouter(
    prefix='/auth'
)


@auth_router.get('/')
async def signup():
    return {'message': "Welcome to signup page."}



@auth_router.post('/signup')
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this email already exist')

    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail='User with this username already exist')


    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_staff=user.is_staff,
        is_active=user.is_active
    )

    session.add(new_user)
    session.commit()

    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
    }

    response = {
        'success': True,
        'status': status.HTTP_201_CREATED,
        'message': 'You have successfully signed up',
        'data': data
    }
    return response


























