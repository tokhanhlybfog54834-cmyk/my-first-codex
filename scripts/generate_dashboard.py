"""Generate a daily construction tender dashboard from configured sources."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR / 'src'))

from daily_bidding import (
    DailyTenderPipeline,
    PipelineConfig,
    save_html,
    write_csv,
)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        action="append",
        default=["data/sample_projects.json"],
        help="路径到包含招标项目JSON数据的文件，可重复指定多个。",
    )
    parser.add_argument(
        "--city",
        default="",
        help="按地市过滤，例如：厦门、福州。默认不过滤。",
    )
    parser.add_argument(
        "--html",
        default="output/daily_tenders.html",
        help="生成的HTML看板输出路径。",
    )
    parser.add_argument(
        "--csv",
        default="output/daily_tenders.csv",
        help="生成的CSV数据表输出路径（Excel可直接打开）。",
    )
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    config = PipelineConfig(
        sources=[Path(path) for path in args.source],
        city_filter=args.city or None,
    )
    pipeline = DailyTenderPipeline(config)
    collection = pipeline.run()

    save_html(collection, Path(args.html))
    write_csv(collection, Path(args.csv))

    print(
        f"生成完成，共 {len(collection.entries)} 条记录，"
        f"HTML 输出：{args.html}，CSV 输出：{args.csv}."
    )


if __name__ == "__main__":
    main()
