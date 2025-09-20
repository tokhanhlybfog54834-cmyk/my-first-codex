# my-first-codex

该仓库提供一个用于整理福建省施工类每日标讯的示例实现。核心思路如下：

- 将不同交易平台当天发布的施工项目整理为统一字段（开标时间、评标办法、资质要求等）。
- 支持从多个 JSON 数据源加载数据，后续可扩展为实际的网页/接口采集脚本。
- 输出结构化数据（CSV，可直接用 Excel 打开）以及一个静态 HTML 看板，方便快速浏览与分享。

当前项目内置了一份示例数据 `data/sample_projects.json`，数据字段参考题主提供的 Excel 表格式，可作为后续真实数据对接的模板。

## 快速开始

1. **准备 Python 3.11 环境**（仓库已经使用该版本生成代码）。
2. 执行以下命令生成看板与 CSV：

   ```bash
   python scripts/generate_dashboard.py
   ```

   运行后将在 `output/` 目录下生成：

   - `daily_tenders.html`：静态可视化看板，包含全部字段与附件标签。
   - `daily_tenders.csv`：表格数据，便于在 Excel 里二次加工或导出。

3. 如果只想查看某个地市的项目，可追加 `--city` 参数：

   ```bash
   python scripts/generate_dashboard.py --city 厦门
   ```

4. 若后续将每日抓取到的真实数据存放为 JSON 文件，可通过多次指定 `--source` 合并：

   ```bash
   python scripts/generate_dashboard.py --source data/sample_projects.json --source /path/to/other_city.json
   ```

## 文件结构

```
├── data/
│   └── sample_projects.json      # 示例标讯数据
├── output/                       # 运行脚本后生成的结果（初次为空）
├── scripts/
│   └── generate_dashboard.py     # 主脚本：加载数据、生成 CSV/HTML
└── src/daily_bidding/
    ├── __init__.py               # 对外暴露的 API
    ├── loader.py                 # 数据加载封装
    ├── models.py                 # 数据模型和表头定义
    ├── pipeline.py               # 汇总/过滤流程
    └── renderers.py              # CSV 与 HTML 输出
```

## 后续扩展建议

- **对接真实网站**：在 `scripts/` 目录新增爬取脚本，将每日采集到的数据写入 JSON，字段保持与示例一致，即可复用现有 UI。
- **接入调度**：可将 `generate_dashboard.py` 配置到定时任务（如 crontab）中，每天自动生成最新报表。
- **输出 Excel**：如果运行环境允许安装第三方库，可在 `renderers.py` 里补充 `openpyxl` 等库将 CSV 进一步转为 `.xlsx`。

欢迎根据实际业务需求继续扩展。
