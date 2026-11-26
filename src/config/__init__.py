from pathlib import Path
import sys
from dotenv import load_dotenv

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).resolve().parent
else:
    ROOT_DIR = Path(__file__).resolve().parents[2]

load_dotenv(ROOT_DIR / "config" / ".env")

ASSETS_DIR = ROOT_DIR / "assets"
RESOURCES_DIR = ROOT_DIR / "resources"
