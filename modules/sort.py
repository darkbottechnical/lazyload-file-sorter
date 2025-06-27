import os
import shutil
import logging
import pymsgbox

from time import sleep
from contextlib import contextmanager
from modules.parse import parse_config, Conf
from modules.constants import FILETYPE_MATCHING
from modules.match import match_checkers, MatchChecker
from modules.file import File

CONFIG: Conf = parse_config()

# Setup logging
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.abspath(os.path.join(log_dir, 'sorter.log'))
logging.basicConfig(
    filename=log_path,
    filemode='a',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

@contextmanager
def _movedir(dir):
    _prevpath = os.path.abspath(os.getcwd())
    try:
        os.chdir(dir)
        yield
    finally:
        os.chdir(_prevpath)

def run_overrides(file: File):
    for matcher in match_checkers:
        matcher: MatchChecker
        try:
            match = matcher.check(file)
        except Exception as e:
            logger.error(f"Error in matcher {matcher.call.__name__} for file {file.name}: {e}")
            pymsgbox.alert(f"Error in matcher {matcher.call.__name__} for file {file.name}: {e}", "Sorter Error")
            continue
        if match:
            return match
    return None

def get_dst_dir(filename: str) -> str:
    root = CONFIG.ROOTDIR
    file = File(name=filename)
    file_extension = os.path.splitext(filename)[1].lstrip(".")

    root_branch = None

    for name, ext_list in CONFIG.filetype_matching.items():
        if file_extension in ext_list:
            root_branch = CONFIG.branches.get(name, CONFIG.else_path)
    if root_branch is None:
        root_branch = CONFIG.else_path
    
    logger.info(f"{filename} belongs in {root_branch}.")
    path = os.path.abspath(os.path.join(root, root_branch, filename))
    return path

def sorter():
    with _movedir(CONFIG.DIRTOSORT):
        while True:
            for file in os.listdir():
                src_dir = file
                try:
                    dst_dir = run_overrides(File(name=file))
                except Exception as e:
                    logger.error(f"Error running overrides for {file}: {e}")
                    pymsgbox.alert(f"Error running overrides for {file}: {e}", "Sorter Error")
                    continue
                if not dst_dir:
                    logger.info(f"No overrides found for {file}. Using specified directory.")
                    dst_dir = get_dst_dir(file)
                logger.info(f"Moving {src_dir} to {dst_dir}")
                try:
                    shutil.move(src=src_dir, dst=dst_dir)
                except FileNotFoundError:
                    logger.error(f"Destination {dst_dir} not found. Skipping {file}.")
                    pymsgbox.alert(f"Destination {dst_dir} not found. Skipping {file}.", "Sorter Error")
                    continue
                except Exception as e:
                    logger.error(f"Error moving {src_dir} to {dst_dir}: {e}")
                    pymsgbox.alert(f"Error moving {src_dir} to {dst_dir}: {e}", "Sorter Error")
                    continue
            sleep(10)
        
if __name__ == "__main__":
    sorter()
    print("[+] Sorter process started.")