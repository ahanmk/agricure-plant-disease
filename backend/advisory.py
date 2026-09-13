import json
import os
from typing import Dict, Any, Optional

BASE_DIR = os.path.dirname(__file__)
ADVISORY_FILE = os.path.abspath(
    os.path.join(BASE_DIR, "data", "advisory.json")
)

# Fallback to outer data/ if running from outer workspace
if not os.path.exists(ADVISORY_FILE):
    ADVISORY_FILE = os.path.abspath(
        os.path.join(BASE_DIR, "..", "data", "advisory.json")
    )

class AdvisoryService:
    def __init__(self, filepath: str = ADVISORY_FILE):
        self.filepath = filepath
        self._cache: Dict[str, Any] = {}
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                self._cache = json.load(f)
        else:
            self._cache = {}

    def get_advisory(self, class_name: str) -> Optional[Dict[str, Any]]:
        return self._cache.get(class_name)

    def get_all_classes(self):
        return list(self._cache.keys())

advisory_service = AdvisoryService()
