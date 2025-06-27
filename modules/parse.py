import json

class Conf:
    def __init__(self, root_path: str, sort_path, branch_paths: dict, overrides: dict, filetype_matching: dict):
        self.ROOTDIR = root_path
        self.DIRTOSORT = sort_path
        self.branches = branch_paths
        self.else_path = self.branches.get("else")
        self.overrides = overrides
        self.filetype_matching = filetype_matching

def parse_config():
    with open("config.json", "r", encoding="utf-8") as f:
        config: dict = json.load(f)
        root_path = config.get("root")
        sort_path = config.get("sort")
        branch_paths = config.get("root_locations")
        overrides = config.get("overrides")
        filetype_matching = config.get("filetype_matching", {})
        return Conf(root_path=root_path, sort_path=sort_path, branch_paths=branch_paths, overrides=overrides, filetype_matching=filetype_matching)

