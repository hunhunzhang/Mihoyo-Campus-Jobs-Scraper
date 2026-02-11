# Mihoyo Campus Jobs Scraper / 米哈游校招爬虫

一个基于 Python Playwright 的自动化爬虫工具，用于抓取米哈游校园招聘官网的职位信息，并直接生成格式化好的 Excel 报表。

## ✨ 项目功能

*   **全自动抓取**：自动遍历米哈游校招官网的所有职位列表页。
*   **深度解析**：针对每个职位自动抓取详情页，提取“任职要求”、“工作职责”、“加分项”等详细描述。
*   **数据清洗**：自动从文本中提取“学历要求”字段。
*   **Excel 导出**：直接生成美观的 `.xlsx` 文件，包含以下字段：
    *   岗位名称
    *   岗位类别（如程序&技术类）
    *   性质（如实习生专项）
    *   学历要求（自动提取）
    *   任职要求
    *   工作职责
    *   加分项

## 🛠️ 实现思路

1.  **自动化控制 (Playwright)**：
    *   为了绕过可能存在的反爬策略（如 API 签名校验），本项目不直接请求 API，而是使用 Playwright 驱动浏览器模拟真实用户操作。
    *   脚本会根据系统环境自动选择 Chrome、Edge 或 Chromium 浏览器启动。

2.  **API 拦截 (Network Interception)**：
    *   **效率优化**：虽然是模拟浏览器，但我们并不通过解析 DOM HTML 来获取数据，而是直接拦截浏览器发出的网络请求响应（Response Hook）。
    *   **列表接口**：拦截 `/api/job/list` 获取职位 ID 和基础信息。
    *   **详情接口**：拦截 `/api/job/info` 获取完整的职位描述。

3.  **数据流处理**：
    *   爬取过程中数据暂存在内存中，去重后直接利用 `pandas` 和 `openpyxl` 生成最终报表，不产生中间临时文件。

## 📦 环境要求与安装

### 1. 安装 Python 依赖

本项目依赖 Python 3.8+。请确保安装以下库：

```bash
pip install -r requirements.txt
```

*   `playwright`: 用于浏览器自动化。
*   `pandas`: 用于数据结构化和 Excel 处理。
*   `openpyxl`: 用于 Excel 格式化（样式、列宽等）。

### 2. 安装浏览器驱动

如果是首次使用 Playwright，需要安装浏览器驱动：

```bash
playwright install
```

> **注意**：如果下载速度慢，脚本内置了自动降级策略，会尝试使用您电脑上已安装的 Google Chrome 或 Microsoft Edge 浏览器。

## 🚀 如何使用

1.  **运行脚本**：

    ```bash
    python main.py
    ```

2.  **查看结果**：
    脚本运行完成后，会在当前目录下生成 `mihoyo_campus_jobs_full.xlsx`。

## 📄 输出示例

生成的 Excel 表格将自动进行美化，包括：
*   蓝色表头，白色加粗字体。
*   所有单元格自动换行，顶端对齐。
*   根据内容类型预设列宽。

## 🤖 完成项目所用工具

本项目主要由 **GitHub Copilot** (Model: Gemini 3 Pro Preview) 协助开发者完成。在开发过程中，Copilot 调用了以下关键工具来加速开发流程：

| 工具名称 | 作用 | 实际应用场景 |
| :--- | :--- | :--- |
| **fetch_webpage** | 网页内容抓取 | 获取米哈游校招官网的初始文本和结构，辅助理解页面布局。 |
| **run_in_terminal** | 终端命令执行 | 运行 Python 脚本、安装依赖 (`pip install`)、执行 Git 操作以及调试代码。 |
| **create_file** | 文件创建 | 快速生成爬虫脚本 (`main.py`)、配置文件 (`requirements.txt`) 和文档 (`README.md`)。 |
| **replace_string_in_file** | 智能文件编辑 | 对现有代码进行精确修改，如优化分页逻辑、添加字段提取功能和修复 Bug。 |
| **runSubagent** | 子智能体任务 | 尝试搜索和分析 API 端点，辅助判断页面加载机制（SPA/API）。 |

## 💬 完成本项目所用提示词

以下是构建该项目过程中所使用的 Prompt 历史，按时间顺序排列：

1.  `写个python爬虫，爬取https://jobs.mihoyo.com/#/campus/position这个网页的所有招聘信息，并转化为结构化数据存储起来`
2.  `检查当前窗口输出分析问题`
3.  `对于每项岗位我需要爬取页面的更多内容信息如https://jobs.mihoyo.com/#/campus/position/6681此页面的“工作职责”、“任职要求”、“加分项”等部分内容`
4.  `编写一个新的代码文件实现将结构化的json数据文件转化为excel表格，表格有“岗位名称”“岗位类别”（如程序&技术类）“性质”（实习/2026秋招）“任职要求”“工作职责”“加分项”等`
5.  `转化为表格在调整行高，对于任职要求、工作职责、加分项等每说完一项要求就换行，使得excel表格大小合适美观`
6.  `在“性质”列之后添加一列“学厉要求”内容在“任职要求”中提取出来`
7.  `优化整个项目的代码将爬取的数据直接采用excel存储省去存为json再由json转为excel的步骤。`
8.  `我现在要将当前项目转化为github仓库并上传，请你删除多余无用的代码和文件并添加仓库的README文档，和环境配置需求文档。在README文档中说明项目做了什么、实现思路及如何使用，注意格式美观、清晰。`
9.  `将我当前项目的会话历史（由我输入的所有提示词）按顺序写入README中的“完成本项目所用提示词”部分`

---
*Disclaimer: This tool is for educational purposes only. Please respect the website's terms of service and robots.txt.*
