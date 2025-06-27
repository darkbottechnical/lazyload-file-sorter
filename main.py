import subprocess
import sys

from modules.match import match_checkers

if __name__ == "__main__":
    subprocess.Popen(
        [sys.executable, "-m", "modules.sort"], creationflags=subprocess.DETACHED_PROCESS
    )
