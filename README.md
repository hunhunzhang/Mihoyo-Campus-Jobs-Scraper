# Campus Jobs Scraper / 校园招聘爬虫集合

一个基于 Python Playwright 的自动化爬虫工具集合，目前支持抓取 **米哈游 (miHoYo)** 和 **字节跳动 (Bytedance)** 的校园招聘官网职位信息，并直接生成格式化好的 Excel 报表。

## ✨ 项目功能

*   **多平台支持**：独立脚本分别针对不同企业的招聘系统进行适配。
*   **全自动抓取**：自动遍历官网的所有职位列表页，智能处理翻页。
*   **API 拦截 (Network Interception)**：直接拦截浏览器发出的 API 响应数据，效率高且稳定，规避了复杂的 HTML 解析。
*   **深度解析**：针对每个职位提取详情，如“任职要求”、“工作职责”、“加分项”等。
*   **数据清洗**：自动从文本中提取“学历要求”等关键字段。
*   **美观报表**：直接生成带有样式、列宽调整的 `.xlsx` 文件。

## 📂 包含脚本

1.  **米哈游 (miHoYo)**: `main.py`
    *   目标网站：[米哈游校园招聘](https://campus.mihoyo.com/)
    *   输出文件：`mihoyo_campus_jobs.xlsx` (或类似)
2.  **字节跳动 (Bytedance)**: `bytedance_crawler.py`
    *   目标网站：[字节跳动校园招聘](https://jobs.bytedance.com/campus/position)
    *   输出文件：`bytedance_campus_jobs.xlsx`

## 🛠️ 实现思路

1.  **自动化控制 (Playwright)**：
    *   为了绕过可能存在的反爬策略（如 API 签名校验、动态渲染），本项目使用 Playwright 驱动浏览器模拟真实用户操作。
    *   自动处理翻页逻辑（识别 `Next` 按钮状态、`aria-disabled` 属性等）。

2.  **数据采集策略**：
    *   **米哈游**：拦截 `/api/job/list` (列表) 和 `/api/job/info` (详情) 接口。
    *   **字节跳动**：拦截 `/api/v1/search/job/posts` 接口，该接口直接返回了列表及详细描述，无需二次请求详情页。

3.  **数据流处理**：
    *   爬取过程中数据暂存在内存中，利用 `pandas` 和 `openpyxl` 生成最终报表，不产生中间临时文件。

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

    *   **爬取米哈游 (miHoYo)**：
        ```bash
        python main.py
        ```
    *   **爬取字节跳动 (Bytedance)**：
        ```bash
        python bytedance_crawler.py
        ```

2.  **查看结果**：
    脚本运行完成后，会在当前目录下生成对应的 Excel 文件，如 `mihoyo_campus_jobs_full.xlsx` 或 `bytedance_campus_jobs.xlsx`。

## 📄 输出示例

生成的 Excel 表格将自动进行美化，包括：
*   蓝色表头，白色加粗字体。
*   所有单元格自动换行，顶端对齐。
*   根据内容类型预设列宽。

## 🤖 完成本项目所用工具

本项目完全由 AI 编程助手辅助构建。

*   **AI 助手**: **GitHub Copilot**
*   **使用模型**: **Gemini 3 Pro (Preview)**

### 💡 核心开发工具 (Agent Tools)
在实现本项目的过程中，Copilot 综合运用了以下能力工具：

1.  **fetch_webpage**: 抓取米哈游招聘官网的前端页面，快速理解网页结构与反爬机制。
2.  **grep_search**: 对下载的网页 `main.js` 核心代码进行文本搜索与分析，成功逆向出隐藏的 API 接口 (`/api/job/list`, `/api/job/info`)。
3.  **run_in_terminal**: 直接在终端环境中执行命令，用于安装 Python 依赖库、运行爬虫脚本进行测试、以及执行 Git 版本管理。
4.  **create_file / replace_string_in_file**: 从零编写并持续迭代项目核心代码 (`main.py`)，自动修复运行报错，并生成项目文档。

### 🏗️ 项目技术栈 (Tech Stack)
*   **Python**: 核心编程语言。
*   **Playwright**: 用于浏览器自动化操作与网络请求拦截（核心爬虫库）。
*   **Pandas**: 用于数据清洗与结构化处理（Excel 导出）。
*   **OpenPyXL**: 用于生成样式美观的 Excel 报表（格式调整）。

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
10. `作为完成本项目的重要工具，请你在README的”完成本项目所用工具“中介绍你自己并列出实现本项目你所用到的所有工具列表及其作用`
11. `现在以同样的思路爬取字节跳动的校园招聘https://jobs.bytedance.com/campus/position的信息。另外编写独立的python代码文件于项目中`
12. `更新README说明和git仓库`
---
*Disclaimer: This tool is for educational purposes only. Please respect the website's terms of service and robots.txt.*
