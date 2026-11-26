output "uploads_bucket" {
  description = "Name of the uploads bucket."
  value       = aws_s3_bucket.uploads.bucket
}

output "jobs_queue_url" {
  description = "URL of the jobs queue."
  value       = aws_sqs_queue.jobs.id
}

output "jobs_dlq_url" {
  description = "URL of the dead-letter queue."
  value       = aws_sqs_queue.jobs_dlq.id
}
