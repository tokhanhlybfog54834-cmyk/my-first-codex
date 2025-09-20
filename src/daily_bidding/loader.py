from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import TenderCollection


class TenderLoader:
    """Loads tender entries from JSON files."""

    def __init__(self, paths: Iterable[Path]):
        self.paths = [Path(path) for path in paths]

    def load(self) -> TenderCollection:
        items = []
        for path in self.paths:
            if not path.exists():
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                data = data.get("items", [])
            if not isinstance(data, list):
                continue
            items.extend(data)
        return TenderCollection.from_dicts(items)
