from fastapi import APIRouter

user_routes = APIRouter(
    prefix='/users',
    tags=['Users']
)

@user_routes.get('/')
async def load_user():
    return {"message": "User Route Loaded successfully."}