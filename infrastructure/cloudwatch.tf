resource "aws_cloudwatch_log_group" "kinesislog" {
  name = "kinesis-log"
}

resource "aws_cloudwatch_event_rule" "analytical-load" {
  name        = "load-analytical-events"
  description = "Stores analytical events into S3"

  schedule_expression = "cron(0, 0, *, *, ?, *)"
}

resource "aws_cloudwatch_event_target" "sns" {
  rule      = aws_cloudwatch_event_rule.analytical-load.name
  target_id = "SendToSNS"
  arn       = aws_sns_topic.aws_logins.arn
}
