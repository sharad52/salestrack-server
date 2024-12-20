from __future__ import annotations
import uvicorn
from salestrackapi import config
from salestrack_utils.addon.databases.console import AlembicCommand


class CliCommand:
    """SalesTrack cli command"""
    def __init__(self) -> None:
        _settings = config.get_application_settings()
        self.alembic = AlembicCommand(_settings)


    def serve(self, host: str = "127.0.0.1", port: int = 8000):
        """Serves the SalesTrack Server/API"""
        uvicorn.run(
            "salestrackapi.main:app",
            host=host,
            port=port,
            log_level="info",
            reload=True
        )