import boto3
import uuid
from app.core.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url = settings.r2_endpoint_url,
    aws_access_key_id = settings.r2_access_key_id,
    aws_secret_access_key = settings.r2_secret_access_key,
)

def upload_image_to_storage(image_bytes: bytes, content_type: str = "image/png") -> str:
    file_key = f"thumbnails/{uuid.uuid4()}.png"

    s3_client.put_object(
        Bucket=settings.r2_bucket_name,
        Key=file_key,
        Body=image_bytes,
        ContentType=content_type,
    )


    return f"{settings.r2_public_url}/{file_key}"