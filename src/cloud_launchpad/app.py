"""HTTP API. For now: liveness and a view of which AWS resources the service is wired to."""

from typing import Annotated

from fastapi import Depends, FastAPI
from pydantic import BaseModel

from cloud_launchpad import __version__
from cloud_launchpad.config import Settings, get_settings


class Health(BaseModel):
    status: str
    version: str


class Info(BaseModel):
    region: str
    uploads_bucket: str
    jobs_queue: str
    target: str


def create_app() -> FastAPI:
    app = FastAPI(title="Cloud Launchpad", version=__version__)

    @app.get("/health")
    def health() -> Health:
        return Health(status="ok", version=__version__)

    @app.get("/info")
    def info(settings: Annotated[Settings, Depends(get_settings)]) -> Info:
        # Resource names only. Credentials never leave the process.
        return Info(
            region=settings.aws_region,
            uploads_bucket=settings.uploads_bucket,
            jobs_queue=settings.jobs_queue,
            target="localstack" if settings.uses_localstack else "aws",
        )

    return app


app = create_app()
