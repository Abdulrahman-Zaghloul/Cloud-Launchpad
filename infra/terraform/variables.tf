variable "project" {
  description = "Name prefix for every resource. The service's default settings expect cloud-launchpad."
  type        = string
  default     = "cloud-launchpad"

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9-]{2,40}$", var.project))
    error_message = "project must be 3-41 lowercase letters, digits or hyphens, starting with a letter or digit."
  }
}

variable "region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "use_localstack" {
  description = "Point the provider at LocalStack instead of real AWS."
  type        = bool
  default     = true
}

variable "localstack_endpoint" {
  description = "LocalStack edge endpoint."
  type        = string
  default     = "http://localhost:4566"
}

variable "job_visibility_timeout_seconds" {
  description = "How long a job message stays hidden while a worker processes it. Must exceed the worker's timeout."
  type        = number
  default     = 60
}

variable "max_receive_count" {
  description = "Failed deliveries before a job message moves to the dead-letter queue."
  type        = number
  default     = 5

  validation {
    condition     = var.max_receive_count >= 1 && var.max_receive_count <= 1000
    error_message = "max_receive_count must be between 1 and 1000."
  }
}
