import json
import os


def get_data_files(path):
    files = []

    for filename in os.listdir(path):
        if not filename.startswith('.'):
            try:
                print('filename', filename)
                with open(os.path.join(path, filename)) as f:
                    json_data = json.loads(f.read())
                files.append({
                    'filename': filename,
                    'data': json_data,
                })
            except json.decoder.JSONDecodeError as e:
                print(f'Error in reading json file: {filename}. Error: {str(e)}')

    return files
