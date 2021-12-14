from common.constants import DATA_PATH
from compiler.importer import compile_yaml
from images.process_images import process_images


process_images(path=DATA_PATH)
compile_yaml()
