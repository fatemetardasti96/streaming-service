resource "aws_s3_bucket" "s3" {
  bucket = "babbel-events-bucket-76549876"
}

resource "aws_s3_bucket" "analytical-s3" {
  bucket = "babbel-analytical-bucket-76549876"
}