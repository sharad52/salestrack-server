from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from salestrack_utils.auth.entrypoints import users
from salestrack_utils.addon.databases.bootstrap import init_database

from salestrackapi import config
from salestrackapi.service_layer import services


def create_app(settings: config.AppSettings) -> FastAPI:
    db = init_database(settings)

    app = FastAPI(
        title="Salestrack",
        debug=settings.debug,
        on_startup=[db.init_db],
        on_shutdown=[db.disconnect]
    )
    # setting db in app state
    app.state.db = db.connect()
    app.state.settings = settings
    return app

app = create_app(config.get_application_settings())

app.include_router(services.router)
app.include_router(users.router)

