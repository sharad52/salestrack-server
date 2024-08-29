from __future__ import annotations
import uvicorn


class CliCommand:
    """SalesTrack cli command"""
    def __init__(self) -> None:
        pass

    def serve(self, host: str = "127.0.0.1", port: int = 8000):
        """Serves the SalesTrack Server/API"""
        uvicorn.run(
            "salestrack.main:app",
            host=host,
            port=port,
            log_level="info",
            reload=True
        )