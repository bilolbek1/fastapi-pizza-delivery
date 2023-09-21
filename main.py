from fastapi import FastAPI
import auth_routes, order_routes
from fastapi_jwt_auth import AuthJWT
from schemas import Settings


app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_routes.auth_router)
app.include_router(order_routes.order_router)

@app.get('/')
async def root():
    return {'message': 'Salom FastApi!'}
