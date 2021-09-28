import yaml


def compile_yaml():

    header = ['a', 'b', 'c']

    head = {
        "name": "mocki",
        "port": 3000,
    }

    yaml_content = yaml.dump(head)

    with open("../.mocki/config3.yml", "w") as config_file:
        config_file.write(yaml_content)

        print('test_yaml \n\n{}'.format(yaml_content))






if __name__ == '__main__':
    # Kick off the program by calling the start_game function.
    compile_yaml()
