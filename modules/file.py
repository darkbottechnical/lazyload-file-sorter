import os
from modules.parse import parse_config, Conf

CONFIG: Conf = parse_config()

class File:
    def __init__(self, name):
        self.name = name
        self.ext = os.path.splitext(name)[1].lstrip(".")
        self.path = os.path.abspath(os.path.join(CONFIG.DIRTOSORT, name))
        