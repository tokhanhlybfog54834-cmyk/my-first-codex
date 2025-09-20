from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Optional

from .loader import TenderLoader
from .models import TenderCollection


@dataclass
class PipelineConfig:
    sources: Iterable[Path]
    city_filter: Optional[str] = None


class DailyTenderPipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config

    def run(self) -> TenderCollection:
        loader = TenderLoader(self.config.sources)
        collection = loader.load()
        if self.config.city_filter:
            collection = collection.filter_by_city(self.config.city_filter)
        return collection.sort_by_bid_date()
