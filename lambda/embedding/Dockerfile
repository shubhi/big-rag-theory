# Use the Amazon Lambda Python runtime base image
FROM public.ecr.aws/lambda/python:3.10

# Copy your function code to the container
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/

# Copy the requirements file and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the command to run your Lambda function
CMD ["lambda_function.lambda_handler"]