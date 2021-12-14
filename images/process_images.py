import json

from common.constants import AWS_BUCKET_NAME
from images.data_utils import get_data_files
from images.image_utils import get_image, convert_image_to_jpg, upload_to_s3


def process_images(path):
    # loop through json files in supplied data folder
    files = get_data_files(path=path)

    # for each json file, loop through contents and find merchant and image keys
    for file in files:
        filename = file.get('filename')
        data = file.get('data')

        find_and_process_images(data)

        # save json file with new data
        with open(f'{path}{filename}', 'w') as outfile:
            json.dump(data, outfile, indent=4)


# recursive function for variable data and key structure
def find_and_process_images(d, merchant=''):
    if isinstance(d, list):
        for i, v in enumerate(d):
            if isinstance(v, dict):
                find_and_process_images(v, merchant)
            elif isinstance(v, str):
                d[i] = process_image(v, merchant)

    elif isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, str):
                if k == 'merchant' or k == 'merchant_name_norm':
                    merchant = v

        for k, v in d.items():
            if isinstance(v, dict) or isinstance(v, list):
                find_and_process_images(v, merchant)
            elif isinstance(v, str):
                d[k] = process_image(v, merchant)


def process_image(v, merchant):
    if merchant and v.startswith('http'):
        image_url = v

        # if image is not on S3, download via requests
        if not image_url.startswith(f'https://{AWS_BUCKET_NAME}'):
            image = get_image(image_url)

            if image:
                key = image_url.rsplit('/', 1)[1]

                # if image is not jpg, convert to jpg
                image, key = convert_image_to_jpg(image, key)

                # transfer to S3
                location = upload_to_s3(merchant, image, key)

                print('new location', location)

                # update json image reference in data
                if location:
                    return location
    return v
