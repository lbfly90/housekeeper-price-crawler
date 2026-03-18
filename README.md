# 北京钟点工价格爬虫

使用 GitHub Actions + Playwright 自动爬取北京钟点工价格数据。

## 数据来源

- 小红书
- 58同城
- 赶集网

## 运行方式

### 手动触发

进入 Actions 页面，选择 "Housekeeper Price Crawler" workflow，点击 "Run workflow"。

### 自动运行

每周一早上8点自动运行。

## 数据格式

### JSON
```json
{
  "platform": "小红书",
  "keyword": "北京钟点工价格",
  "price": 50,
  "unit": "元/小时",
  "crawl_time": "2024-01-15T08:00:00"
}
```

### CSV
包含所有原始数据，可直接用 Excel 打开。

## 历史数据

所有数据保存在 `data/` 目录，按日期命名。

## 价格统计

查看 `data/latest_summary.csv` 获取最新汇总。
