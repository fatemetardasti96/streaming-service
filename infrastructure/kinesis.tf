resource "aws_kinesis_stream" "stream" {
  name             = "kinesis-stream"
  retention_period = 24 # Length of time data records are accessible after they are added to the stream.

  shard_level_metrics = [ # metrics visible to monitor in cloudwatch
    "IncomingBytes",
    "OutgoingBytes",
  ]
stream_mode_details {
    stream_mode = "ON_DEMAND" # on-demand automatically scales and requires no planning
  }
}

resource "aws_iam_role" "kinesis_role" {
  name = "KinesisRole"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = [
                    "firehose.amazonaws.com",
                    "kinesis.amazonaws.com"]
        }
      }
    ]
  })
}

resource "aws_iam_policy" "cloudwatch_logs_policy" {
  name        = "CloudWatchLogsPolicy"
  description = "Policy for CloudWatch Logs to log Kinesis stream"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "cloudwatch_logs_attachment" {
  policy_arn = aws_iam_policy.cloudwatch_logs_policy.arn
  role       = aws_iam_role.kinesis_role.name
}


resource "aws_kinesis_firehose_delivery_stream" "extended_s3_stream" {
  name        = "terraform-kinesis-firehose-extended-s3-stream"
  destination = aws_s3_bucket.s3.bucket

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn

    dynamic_partitioning_configuration {
      enabled = "true"
    }

    prefix              = "events/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/"
    error_output_prefix = "errors/year=!{timestamp:yyyy}/month=!{timestamp:MM}/day=!{timestamp:dd}/hour=!{timestamp:HH}/!{firehose:error-output-type}/"

    processing_configuration {
      enabled = "true"

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.lambda_processor.arn}:$LATEST"
        }
      }
    }

  }

  kinesis_source_configuration {
    kinesis_stream_arn = aws_kinesis_stream.stream.arn
    role_arn = aws_iam_role.kinesis_role.arn
  }
}