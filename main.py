from fastapi import FastAPI
import auth_routes, order_routes

app = FastAPI()

app.include_router(auth_routes.auth_router)
app.include_router(order_routes.order_router)

@app.get('/')
async def root():
    return {'message': 'Salom FastApi!'}
