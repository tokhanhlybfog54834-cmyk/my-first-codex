from __future__ import annotations

import csv
import html
from pathlib import Path

from .models import TenderCollection, TenderEntry


def write_csv(collection: TenderCollection, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fp:
        writer = csv.writer(fp)
        for row in collection.to_csv_rows():
            writer.writerow(row)


def render_html(collection: TenderCollection, title: str = "每日施工标讯汇总") -> str:
    headers = collection.to_csv_rows()[0]
    rows = collection.entries
    table_rows = "\n".join(_render_row(entry) for entry in rows)
    header_cells = "".join(f"<th>{html.escape(text)}</th>" for text in headers)
    body = (
        f"<table class=\"tender-table\">"
        f"<thead><tr>{header_cells}</tr></thead>"
        f"<tbody>{table_rows}</tbody>"
        f"</table>"
    )
    return f"""<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\">
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: "Microsoft YaHei", Arial, sans-serif; margin: 2rem; background-color: #f6f6f6; }}
    h1 {{ color: #333; }}
    .summary {{ margin-bottom: 1rem; color: #555; }}
    table.tender-table {{ width: 100%; border-collapse: collapse; background: white; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }}
    table.tender-table th, table.tender-table td {{ border: 1px solid #e5e5e5; padding: 0.5rem; text-align: left; vertical-align: top; }}
    table.tender-table th {{ background: #f0f3f9; font-weight: 600; }}
    table.tender-table tbody tr:nth-child(even) {{ background: #fafafa; }}
    table.tender-table tbody tr:hover {{ background: #f1f7ff; }}
    .attachments span {{ display: inline-block; background: #eef2ff; border-radius: 4px; padding: 0.1rem 0.4rem; margin-right: 0.3rem; margin-bottom: 0.2rem; }}
    .numeric {{ text-align: right; }}
    .footer {{ margin-top: 2rem; font-size: 0.85rem; color: #777; }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <div class=\"summary\">共 {len(rows)} 条施工项目，支持按地市筛选与排序。</div>
  {body}
  <div class=\"footer\">数据来源：项目配置文件（示例数据）。实际对接可通过扩展 <code>TenderLoader</code> 加载每日实时标讯。</div>
</body>
</html>
"""


def _render_row(entry: TenderEntry) -> str:
    attachments = "".join(
        f"<span>{html.escape(label)}</span>" for label in entry.attachments
    ) or "-"
    values = entry.to_csv_row()
    rendered = []
    numeric_columns = {7, 8, 12}
    for idx, value in enumerate(values):
        if idx == 17:  # attachments list column
            rendered.append(f"<td class=\"attachments\">{attachments}</td>")
        else:
            cell_class = "numeric" if idx in numeric_columns else ""
            escaped = html.escape(value)
            rendered.append(f"<td class=\"{cell_class}\">{escaped if escaped else '-'}" + "</td>")
    return "<tr>" + "".join(rendered) + "</tr>"


def save_html(collection: TenderCollection, path: Path, title: str = "每日施工标讯汇总") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = render_html(collection, title=title)
    path.write_text(content, encoding="utf-8")
