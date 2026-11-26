from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from cloud_launchpad import __version__
from cloud_launchpad.app import create_app
from cloud_launchpad.config import Settings, get_settings


@pytest.fixture
def client() -> Iterator[TestClient]:
    app = create_app()
    app.dependency_overrides[get_settings] = lambda: Settings(
        aws_region="eu-west-1",
        aws_endpoint_url=None,
        uploads_bucket="test-uploads",
        jobs_queue="test-jobs",
    )
    with TestClient(app) as test_client:
        yield test_client


def test_health_reports_ok_and_version(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "version": __version__}


def test_info_shows_wired_resources_and_target(client: TestClient) -> None:
    response = client.get("/info")

    assert response.status_code == 200
    assert response.json() == {
        "region": "eu-west-1",
        "uploads_bucket": "test-uploads",
        "jobs_queue": "test-jobs",
        "target": "aws",
    }


def test_info_never_exposes_credentials(client: TestClient) -> None:
    body = client.get("/info").text.lower()

    assert "secret" not in body
    assert "access_key" not in body
