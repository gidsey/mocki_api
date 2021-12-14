import os
import random
import string
import boto3
import requests

from botocore.exceptions import ClientError
from io import BytesIO
from PIL import Image
from requests.structures import CaseInsensitiveDict

from common.constants import (
    AWS_S3_REGION_NAME,
    AWS_S3_ENDPOINT_URL,
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_BUCKET_NAME,
)

headers = CaseInsensitiveDict()
headers["Accept"] = "*/*"
headers["User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6)"


def generate_id(size=7, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def append_id(filename):
    name, ext = os.path.splitext(filename)
    return "{name}-{uid}{ext}".format(name=name, uid=generate_id(), ext=ext)


def get_boto_s3_client():
    return boto3.client(service_name='s3',
                        region_name=AWS_S3_REGION_NAME,
                        endpoint_url=AWS_S3_ENDPOINT_URL,
                        aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


def get_image(url):
    try:
        response = requests.get(url=url, timeout=5, headers=headers, stream=True)
        if not response.headers['content-type'].lower().startswith('image/'):
            response.connection.close()
            return None
    except Exception as e:
        print(f'Error in get_image: {str(e)}')
        return None

    if response.status_code == requests.codes.ok:
        image = Image.open(BytesIO(response.content))
        return image


def convert_image_to_jpg(image, key):
    try:
        image_format = image.format.lower()
        if image_format != 'jpeg' and image_format != 'jpg':
            image = image.convert('RGB')
            filename = key.rsplit('.', 1)[0]
            key = f'{filename}.jpeg'
    except Exception as e:
        print(f'Error in convert_image_to_jpg: {str(e)}')

    return image, key


def upload_to_s3(merchant, image, key):
    try:
        client = get_boto_s3_client()

        # create folder and filename, create folder if merchant doesn't already exist
        merchant = merchant.lower().replace(' ', '_')
        key = key.rsplit('?', 1)[0].replace('?', '')
        location = f'mocki/{merchant}/{key}'

        # if filename already exists, add unique id to avoid overwriting
        exists = True
        while exists:
            try:
                exists = client.head_object(Bucket=AWS_BUCKET_NAME, Key=location)
                location = append_id(location)
            except ClientError:
                exists = False

        # create in-memory image file
        in_mem_file = BytesIO()
        image.save(in_mem_file, format=image.format)
        in_mem_file.seek(0)

        # upload to S3
        client.upload_fileobj(
            in_mem_file,
            AWS_BUCKET_NAME,
            location,
            ExtraArgs={
                'ContentType': 'image',
                'ACL': 'public-read'
            }
        )

        aws_path = AWS_S3_ENDPOINT_URL.split('https://', 1)[1]
        location = f'https://{AWS_BUCKET_NAME}.{aws_path}/{location}'

        return location

    except Exception as e:
        print(f'Error in upload_to_s3: {str(e)}')
