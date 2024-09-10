from contextlib import asynccontextmanager

from fastapi import FastAPI
from structlog import get_logger
from starlette.middleware.cors import CORSMiddleware

from auth.entrypoints import users

from salestrack.domain.models import Base
from salestrack.core.config import settings
from salestrack.dbconfig.db_config import engine
from salestrack.service_layer import services
from salestrack.core.settings import get_app_settings

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading application lifespan objects.")

    #bootstrap settings
    settings = get_app_settings()
    app.state.settings = settings

    #bootstrap database
    # TODO: bootstrap postgresql client 

    logger.info("Unloading application lifespan objects.")



def startup():
    print('Ready to go')

def on_shutdown():
    return "An application has shutdown successfylly."


def get_application():
    _app = FastAPI(title="SalesTrack", lifespan=lifespan)

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

