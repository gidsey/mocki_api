import json
import os

from common.constants import DATA_PATH


def get_data_files():
    files = []

    for filename in os.listdir(DATA_PATH):
        try:
            print('filename', filename)
            with open(os.path.join(DATA_PATH, filename)) as f:
                json_data = json.loads(f.read())
            files.append({
                'filename': filename,
                'data': json_data,
            })
        except json.decoder.JSONDecodeError as e:
            print(f'Error in reading json file: {filename}. Error: {str(e)}')

    return files
