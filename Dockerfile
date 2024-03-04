FROM public.ecr.aws/lambda/python:3.12

# Copy requirements.txt
COPY requirements.txt ./requirements.txt

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY ./src ./src

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "src.lambda_handler.lambda_handler" ]