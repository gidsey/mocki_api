import json
import os
import yaml

from yaml.representer import SafeRepresenter


class LiteralString(str):
    pass


def change_style(style, representer):
    def new_representer(dumper, data):
        scalar = representer(dumper, data)
        scalar.style = style
        return scalar
    return new_representer


represent_literal_str = change_style('|', SafeRepresenter.represent_str)


yaml.add_representer(LiteralString, represent_literal_str)


def compile_yaml():

    data_path = '/app/data_mocki/'
    files = []
    endpoints = []

    for filename in os.listdir(data_path):
        if not filename.startswith('.'):
            try:
                print('filename', filename)
                with open(os.path.join(data_path, filename)) as f:
                    json_data = json.loads(f.read())
                files.append({
                    'filename': filename,
                    'data': json_data,
                })
            except json.decoder.JSONDecodeError as e:
                print(f'Error in reading json file: {filename}. Error: {str(e)}')

    for item in files:
        path = f'/{item.get("filename").rsplit(".json", 1)[0]}'
        endpoints.append({
            "path": path,
            "method": "post",
            "responses": [
                {
                    "status code": 200,
                    "headers": [{
                        "name": "content-type",
                        "value": "application/json"
                    }],
                    'body': LiteralString(json.dumps(item.get('data')))
                }
            ]
        })

    data = {
        "name": "mocki",
        "port": 3000,
        "endpoints": endpoints
    }

    content = yaml.dump(data, sort_keys=False, default_flow_style=False)
    with open("/app/.mocki/config.yml", "w") as config_file:
        config_file.write(content)

        print('config.yml successfully compiled')
