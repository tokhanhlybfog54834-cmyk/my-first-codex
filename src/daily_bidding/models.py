from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TenderEntry:
    """Represents a single construction tender item."""

    bid_date: str
    bid_time: str
    publish_date: str
    city: str
    county: str
    evaluation_method: str
    project_name: str
    budget: Optional[float]
    bid_bond: Optional[float]
    company_qualification: str
    pm_qualification: str
    tech_lead_qualification: str
    duration: Optional[int]
    performance_requirement: str
    price_adjustment: str
    document_type: str
    attachment_count: int
    attachments: List[str] = field(default_factory=list)
    source_site: str = ""
    detail_url: str = ""

    def to_csv_row(self) -> List[str]:
        """Return a list ready to be written to CSV."""
        return [
            self.bid_date,
            self.bid_time,
            self.publish_date,
            self.city,
            self.county,
            self.evaluation_method,
            self.project_name,
            format_number(self.budget),
            format_number(self.bid_bond),
            self.company_qualification,
            self.pm_qualification,
            self.tech_lead_qualification,
            format_number(self.duration),
            self.performance_requirement,
            self.price_adjustment,
            self.document_type,
            str(self.attachment_count),
            "\n".join(self.attachments),
            self.source_site,
            self.detail_url,
        ]


@dataclass
class TenderCollection:
    """Container that holds multiple tender entries and provides helpers."""

    entries: List[TenderEntry] = field(default_factory=list)

    @classmethod
    def from_dicts(cls, data: List[dict]) -> "TenderCollection":
        entries = [TenderEntry(**item) for item in data]
        return cls(entries=entries)

    def filter_by_city(self, city: str) -> "TenderCollection":
        city = city.strip()
        if not city:
            return TenderCollection(entries=list(self.entries))
        filtered = [entry for entry in self.entries if entry.city == city]
        return TenderCollection(entries=filtered)

    def sort_by_bid_date(self) -> "TenderCollection":
        def sort_key(entry: TenderEntry):
            return parse_sortable_key(entry.bid_date, entry.bid_time)

        return TenderCollection(entries=sorted(self.entries, key=sort_key))

    def to_csv_rows(self) -> List[List[str]]:
        headers = [
            "开标日期",
            "开标时间",
            "公告发布日期",
            "地市",
            "县区",
            "评标办法",
            "项目名称",
            "预算金额（万元）",
            "投标保证金（万元）",
            "企业资质",
            "拟派项目经理资质",
            "拟派技术负责人资质",
            "工期（日）",
            "业绩要求",
            "计价基准/下浮",
            "阶段",
            "附件数量",
            "附件列表",
            "来源网站",
            "详情链接",
        ]
        return [headers] + [entry.to_csv_row() for entry in self.entries]


def parse_sortable_key(bid_date: str, bid_time: str) -> tuple:
    """Convert Chinese month/day strings to a tuple for sorting."""
    month, day = parse_month_day(bid_date)
    hour, minute = parse_time(bid_time)
    return month, day, hour, minute


def parse_month_day(value: str) -> tuple:
    value = value.strip()
    month = 0
    day = 0
    if "月" in value and "日" in value:
        try:
            before, after = value.split("月", 1)
            month = int(before)
            day = int(after.split("日", 1)[0])
        except ValueError:
            month = 0
            day = 0
    return month, day


def parse_time(value: str) -> tuple:
    value = value.strip()
    try:
        hour_str, minute_str = value.split(":", 1)
        return int(hour_str), int(minute_str)
    except ValueError:
        return 0, 0


def format_number(value: Optional[float]) -> str:
    if value is None or value == "":
        return ""
    if isinstance(value, (int, float)):
        if float(value).is_integer():
            return str(int(float(value)))
        return f"{float(value):.4f}".rstrip("0").rstrip(".")
    return str(value)
