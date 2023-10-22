from __future__ import annotations

import os


# Directories
UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_PACKAGE = os.path.dirname(UTILS_DIR)
ROOT = os.path.dirname(PROJECT_PACKAGE)
DATA_DIR = os.path.join(ROOT, "data")

# Files
CONFIG_FILE = os.path.join(ROOT, "config.yaml")

# Logging
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
