from pathlib import Path
import subprocess
import sys

project_root = Path(__file__).resolve().parent.parent

script_path = project_root / "src" / "RidersPyTools_KC" / "MapParser.py"
target_dir = "C:/Users/Jerrod/Documents/riders/sonicriderste/build"
lookingList = ["players","Action_TrickSpin"]

# subprocess.run(
#     [
#         sys.executable,
#         str(script_path),
#         str(target_dir),
#         lookingList,
#     ],
#     cwd=str(script_path.parent),
#     check=True,
# )

from src.RidersPyTools_KC.MapParser import read_for_list

lookingList = ["players","Action_TrickSpin"]
lister=read_for_list(target_dir,lookingList)
print(lister)
print(type(lister["players"]))