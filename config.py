import os
from pathlib import Path

DEV = os.environ.get("DEV", False)

if DEV:
    DATA_PATH = Path(__file__).parent / "data"
else:
    DATA_PATH = Path("/var/lib/data")
