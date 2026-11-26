import re
from pathlib import Path

import pytest

from cloud_launchpad.config import Settings


def test_defaults_target_localstack(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("AWS_REGION", "AWS_ENDPOINT_URL", "UPLOADS_BUCKET", "JOBS_QUEUE"):
        monkeypatch.delenv(f"LAUNCHPAD_{name}", raising=False)

    settings = Settings()

    assert settings.aws_endpoint_url == "http://localhost:4566"
    assert settings.uses_localstack


def test_reads_prefixed_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LAUNCHPAD_UPLOADS_BUCKET", "from-env")
    monkeypatch.setenv("LAUNCHPAD_AWS_REGION", "us-west-2")

    settings = Settings()

    assert settings.uploads_bucket == "from-env"
    assert settings.aws_region == "us-west-2"


@pytest.mark.parametrize("blank", ["", "   "])
def test_blank_endpoint_means_real_aws(monkeypatch: pytest.MonkeyPatch, blank: str) -> None:
    monkeypatch.setenv("LAUNCHPAD_AWS_ENDPOINT_URL", blank)

    settings = Settings()

    assert settings.aws_endpoint_url is None
    assert not settings.uses_localstack


def _terraform_project_default() -> str:
    variables = (Path(__file__).parents[1] / "infra" / "terraform" / "variables.tf").read_text()
    block = re.search(r'variable "project" \{(.*?)\n\}', variables, re.DOTALL)
    assert block, 'variable "project" not found in variables.tf'
    default = re.search(r'default\s*=\s*"([^"]+)"', block.group(1))
    assert default, 'variable "project" has no default'
    return default.group(1)


def test_defaults_match_terraform_names() -> None:
    # Terraform names resources "${var.project}-uploads" and "${var.project}-jobs".
    # If either side is renamed alone, the service would look for resources that don't exist.
    project = _terraform_project_default()
    settings = Settings(aws_endpoint_url=None)

    assert settings.uploads_bucket == f"{project}-uploads"
    assert settings.jobs_queue == f"{project}-jobs"
