from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from salestrack_utils.auth.entrypoints import users

from salestrackapi.domain.models import Base
from salestrackapi.config import settings
from salestrackapi.dbconfig.db_config import engine
from salestrackapi.service_layer import services



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


app.include_router(services.router)
app.include_router(users.router)

