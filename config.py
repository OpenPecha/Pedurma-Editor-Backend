import os
from pathlib import Path

DEV = os.environ.get("DEV", False)

if DEV:
    DATA_PATH = Path(__file__).parent / "data"
    os.environ["AWS_SHARED_CREDENTIALS_FILE"] = str(
        Path.home().resolve() / ".aws" / "op_credentials"
    )
    print(os.environ["AWS_SHARED_CREDENTIALS_FILE"])
else:
    DATA_PATH = Path("/var/lib/data")
