import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

include(
    "components/base.py",
    "components/database.py",
    "components/apps.py",
    "components/templates.py",
    "components/security.py",
    "components/localization.py",
    "components/files.py",
)
