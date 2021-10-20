import json

from common.constants import DATA_PATH, AWS_BUCKET_NAME
from images.data_utils import get_data_files
from images.image_utils import get_image, convert_image_to_jpg, upload_to_s3


def process_images():
    # loop through json files in data folder
    files = get_data_files()

    # for each json file, loop through contents and find merchant and image keys
    for file in files:
        filename = file.get('filename')
        data = file.get('data')
        changed = False

        for product in data.get('products'):
            merchant = product.get('merchant')
            image_url = product.get('image')
            key = image_url.rsplit('/', 1)[1]

            # if image is not on S3, download via requests
            if not image_url.startswith(f'https://{AWS_BUCKET_NAME}'):
                image = get_image(image_url)

                if image:

                    # if image is not jpg, convert to jpg
                    image, key = convert_image_to_jpg(image, key)

                    # transfer to S3
                    location = upload_to_s3(merchant, image, key)

                    print('new location', location)

                    # update json image reference in data
                    product['image'] = location
                    changed = True

        # if any changes, save json file with new data
        if changed:
            with open(f'{DATA_PATH}{filename}', 'w') as outfile:
                json.dump(data, outfile, indent=4)
