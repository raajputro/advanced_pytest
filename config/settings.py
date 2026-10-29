"""Central configuration. Every value can be overridden with an environment variable."""
import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# GlobalSQA "XYZ Bank" – a public AngularJS demo banking app (no registration needed)
BASE_URL = os.getenv(
    "BASE_URL",
    "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login",
)

DEFAULT_TIMEOUT_MS = int(os.getenv("DEFAULT_TIMEOUT_MS", "15000"))
SCREENSHOT_DIR = Path(os.getenv("SCREENSHOT_DIR", ROOT_DIR / "screenshots"))
MOCK_SITE_DIR = ROOT_DIR / "mock_site"
