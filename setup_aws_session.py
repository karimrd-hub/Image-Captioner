import os
from dotenv import load_dotenv
import boto3

def setup_aws_session():
    # Load environment variables from .env
    load_dotenv()

    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION")
    aws_output = os.getenv("AWS_DEFAULT_OUTPUT_FORMAT")

    if not all([aws_access_key_id, aws_secret_access_key, aws_region]):
        raise ValueError("Missing AWS environment variables in .env file")

    # Create a boto3 session (instead of running aws configure manually)
    session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    return session
