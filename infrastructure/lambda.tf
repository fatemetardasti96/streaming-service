resource "aws_lambda_function" "test_lambda" {
    function_name = "lambda_handler"
    role          = aws_iam_role.iam_for_lambda.arn
    package_type = "Image"
    image_uri = aws_ecr_repository.ecr

}

resource "aws_iam_role" "lambda_execution_role" {
  name = "lambda_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com",
        },
      },
    ],
  })
}

resource "aws_iam_role_policy_attachment" "logs_attachment" {
  policy_arn = aws_iam_policy.cloudwatch_logs_policy.arn
  role       = aws_iam_role.lambda_execution_role.name
}