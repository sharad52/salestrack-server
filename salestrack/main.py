from fastapi import FastAPI
from salestrack.entrypoints.routes import user_routes, product_routes

def startup():
    print('Ready to go')

def on_shutdown():
    return "An application has shutdown successfylly."

app = FastAPI(
    debug=False,
    on_startup=[startup],
    on_shutdown=[on_shutdown]
)

app.include_router(user_routes, prefix="/users", tags=["users"])
app.include_router(product_routes, prefix="/products", tags=["products"])



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}