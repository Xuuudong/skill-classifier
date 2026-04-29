---
name: skill-classifier
description: 对 skills 文件夹进行智能分类。当用户说「帮忙分类 skills」「分析这个 skills 文件夹」「这个 skill 应该归于什么类别」「对这些 skills 进行分类」时，必须使用本 skill。自动扫描指定路径下的所有 skill，读取 SKILL.md 内容，按两级分类体系归类，生成 JSON 和 HTML 报告。
---

# Skill 分类器

对指定文件夹中的 skills 进行智能分类，生成结构化分类报告。

## 分类体系

### 一级分类

| 类别 | 图标 | 说明 | 核心特征 |
|------|------|------|---------|
| 开发与自动化 | 🛠️ | 软件开发工具、自动化脚本、AI Agent 框架 | 代码开发、流程自动化、智能体构建 |
| 文档与内容创作 | 📄 | 文档生成、媒体处理、格式转换 | 文件输出、内容创作、可视化 |
| 搜索与研究 | 🔍 | 网络搜索、信息采集、深度分析 | 信息检索、内容监控、研究整合 |
| 金融数据 | 💰 | 股票行情、量化分析、金融数据 API | 投资分析、数据获取、风险监控 |
| 通讯与协作 | 💬 | 邮件收发、即时通讯、笔记协作 | 消息传递、团队协作、知识管理 |
| 其他 | 📦 | 未归入以上类别的工具 | 天气、智能家居、营销等 |

### 二级分类

| 一级分类 | 二级分类 | 说明 | 分类依据 | 典型技能 |
|---------|---------|------|---------|---------|
| 开发与自动化 | AI Agent框架 | Agent 记忆系统、自我进化、多智能体协作 | agent, memory, evolver, self-improving | agent-memory, evolver |
| 开发与自动化 | 浏览器自动化 | Playwright、Selenium、浏览器控制 | playwright, browser, selenium, headless | playwright-mcp, browser-use |
| 开发与自动化 | 开发工具 | MCP 服务器、CLI 工具、SDK、API 工具 | mcp, server, api, sdk, cli tool | mcporter, skill-classifier |
| 文档与内容创作 | 文档生成与编辑 | Word/PDF/PPT/Excel 创建与编辑 | docx, pdf, pptx, xlsx, document | minimax-docx, weekly-report |
| 文档与内容创作 | 媒体与设计 | 图像、视频、音频、图表可视化 | image, video, graph, diagram, design | fireworks-tech-graph, whisper |
| 搜索与研究 | Web搜索 | 搜索引擎集成、多源检索 | search, tavily, brave, google | tavily-search, brave-search |
| 搜索与研究 | 深度研究 | 信息整合、分析报告、RSS 监控 | research, analysis, rss, watcher | deep-research, blogwatcher |
| 金融数据 | 基金投资 | 基金日报、持仓诊断、退休规划 | fund, 基金, portfolio, retirement | fund-daily, portfolio-doctor |
| 金融数据 | 量化数据 | 金融数据 API、量化分析平台 | tushare, akshare, quant, 量化 | akshare, tushare-finance |
| 通讯与协作 | 通讯平台 | 邮件、Slack、Discord、飞书 | email, slack, discord, 飞书 | gmail, slack, discord |
| 通讯与协作 | 笔记协作 | Notion、Obsidian、项目管理 | notion, obsidian, trello, 笔记 | notion, trello, apple-notes |

### 二级分类优先级规则

当技能匹配多个二级分类时，按以下优先级判定：

| 一级分类 | 优先级（高→低） |
|---------|----------------|
| 开发与自动化 | AI Agent框架 > 浏览器自动化 > 开发工具 |
| 文档与内容创作 | 媒体与设计 > 文档生成与编辑 |
| 搜索与研究 | 深度研究 > Web搜索 |
| 金融数据 | 基金投资 > 量化数据 |
| 通讯与协作 | 通讯平台 > 笔记协作 |

### 特殊规则

- **图表/可视化**：含 graph/diagram/chart/可视化 → 优先归入「媒体与设计」
- **PDF 文档**：含 pdf + document → 优先归入「文档生成与编辑」
- **Agent 浏览器**：名称含 agent 但功能是浏览器自动化 → 按功能归入「浏览器自动化」

### 高级分类规则

#### 负向规则

当检测到特定关键词时，自动排除该分类，避免错误归类：

| 一级分类 | 二级分类 | 排除关键词 |
|---------|---------|-----------|
| 开发与自动化 | AI Agent框架 | playwright, selenium, browser, mcp server |
| 开发与自动化 | 浏览器自动化 | agent memory, evolver, self-improving |
| 文档与内容创作 | 媒体与设计 | docx, word 文档, pdf 文档, excel, pptx |
| 文档与内容创作 | 文档生成与编辑 | 图像生成, 视频处理, audio, whisper |
| 金融数据 | 基金投资 | tushare, akshare, quant api |
| 金融数据 | 量化数据 | portfolio, retirement, 基金日报 |

#### 强制匹配规则

当匹配到精确模式时，强制归入指定分类（置信度 0.95）：

| 模式 | 二级分类 |
|------|---------|
| `agent.*memory` / `evolver` / `multi-agent` | AI Agent框架 |
| `playwright` / `selenium` / `browser-use` | 浏览器自动化 |
| `mcp.*server` / `mcporter` | MCP工具 |
| `架构图` / `流程图` / `可视化` / `画图` | 媒体与设计 |
| `docx.*create` / `pdf.*generate` / `周报` | 文档生成与编辑 |
| `deep-research` / `rss.*monitor` | 深度研究 |
| `tavily` / `web-search` / `搜索引擎` | Web搜索 |
| `基金.*日报` / `portfolio.*doctor` / `退休规划` | 基金投资 |
| `tushare` / `akshare` / `量化.*接口` | 量化数据 |

#### 置信度计算

```
置信度 = 最高分 / (最高分 + 次高分 + 1)
```

| 置信度范围 | 标记 | 说明 |
|-----------|------|------|
| ≥ 0.7 | 高置信度 | 分类确定 |
| 0.5 - 0.7 | 中等置信度 | 分类较确定 |
| < 0.5 | 低置信度 | 标记「待确认」 |

强制匹配命中时，置信度固定为 0.95。

## 工作流程

### Step 1: 获取用户输入

询问用户要扫描的 skills 文件夹路径：
- **文件夹路径**：直接扫描该文件夹下的所有 skill 子目录
- **JSON 文件路径**：读取类似 `anthropics-skills.json` 格式的索引文件

### Step 2: 扫描 Skills

**使用脚本自动扫描（推荐）：**

```bash
python "C:\Users\Lenovo\.claude\skills\skill-classifier\scripts\scan_skills.py" "<目录路径>" --output scan_result.json
```

脚本自动处理：
- 大小写兼容（SKILL.md / skill.md / Skill.md）
- 备选文件（README.md）
- 完整性验证

### Step 3: 一级分类

基于关键词权重自动归类到 6 个一级分类：

```bash
python scripts/classify_skills.py scan_result.json --output classification.json
```

### Step 4: 二级分类

在一级分类基础上，根据具体功能细分到二级分类：

```bash
python scripts/subclassify.py classification.json --output final_result.json
```

二级分类规则示例：
- `playwright-mcp` → 开发与自动化 > MCP与浏览器自动化
- `agent-memory` → 开发与自动化 > AI Agent框架
- `pdf-docx` → 文档与内容创作 > 文档生成与编辑

### Step 5: 生成报告

```bash
python scripts/generate_report.py final_result.json report.html
```

## 一键执行

完整流程合并为一条命令：

```bash
# 扫描 + 一级分类 + 二级分类 + 生成报告
python scripts/scan_skills.py "<目录>" --output scan.json && \
python scripts/classify_skills.py scan.json --output classification.json && \
python scripts/subclassify.py classification.json --output final.json && \
python scripts/generate_report.py final.json report.html
```

## 目录结构

```
skill-classifier/
├── SKILL.md                      # 本文件
├── scripts/
│   ├── scan_skills.py           # 扫描脚本
│   ├── classify_skills.py       # 一级分类脚本
│   ├── subclassify.py           # 二级分类脚本
│   ├── generate_report.py       # 报告生成脚本
│   └── organize_skills.py       # 归类整理脚本
└── references/
    ├── classification-rules.md  # 分类规则详解
    └── output-schema.md         # 输出格式规范
```

## 归类整理

分类完成后，可以使用 `organize_skills.py` 将 skills 按分类整理到不同文件夹：

```bash
# 预览整理效果（不执行实际操作）
python scripts/organize_skills.py final_result.json -o ./organized_skills --dry-run

# 复制模式（默认，保留原文件）
python scripts/organize_skills.py final_result.json -o ./organized_skills

# 移动模式（会删除原文件，请谨慎使用）
python scripts/organize_skills.py final_result.json -o ./organized_skills --mode move
```

整理后的目录结构：
```
organized_skills/
├── 开发与自动化/
│   ├── AI Agent框架/
│   │   ├── agent-memory/
│   │   └── evolver/
│   ├── 浏览器自动化/
│   │   └── playwright-mcp/
│   └── 开发工具/
│       └── skill-classifier/
├── 文档与内容创作/
│   ├── 媒体与设计/
│   └── 文档生成与编辑/
└── organize_summary.md    # 整理报告
```

## 输出文件

### 分类结果文件

| 文件 | 说明 |
|------|------|
| `scan_result.json` | 扫描结果，包含所有 skill 的元信息 |
| `classification.json` | 一级分类结果 |
| `final_result.json` | 二级分类最终结果（含置信度） |
| `report.html` | 可视化 HTML 报告（含二级分类） |

### 归类整理文件

| 文件 | 说明 |
|------|------|
| `organized_skills/` | 按分类整理后的 skills 目录 |
| `organize_summary.md` | 整理结果摘要报告 |

## 输出字段说明

每个 skill 的分类结果包含以下字段：

```json
{
  "name": "skill-name",
  "description": "技能描述",
  "primary_category": "一级分类",
  "secondary_category": "二级分类",
  "confidence": 0.85,
  "classification_reason": "分类理由",
  "secondary_reason": "二级分类理由",
  "secondary_confidence": 0.92
}
```

## 输出位置

默认保存在用户指定目录：
- JSON: `<输出目录>/skills-classification.json`
- HTML: `<输出目录>/skills-classification-report.html`

## 示例用法

```
用户: 帮忙分类这个 skills 文件夹：d:/projects/my-skills
Claude: [执行扫描 → 分类 → 生成报告]

用户: 这个 skill 应该归于什么类别？分析 d:/skills/new-skill
Claude: [读取 SKILL.md → 分析关键词 → 返回分类结果]
```

## 大规模扫描

| Skills 数量 | 建议方式 |
|------------|---------|
| < 50 个 | 一次性扫描 |
| 50-100 个 | 分批处理（默认每批 20 个） |
| > 100 个 | 仅读取 description 字段 |

## 注意事项

1. **文件命名兼容**：自动识别 SKILL.md、skill.md 等大小写变体
2. **完整性验证**：扫描后对比目录数量和文件数量，发现遗漏立即报告
3. **Glob 工具限制**：在 Windows 下可能大小写敏感，建议使用脚本扫描
4. **时间自动获取**：脚本自动获取当前系统时间
5. **分类置信度**：低于 0.5 的分类标记为「待确认」
