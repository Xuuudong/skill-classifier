# 分类规则参考

本文档定义了 skill 分类的详细规则，包括一级分类、二级分类和分类依据。

## 一级分类

| 类别 | 图标 | 颜色 | 说明 | 核心特征 |
|------|------|------|------|---------|
| 开发与自动化 | 🛠️ | 蓝色 | 软件开发工具、自动化脚本、AI Agent 框架 | 代码开发、流程自动化、智能体构建 |
| 文档与内容创作 | 📄 | 粉色 | 文档生成、媒体处理、格式转换 | 文件输出、内容创作、可视化 |
| 搜索与研究 | 🔍 | 绿色 | 网络搜索、信息采集、深度分析 | 信息检索、内容监控、研究整合 |
| 金融数据 | 💰 | 青色 | 股票行情、量化分析、金融数据 API | 投资分析、数据获取、风险监控 |
| 通讯与协作 | 💬 | 紫色 | 邮件收发、即时通讯、笔记协作 | 消息传递、团队协作、知识管理 |
| 其他 | 📦 | 灰色 | 未归入以上类别的工具 | 天气、智能家居、营销等 |

---

## 二级分类详解

### 1. 开发与自动化

#### MCP与浏览器自动化

**说明**：MCP 服务器构建与管理、浏览器自动化控制、网页抓取工具

**分类依据**：
- 描述中包含 playwright、browser、mcp、server、selenium、puppeteer
- 功能涉及网页导航、表单填写、截图、DOM 操作
- MCP 协议相关的服务器或工具构建

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| playwright-mcp | 通过 Playwright MCP 进行浏览器自动化、导航、表单填写 | Playwright 浏览器自动化 |
| browser-use | 浏览器自动化工具，支持 Web 测试、表单填写、截图 | 浏览器自动化 |
| mcporter | MCP 服务器 CLI 工具，用于调用、配置和管理 MCP 服务器 | MCP 服务器管理 |
| api-gateway | 连接 100+ API 的网关，支持 OAuth 托管 | API 连接和管理 |

#### AI Agent框架

**说明**：AI Agent 记忆系统、自我进化引擎、多智能体协作框架

**分类依据**：
- 描述中包含 agent、memory、evolver、self-improving、multi-agent
- 功能涉及持久记忆、经验学习、跨会话追踪
- 智能体自我改进、能力进化相关

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| agent-memory | AI 代理持久记忆系统，支持记住事实、从经验中学习 | AI agent 记忆系统 |
| evolver | AI 代理自我进化引擎，分析运行历史并自动改进 | AI agent 自我进化引擎 |
| memory-manager | AI 代理的本地内存管理，支持压缩检测、快照 | AI agent 记忆管理 |
| capability-evolver | AI 代理自我进化引擎，分析运行历史并应用进化协议 | AI agent 自我进化引擎 |

---

### 2. 文档与内容创作

#### 文档生成与编辑

**说明**：Word/PDF/PPT/Excel 文档的创建、编辑、格式转换

**分类依据**：
- 描述中包含 docx、pdf、word、pptx、xlsx、excel、document
- 功能涉及文档创建、内容编辑、格式转换
- 支持 Word、PDF、PPT、Excel 等办公文档

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| word-docx | 创建、检查和编辑 Microsoft Word 文档 | Word 文档处理 |
| pdf | 综合 PDF 处理工具包，支持文本提取、创建、合并拆分 | PDF 文档处理 |
| excel-xlsx | 创建、检查和编辑 Excel 工作簿和 XLSX 文件 | Excel 文档处理 |
| markdown-converter | 将 PDF、Word、Excel、HTML 等文档转换为 Markdown | 文档格式转换 |

#### 媒体与设计

**说明**：图像生成、视频处理、音频转文字、UI/UX 设计

**分类依据**：
- 描述中包含 image、video、audio、design、ui、ux、whisper
- 功能涉及图像生成、视频处理、音频转录
- UI/UX 设计指导和最佳实践

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| openai-image-gen | 通过 OpenAI Images API 批量生成图像 | 图像生成 |
| video-frames | 使用 ffmpeg 从视频中提取帧或短片 | 视频处理 |
| openai-whisper | 通过 OpenAI API 转录音频文件 | 音频转文字 |
| ui-ux-pro-max | UI/UX 设计智能和实现指导 | UI/UX 设计 |

---

### 3. 搜索与研究

#### Web搜索

**说明**：搜索引擎集成、多源检索、网络搜索 API

**分类依据**：
- 描述中包含 search、tavily、brave、google、baidu、bing、duckduckgo
- 功能涉及网页搜索、新闻搜索、图片搜索
- 多搜索引擎聚合或特定搜索引擎集成

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| tavily-search | AI 优化的网页搜索 API，支持新闻、图片搜索 | AI 网络搜索 |
| brave-search | 通过 Brave Search API 进行网络搜索和内容提取 | 网络搜索 |
| web-search | 使用 DuckDuckGo API 进行网页、新闻、图片、视频搜索 | 网络搜索 |
| multi-search-engine | 集成 17 个搜索引擎的搜索工具 | 多引擎搜索 |

#### 深度研究

**说明**：信息整合分析、研究报告生成、RSS/博客监控

**分类依据**：
- 描述中包含 research、analysis、rss、blog、watcher、monitor
- 功能涉及深度研究、信息整合、内容监控
- RSS 订阅、博客更新追踪

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| deep-research-pro | 多源深度研究 agent，网络搜索并生成引用报告 | 深度研究 |
| blogwatcher | 监控博客和 RSS/Atom 订阅更新 | 博客/RSS 监控 |
| news-summary | 从国际 RSS 源获取新闻并生成摘要 | 新闻研究 |

---

### 4. 金融数据

#### 股票分析

**说明**：股票行情查询、技术分析、自选股监控

**分类依据**：
- 描述中包含 stock、股票、watcher、quote、行情、analysis
- 功能涉及股票报价、技术指标、自选股管理
- 股票市场监控和预警

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| stock-analysis | 股票和加密货币分析，包含组合管理、监视列表 | 股票分析 |
| stock-market-pro | Yahoo Finance 股票分析，含报价、基本面、图表 | 股票行情分析 |
| stock-watcher | 自选股管理和监控工具，数据来源同花顺 | 股票监控 |

#### 量化数据

**说明**：金融数据 API、量化分析平台、历史数据获取

**分类依据**：
- 描述中包含 tushare、akshare、quant、量化、finance、金融数据
- 功能涉及金融数据获取、量化策略回测
- 支持 A 股、期货、债券等多品种数据

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| akshare | A 股量化数据分析工具，获取行情、财务数据、板块信息 | A股量化分析 |
| tushare-finance | 获取中国金融市场数据，支持股票、基金、期货、债券等 220+ 接口 | 金融数据获取 |

---

### 5. 通讯与协作

#### 通讯平台

**说明**：邮件收发、Slack/Discord/飞书等即时通讯平台

**分类依据**：
- 描述中包含 email、gmail、slack、discord、feishu、outlook、imap、smtp
- 功能涉及邮件读取、发送、管理
- 即时通讯平台消息管理

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| gmail | Gmail API 集成，读取、发送和管理邮件 | Gmail 邮件管理 |
| slack | 控制 Slack 消息、反应、置顶等功能 | Slack 协作 |
| discord | Discord 消息管理、反应、投票、线程、表情包等操作 | Discord 协作 |
| himalaya | CLI 邮件管理工具，支持 IMAP/SMTP 协议 | 邮件管理 |

#### 笔记协作

**说明**：Notion/Obsidian 笔记、Trello/Jira 项目管理

**分类依据**：
- 描述中包含 notion、obsidian、trello、jira、notes、笔记
- 功能涉及笔记创建、编辑、搜索
- 项目管理、看板、任务跟踪

**典型技能**：
| 技能名称 | 描述 | 分类依据 |
|---------|------|---------|
| notion | Notion API 用于创建和管理页面、数据库和块 | Notion 协作 |
| trello | 管理 Trello 看板、列表和卡片 | Trello 项目管理 |
| apple-notes | 通过 memo CLI 管理 Apple Notes，支持创建、查看、编辑 | 笔记管理 |
| obsidian | 操作 Obsidian 知识库的 Markdown 笔记工具 | Markdown 笔记 |

---

### 6. 其他

不设二级分类。

**归入此类的情况**：

| 类型 | 关键词 | 示例 |
|------|-------|------|
| 天气查询 | weather | weather-1: 获取当前天气和预报 |
| 智能家居 | sonos, speaker | sonoscli: 控制 Sonos 音箱设备 |
| 营销工具 | marketing | marketing-mode: 整合 23 种营销技能 |
| 数据分析 | data analysis, analytics | data-analyst: 数据可视化和报告生成 |
| 使用统计 | usage, statistics | model-usage: 获取模型使用成本数据 |

---

## 分类算法

### 一级分类得分计算

```
得分 = Σ(强关键词匹配 × 3) + Σ(中关键词匹配 × 1)
```

**字段权重**：
- description: × 2.0（最重要）
- name: × 1.5
- content: × 1.0

**决策规则**：
1. 得分 ≥ 2：归类到该类别
2. 多类别同分：按优先级选择
   - 开发与自动化 > 金融数据 > 搜索与研究 > 通讯与协作 > 文档与内容创作 > 其他
3. 所有得分 < 2：放入「其他」

### 二级分类判定

```
二级得分 = Σ(二级关键词匹配 × 权重)
```

选择得分最高的二级分类。

### 置信度计算

```
置信度 = 最高分 / (最高分 + 次高分 + 1)
```

| 置信度范围 | 标记 |
|-----------|------|
| ≥ 0.7 | 高置信度 |
| 0.5 - 0.7 | 中等置信度 |
| < 0.5 | 低置信度，标记「待确认」 |

---

## 输出格式

```json
{
  "name": "playwright-mcp",
  "description": "通过 Playwright MCP 进行浏览器自动化",
  "primary_category": "开发与自动化",
  "secondary_category": "MCP与浏览器自动化",
  "confidence": 0.85,
  "classification_reason": "匹配关键词: playwright, mcp, browser",
  "secondary_reason": "匹配: playwright, browser"
}
```

---

## 二级分类高级规则

### 二级负向规则

当检测到特定关键词时，排除该二级分类：

| 一级分类 | 二级分类 | 排除关键词 |
|---------|---------|-----------|
| 开发与自动化 | AI Agent框架 | playwright, selenium, browser, 浏览器, mcp server, api gateway |
| 开发与自动化 | 浏览器自动化 | agent memory, 记忆系统, evolver, self-improving, mcp server, api tool |
| 开发与自动化 | MCP工具 | agent memory, 记忆系统, browser automation, playwright, selenium, 浏览器自动化 |
| 文档与内容创作 | 媒体与设计 | docx, word 文档, pdf 文档, excel, 表格, pptx, powerpoint, 演示文稿 |
| 文档与内容创作 | 文档生成与编辑 | 图像生成, 视频处理, 音频转换, image generation, video processing, audio, whisper |
| 搜索与研究 | 深度研究 | search engine, 搜索引擎, tavily, brave search, google search, web search api |
| 搜索与研究 | Web搜索 | deep research, 深度研究, research analysis, rss monitor, blog watcher, 信息整合 |
| 金融数据 | 基金投资 | tushare, akshare, quant api, 量化接口, historical data, 历史数据获取 |
| 金融数据 | 量化数据 | portfolio, 投资组合, retirement, 退休规划, fund report, 基金日报, 持仓诊断 |
| 通讯与协作 | 通讯平台 | notion, obsidian, 笔记, 知识库, 项目管理, kanban, trello, jira |
| 通讯与协作 | 笔记协作 | email, 邮件, gmail, slack, discord, 即时通讯, messaging |

### 二级强制匹配规则

当匹配到精确模式时，强制归入指定二级分类（置信度 0.95）：

```
开发与自动化:
  - \bagent\b.*\bmemory\b → AI Agent框架
  - \bevolver\b → AI Agent框架
  - \bmulti[- ]agent\b → AI Agent框架
  - \bplaywright\b → 浏览器自动化
  - \bselenium\b → 浏览器自动化
  - \bbrowser[- ]?use\b → 浏览器自动化
  - \bmcp\b.*\bserver\b → MCP工具
  - \bmcporter\b → MCP工具

文档与内容创作:
  - \b架构图\b → 媒体与设计
  - \b流程图\b → 媒体与设计
  - \b可视化\b → 媒体与设计
  - \b画图\b → 媒体与设计
  - \bwhisper\b → 媒体与设计
  - \bdocx\b.*\b(create|generate|edit)\b → 文档生成与编辑
  - \bpdf\b.*\b(create|generate|edit)\b → 文档生成与编辑
  - \b周报\b → 文档生成与编辑

搜索与研究:
  - \bdeep[- ]research\b → 深度研究
  - \brss\b.*\b(monitor|watcher)\b → 深度研究
  - \btavily\b → Web搜索
  - \b搜索引擎\b → Web搜索

金融数据:
  - \b基金\b.*\b(日报|分析|诊断)\b → 基金投资
  - \bportfolio\b.*\b(analysis|doctor)\b → 基金投资
  - \b退休规划\b → 基金投资
  - \b盈米\b → 基金投资
  - \btushare\b → 量化数据
  - \bakshare\b → 量化数据
  - \b量化\b.*\b(数据|接口)\b → 量化数据

通讯与协作:
  - \bgmail\b → 通讯平台
  - \bslack\b → 通讯平台
  - \b飞书\b → 通讯平台
  - \bnotion\b → 笔记协作
  - \bobsidian\b → 笔记协作
  - \b笔记\b → 笔记协作
```

### 二级置信度计算

```
置信度 = 最高分 / (最高分 + 次高分 + 1)
```

| 置信度范围 | 标记 |
|-----------|------|
| ≥ 0.7 | 高置信度 |
| 0.5 - 0.7 | 中等置信度 |
| < 0.5 | 低置信度，标记「待确认」 |

强制匹配命中时，置信度固定为 0.95。

---

## 边界情况处理

### 跨领域 Skill

优先判断主要功能：

| 技能 | 一级分类 | 二级分类 | 理由 |
|-----|---------|---------|------|
| weekly-report | 文档与内容创作 | 文档生成与编辑 | 最终输出为 PDF 文档 |
| fund-daily | 金融数据 | 股票分析 | 核心功能是基金数据分析 |
| deep-research-pro | 搜索与研究 | 深度研究 | 主要功能是信息整合研究 |
| agent-memory | 开发与自动化 | AI Agent框架 | 核心是 Agent 记忆系统 |

### AI 相关工具归类

| 类型 | 一级分类 | 二级分类 | 示例 |
|-----|---------|---------|------|
| Agent/智能体/记忆 | 开发与自动化 | AI Agent框架 | agent-memory, evolver |
| LLM API 工具 | 开发与自动化 | MCP与浏览器自动化 | claude-api |
| 文档生成 AI | 文档与内容创作 | 文档生成与编辑 | ai-ppt-generator |
| 搜索增强 AI | 搜索与研究 | Web搜索 | tavily-ai-search |
