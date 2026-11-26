# Targets LocalStack by default, so `terraform apply` needs no AWS account.
# The static "test" credentials are LocalStack's convention, not real secrets.
# To deploy to real AWS, set use_localstack = false and supply credentials the
# usual way (environment, profile or OIDC in CI).
provider "aws" {
  region = var.region

  access_key                  = var.use_localstack ? "test" : null
  secret_key                  = var.use_localstack ? "test" : null
  skip_credentials_validation = var.use_localstack
  skip_metadata_api_check     = var.use_localstack
  skip_requesting_account_id  = var.use_localstack
  s3_use_path_style           = var.use_localstack

  endpoints {
    s3  = var.use_localstack ? var.localstack_endpoint : null
    sqs = var.use_localstack ? var.localstack_endpoint : null
  }

  default_tags {
    tags = {
      project    = var.project
      managed_by = "terraform"
    }
  }
}
