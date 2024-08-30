from fastapi import FastAPI
from salestrack.entrypoints.routes import user_routes

app = FastAPI()
app.include_router(user_routes)




@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}