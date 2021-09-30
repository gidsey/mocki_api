import yaml


def compile_yaml():
    data = {
        "name": "mocki",
        "port": 3000,
        "endpoints":

            [
                {
                    "path": "\hello",
                    "method": "post",
                    "responses": [
                        {
                            "status code": 200,
                            "headers": [{
                                "name": "content-type",
                                "value": "application/json"
                            }],
                            "body": "\|"
                        }
                    ]}
            ]
    }

    content = yaml.dump(data, sort_keys=False)
    with open("../.mocki/config3.yml", "w") as config_file:
        config_file.write(content)

        print("test_yaml \n\n{}".format(data))


if __name__ == "__main__":
    compile_yaml()
