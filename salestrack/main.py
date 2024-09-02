from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from salestrack.domain.models import Base
from salestrack.core.config import settings
from salestrack.dbconfig.db_config import database, metadata, engine
from salestrack.entrypoints.routes import user_routes, product_routes



def startup():
    print('Ready to go')

def on_shutdown():
    return "An application has shutdown successfylly."


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    return _app

app = get_application()

#SQLAlchemy define table to db
Base.metadata.create_all(bind=engine)

#Dependency to obtain db session
def get_db():
    db = database.connect()
    try: 
        yield db
    finally: 
        db.disconnect()





app.include_router(user_routes, prefix="/users", tags=["users"])
app.include_router(product_routes, prefix="/products", tags=["products"])



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}