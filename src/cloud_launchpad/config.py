"""Typed settings, read from LAUNCHPAD_* environment variables.

Defaults target LocalStack on localhost so the service runs with no AWS account.
Point it at real AWS by setting LAUNCHPAD_AWS_ENDPOINT_URL to an empty string.
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="LAUNCHPAD_", frozen=True)

    aws_region: str = "us-east-1"
    aws_endpoint_url: str | None = "http://localhost:4566"
    uploads_bucket: str = "cloud-launchpad-uploads"
    jobs_queue: str = "cloud-launchpad-jobs"

    @field_validator("aws_endpoint_url", mode="before")
    @classmethod
    def blank_means_real_aws(cls, value: object) -> object:
        """An empty endpoint means "use the real AWS endpoints", so normalise it to None."""
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def uses_localstack(self) -> bool:
        return self.aws_endpoint_url is not None


@lru_cache
def get_settings() -> Settings:
    return Settings()
