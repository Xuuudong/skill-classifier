# 🔖 Skill Classifier

> 一个专门针对 OpenCode/Claude Skills 进行智能分类和归类的自动化工具

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## ✨ 它能做什么？

当你的 skills 文件夹里有几十上百个 skill 散落一地时，手动归类是件痛苦的事。

**Skill Classifier** 一键帮你：

| 步骤 | 说明 |
|------|------|
| 🔍 **自动扫描** | 扫描目录下所有 skill，兼容 `SKILL.md`/`skill.md` 等大小写变体，自动补全缺失验证 |
| 🏷️ **智能分类** | 基于关键词权重 + 强制匹配 + 负向规则，自动归入两级分类体系 |
| 📊 **可视化报告** | 生成带饼图、可折叠分类、悬停动画的自包含 HTML 报告 |
| 📁 **归类整理** | 按分类自动把 skills 复制/移动到对应的文件夹 |

---

## 🚀 快速开始

```bash
# 一键：扫描 → 分类 → 生成报告
python scan_skills.py "你的skills目录" --output scan.json
python classify_skills.py scan.json --output classification.json
python subclassify.py classification.json --output final.json
python generate_report.py final.json report.html

# 打开 report.html 即可看到完整的分类报告
```

**30 秒内搞定 50 个 skill 的分类！**

---

## 📊 分类体系

### 6 大一级分类

| 分类 | 图标 | 典型 skill |
|------|:--:|------|
| 开发与自动化 | 🛠️ | playwright-mcp, skill-creator, agent-memory |
| 文档与内容创作 | 📄 | minimax-docx, fireworks-tech-graph, weekly-report |
| 搜索与研究 | 🔍 | tavily-search, deep-research, blogwatcher |
| 金融数据 | 💰 | fund-daily, portfolio-doctor, akshare |
| 通讯与协作 | 💬 | gmail, slack, notion, feishu |
| 其他 | 📦 | weather, marketing tools |

### 18+ 二级细分

AI Agent框架、浏览器自动化、MCP工具、文档生成与编辑、媒体与设计、Web搜索、深度研究、基金投资、量化数据、通讯平台、笔记协作……

> 完整分类规则详见 [`classification-rules.md`](classification-rules.md)

---

## 🎯 为什么选它？

### vs. 手动分类

|  | 手动 | Skill Classifier |
|------|:--:|:--:|
| 50 个 skill | ~30 分钟 | **< 5 秒** |
| 分类一致性 | 主观随意 | **规则统一** |
| 置信度评估 | 无 | **0-1 置信度 + 分类理由** |
| 可视化报告 | 需额外工具 | **自动生成 HTML 报告** |

### 核心特性

- **🔬 三级决策引擎**：强制匹配（精准命中）→ 关键词打分（权重+字段加权）→ 负向规则（排除误判）
- **📈 置信度系统**：每次分类附带 0.3~0.95 置信度，低置信度自动标记「待确认」
- **🛡️ 负向规则**：防止 `gmail` 被误判为"开发工具"、`基金日报` 被误判为"文档工具"
- **📱 响应式报告**：HTML 报告支持移动端，饼图+可折叠分类+悬停上浮动画
- **🔧 边界处理**：大小写兼容、缺失文件 fallback 到 README.md、大规模分批扫描

---

## 🧩 文件结构

```
skill-classifier/
├── SKILL.md                   # Skill 定义文件
├── classification-rules.md    # 分类规则详解
├── scan_skills.py             # 扫描脚本
├── classify_skills.py         # 一级分类（6大类）
├── subclassify.py             # 二级分类（18+子类）
├── generate_report.py         # HTML 报告生成
└── organize_skills.py         # 按分类整理文件夹
```

---

## 📖 示例

### 输入

```
my-skills/
├── playwright-mcp/SKILL.md      # "浏览器自动化..."
├── fund-daily/SKILL.md          # "基金日报，持仓基金数据..."
├── fireworks-tech-graph/SKILL.md # "画架构图、流程图..."
├── agent-memory/SKILL.md        # "AI Agent 持久记忆系统..."
└── ...
```

### 输出

```json
{
  "name": "fund-daily",
  "primary_category": "金融数据",
  "secondary_category": "基金投资",
  "confidence": 0.95,
  "classification_reason": "基金投资"
}
```

### HTML 报告

<div align="center">
  <img src="https://via.placeholder.com/800x450/667eea/ffffff?text=Skills+分类报告+%7C+饼图+%7C+可折叠分类+%7C+悬停动画" alt="报告预览" />
  <p><em>报告包含饼图统计、可折叠分类面板、二级分类标签、分类依据说明</em></p>
</div>

---

## 🔧 高级用法

### 归类整理

```bash
# 预览整理效果
python organize_skills.py final.json -o ./organized --dry-run

# 复制模式（保留原文件）
python organize_skills.py final.json -o ./organized

# 移动模式（删除原文件）
python organize_skills.py final.json -o ./organized --mode move
```

整理后的目录结构：
```
organized/
├── 开发与自动化/
│   ├── AI Agent框架/agent-memory/
│   ├── 浏览器自动化/playwright-mcp/
│   └── 开发工具/skill-classifier/
├── 金融数据/
│   └── 基金投资/fund-daily/
└── organize_summary.md
```

### 大规模扫描

```python
# 分批处理，避免内存溢出
scan_in_batches(skill_files, batch_size=20)
```

---

## 🤝 贡献

欢迎提 Issue 和 PR！分类规则在 `classification-rules.md` 中，可以按需扩充关键词。

---

## 📄 License

MIT © [Xuuudong](https://github.com/Xuuudong)