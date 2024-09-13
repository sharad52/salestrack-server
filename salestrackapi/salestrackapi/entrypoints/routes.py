from fastapi import APIRouter
from salestrackapi.service_layer.services import load_user

user_routes = APIRouter(
    prefix='/users',
    tags=['Users']
)

product_routes = APIRouter(
    prefix="/products",
    tags=["products"]
)

@user_routes.get('/')
async def load_user():
    return {"message": "User Route Loaded successfully."}