#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills 分类脚本 - 基于关键词权重的自动分类
支持置信度计算和多字段匹配
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# 分类关键词定义（权重：strong=3, medium=1）
# 注：AI Agent 相关已合并到"开发与自动化"下的二级分类
CATEGORY_KEYWORDS = {
    "开发与自动化": {
        "strong": [
            "api", "sdk", "rest", "graphql", "openapi",
            "code", "development", "developer", "coding",
            "build", "deploy", "deployment", "release",
            "test", "testing", "ci/cd", "pipeline",
            "git", "github", "gitlab", "version control",
            "mcp", "server", "builder", "tool",
            "browser", "playwright", "puppeteer", "selenium",
            "automation", "automated", "automate",
            "workflow", "orchestration",
            "docker", "container", "kubernetes", "k8s",
            "cli", "command", "shell", "terminal",
            "skill", "create skills", "eval", "benchmark",
            # AI Agent 相关（合并至此）
            "agent", "agents", "智能体",
            "memory", "记忆系统", "evolver",
            "self-improving", "proactive", "multi-agent"
        ],
        "medium": [
            "framework", "library", "package",
            "debug", "debugging", "troubleshooting",
            "refactor", "refactoring", "optimize",
            "plugin", "extension", "module",
            "scraping", "scraper", "crawler", "spider",
            "n8n", "zapier",
            "performance", "metrics", "quantitative"
        ]
    },
    "文档与内容创作": {
        "strong": [
            "document", "docx", "word", "docs",
            "pdf", "presentation", "pptx", "powerpoint",
            "design", "art", "creative", "graphics",
            "writing", "content", "text", "editing",
            "image", "video", "media", "audio",
            "markdown", "md", "convert", "format",
            "excel", "xlsx", "spreadsheet", "csv",
            "图表", "graph", "diagram", "visualization",
            "visualize", "chart", "flowchart", "architecture",
            "svg", "png", "export", "render"
        ],
        "medium": [
            "template", "formatting", "layout",
            "typography", "font", "style",
            "generate", "create", "produce",
            "report", "summary", "brief",
            "ui", "ux", "interface",
            "画图", "生成图", "架构图", "流程图"
        ]
    },
    "搜索与研究": {
        "strong": [
            "search", "web-search", "web search",
            "tavily", "brave", "exa", "serper",
            "research", "deep-research", "analysis",
            "knowledge", "graph", "ontology",
            "crawler", "scraping", "scraper",
            "baidu", "google", "bing", "duckduckgo"
        ],
        "medium": [
            "find", "query", "retrieve", "lookup",
            "index", "indexing", "crawl",
            "rss", "feed", "news", "blog",
            "summarize", "summary", "digest"
        ]
    },
    "金融数据": {
        "strong": [
            "finance", "financial", "财经",
            "investment", "invest", "投资",
            "portfolio", "asset", "资产",
            "fund", "stock", "trading", "基金", "股票",
            "retirement", "pension", "养老", "退休",
            "bond", "equity", "债券",
            "tushare", "akshare", "quantitative",
            "盈米", "qieman"
        ],
        "medium": [
            "return", "yield", "profit", "收益",
            "risk", "volatility", "风险",
            "allocation", "diversification", "配置",
            "market", "benchmark", "市场",
            "wealth", "capital", "财富",
            "quant", "量化"
        ]
    },
    "通讯与协作": {
        "strong": [
            "email", "mail", "gmail", "outlook",
            "slack", "discord", "teams", "telegram",
            "notion", "obsidian", "trello", "jira",
            "calendar", "schedule", "meeting",
            "imap", "smtp", "pop3",
            "feishu", "lark", "飞书",
            "notes", "note-taking", "笔记"
        ],
        "medium": [
            "message", "messaging", "chat",
            "collaborate", "collaboration", "team",
            "workspace", "channel", "group",
            "reminder", "task", "todo",
            "contact", "address book"
        ]
    },
    "其他": {
        "strong": [
            "weather", "天气",
            "gaming", "game", "游戏",
            "sonos", "speaker", "音频控制",
            "ads", "advertising", "广告"
        ],
        "medium": [
            "data analysis", "analytics", "数据分析",
            "marketing", "营销",
            "utility", "工具",
            "misc", "其他"
        ]
    }
}

# 负向规则：当检测到这些关键词时，排除该分类
# 格式: {分类名: [排除关键词列表]}
NEGATIVE_KEYWORDS = {
    "开发与自动化": [
        # 文档类关键词不应归入开发
        "docx", "word 文档", "pdf 生成", "pptx", "excel",
        # 金融类关键词不应归入开发
        "基金", "股票", "fund", "stock", "投资组合",
        # 通讯类关键词不应归入开发
        "email", "gmail", "slack", "discord", "飞书"
    ],
    "文档与内容创作": [
        # 纯搜索工具不应归入文档
        "search engine", "搜索引擎", "web search",
        # 纯金融工具不应归入文档
        "stock api", "股票数据", "fund api", "基金数据",
        # 纯通讯工具不应归入文档
        "email client", "邮件客户端", "slack bot"
    ],
    "搜索与研究": [
        # 纯文档生成不应归入搜索
        "create pdf", "生成 pdf", "docx 生成", "word 创建",
        # 纯金融分析不应归入搜索
        "portfolio analysis", "投资组合分析", "fund report",
        # 纯通讯不应归入搜索
        "send email", "发送邮件", "slack message"
    ],
    "金融数据": [
        # 纯开发工具不应归入金融
        "mcp server", "api gateway", "cli tool",
        # 纯文档工具不应归入金融
        "pdf editor", "docx editor", "image converter"
    ],
    "通讯与协作": [
        # 纯开发工具不应归入通讯
        "mcp server", "api tool", "browser automation",
        # 纯文档工具不应归入通讯
        "pdf generator", "docx creator", "chart tool"
    ],
    "其他": []  # 其他类别无负向规则，作为兜底
}

# 强制匹配规则：当检测到这些精确模式时，强制归入指定分类
# 格式: [(正则模式, 分类, 置信度加成, 可读描述)]
# 注意：规则顺序很重要，先匹配到的先生效
FORCE_MATCH_RULES = [
    # ===== Skill 开发工具（最高优先级）=====
    (r'\bskill[- ]?classifier\b', "开发与自动化", 8, "包含 skill-classifier"),
    (r'\bskill[- ]?creator\b', "开发与自动化", 8, "包含 skill-creator"),
    (r'\bskills?\s*分类\b', "开发与自动化", 8, "包含 skills 分类"),
    (r'\bclassify\s+skills?\b', "开发与自动化", 8, "包含 classify skills"),
    (r'\bcreate\s+new\s+skills?\b', "开发与自动化", 8, "包含 create new skills"),
    (r'\boptimize\s+skill\b', "开发与自动化", 8, "包含 optimize skill"),
    (r'\bskill\s+performance\b', "开发与自动化", 8, "包含 skill performance"),

    # ===== API Gateway/开发工具（高优先级）=====
    # 注意：api-gateway 只在名称中匹配，避免误判推荐文本
    # 已在 check_force_match 函数中特殊处理，只在 name 字段匹配
    (r'\bapi[- ]?gateway\b', "开发与自动化", 7, "包含 api-gateway"),
    (r'\bpassthrough\s+proxy\b', "开发与自动化", 7, "包含 passthrough proxy"),

    # ===== 金融相关（高优先级）=====
    (r'\b基金\b[\s一-龥]{0,5}(日报|分析|诊断)\b', "金融数据", 6, "包含 基金日报/分析/诊断"),
    (r'\bfund\s+(report|daily|analysis)\b', "金融数据", 6, "包含 fund report/daily/analysis"),
    (r'\bportfolio\s+(analysis|doctor)\b', "金融数据", 6, "包含 portfolio analysis/doctor"),
    (r'\b投资组合\b[\s一-龥]{0,5}(分析|诊断)\b', "金融数据", 6, "包含 投资组合分析/诊断"),
    (r'\bretirement\s+planner\b', "金融数据", 6, "包含 retirement planner"),
    (r'\b退休规划\b', "金融数据", 6, "包含 退休规划"),
    (r'\b养老规划\b', "金融数据", 6, "包含 养老规划"),
    (r'\btushare\b', "金融数据", 6, "包含 tushare"),
    (r'\bakshare\b', "金融数据", 6, "包含 akshare"),
    (r'\b盈米\b', "金融数据", 6, "包含 盈米"),
    (r'\bqieman\b', "金融数据", 6, "包含 qieman"),
    (r'\b持仓\b[\s一-龥]{0,5}(诊断|分析)\b', "金融数据", 6, "包含 持仓诊断/分析"),
    (r'\b基金组合体检\b', "金融数据", 6, "包含 基金组合体检"),
    # 股票分析相关
    (r'\bstock\s+analysis\b', "金融数据", 7, "包含 stock analysis"),
    (r'\banalyze\s+stocks?\b', "金融数据", 7, "包含 analyze stock(s)"),
    (r'\byahoo\s+finance\b', "金融数据", 7, "包含 yahoo finance"),
    (r'\bstock\s+(watch|watchlist|scanner)\b', "金融数据", 7, "包含 stock watch/watchlist/scanner"),
    (r'\bdividend\s+analysis\b', "金融数据", 7, "包含 dividend analysis"),
    (r'\b股票分析\b', "金融数据", 7, "包含 股票分析"),

    # ===== 文档与内容创作（图表/可视化优先）=====
    (r'\b(create|generate|draw)\s+diagram\b', "文档与内容创作", 5, "包含 create/generate/draw diagram"),
    (r'\bdiagram\s+(create|generate|draw)\b', "文档与内容创作", 5, "包含 diagram create/generate/draw"),
    (r'\b架构图\b', "文档与内容创作", 6, "包含 架构图"),
    (r'\b流程图\b', "文档与内容创作", 6, "包含 流程图"),
    (r'\b可视化\b', "文档与内容创作", 6, "包含 可视化"),
    # AI 文本人性化相关
    (r'\bhumanize\s+(ai\s+)?text\b', "文档与内容创作", 7, "包含 humanize ai text"),
    (r'\bhumanizer\b', "文档与内容创作", 7, "包含 humanizer"),
    (r'\bAI[- ]generated\s+text\b', "文档与内容创作", 7, "包含 AI-generated text"),
    (r'\bbypass\s+AI\s+detection\b', "文档与内容创作", 7, "包含 bypass AI detection"),
    (r'\b画图\b', "文档与内容创作", 6, "包含 画图"),
    (r'\b生成图\b', "文档与内容创作", 6, "包含 生成图"),
    (r'\b(create|generate|edit)\s+docx\b', "文档与内容创作", 5, "包含 create/generate/edit docx"),
    (r'\bdocx\s+(create|generate|edit)\b', "文档与内容创作", 5, "包含 docx create/generate/edit"),
    # PDF 规则：避免匹配文件路径如 pdf.co 或 pdf-co
    (r'\bpdf\s+(create|generate|edit|document)\b', "文档与内容创作", 5, "包含 pdf create/generate/edit/document"),
    (r'\bcreate\s+pdf\b', "文档与内容创作", 5, "包含 create pdf"),
    (r'\bgenerate\s+pdf\b', "文档与内容创作", 5, "包含 generate pdf"),
    (r'\.docx\b', "文档与内容创作", 4, "文件名含 .docx"),
    (r'\.pdf\b', "文档与内容创作", 3, "文件名含 .pdf"),
    (r'\b周报\b', "文档与内容创作", 5, "包含 周报"),

    # ===== MCP/Agent 相关 =====
    (r'\bmcp\s+server\b', "开发与自动化", 4, "包含 mcp server"),
    (r'\bmcp\s+tool\b', "开发与自动化", 4, "包含 mcp tool"),
    (r'\bmcporter\b', "开发与自动化", 5, "包含 mcporter"),
    (r'\bagent\s+memory\b', "开发与自动化", 5, "包含 agent memory"),
    (r'\bmemory\s+system\b', "开发与自动化", 5, "包含 memory system"),
    (r'\bevolver\b', "开发与自动化", 5, "包含 evolver"),
    (r'\bmulti[- ]agent\b', "开发与自动化", 5, "包含 multi-agent"),
    (r'\bplaywright\b', "开发与自动化", 4, "包含 playwright"),
    (r'\bselenium\b', "开发与自动化", 4, "包含 selenium"),
    (r'\bpuppeteer\b', "开发与自动化", 4, "包含 puppeteer"),
    (r'\bskill[- ]creator\b', "开发与自动化", 5, "包含 skill-creator"),
    (r'\bcreate\s+skills?\b', "开发与自动化", 5, "包含 create skills"),

    # ===== 搜索相关（精确匹配，避免误判 API 列表）=====
    (r'\bweb[- ]?search\b', "搜索与研究", 5, "包含 web-search"),
    (r'\bsearch\s+engine\b', "搜索与研究", 5, "包含 search engine"),
    (r'\btavily\b', "搜索与研究", 5, "包含 tavily"),
    (r'\bbrave\s+search\b', "搜索与研究", 5, "包含 brave search"),

    # ===== 通讯相关（高优先级，但需要精确匹配）=====
    (r'\bemail\s+(send|client)\b', "通讯与协作", 7, "包含 email send/client"),
    (r'\bgmail\b', "通讯与协作", 7, "包含 gmail"),
    (r'\bslack\b', "通讯与协作", 7, "包含 slack"),
    (r'\bdiscord\b', "通讯与协作", 7, "包含 discord"),
    # outlook: 排除 "Future Outlook"、"Market Outlook" 等非邮件场景
    (r'\boutlook\s*(app|client|email|邮箱)\b', "通讯与协作", 7, "包含 outlook app/client/email"),
    (r'\bmicrosoft\s+outlook\b', "通讯与协作", 7, "包含 microsoft outlook"),
    (r'\bfeishu\b', "通讯与协作", 7, "包含 feishu"),
    (r'\b飞书\b', "通讯与协作", 7, "包含 飞书"),
    # telegram: 排除 "Telegram format" 等非通讯场景
    (r'\btelegram\s*(bot|api|channel|group)\b', "通讯与协作", 7, "包含 telegram bot/api/channel"),
    (r'\bteams\b', "通讯与协作", 7, "包含 teams"),
    (r'\b邮件\b', "通讯与协作", 7, "包含 邮件"),
    (r'\bnotion\b', "通讯与协作", 4, "包含 notion"),
    (r'\bobsidian\b', "通讯与协作", 4, "包含 obsidian"),
]

# 分类优先级（得分相同时使用）
CATEGORY_PRIORITY = [
    "开发与自动化",
    "金融数据",
    "搜索与研究",
    "通讯与协作",
    "文档与内容创作",
    "其他"
]


def extract_text_fields(content: str) -> Dict[str, str]:
    """从内容中提取各字段"""
    fields = {
        "name": "",
        "description": "",
        "content": content.lower() if content else ""
    }

    if not content:
        return fields

    # 提取 YAML frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            lines = frontmatter.split('\n')
            current_key = None
            current_value = []
            in_multiline = False

            for line in lines:
                stripped = line.strip()

                # 跳过空行和 --- 分隔符
                if not stripped or stripped == '---':
                    continue

                # 检测多行字符串开始 (>- 或 |)
                if ':' in line and not line.startswith(' ') and not line.startswith('\t'):
                    # 保存之前的键值
                    if current_key and current_value:
                        value = ' '.join(current_value).strip()
                        if current_key == 'name':
                            fields["name"] = value.lower()
                        elif current_key == 'description':
                            fields["description"] = value.lower()

                    # 开始新的键
                    key, _, val = stripped.partition(':')
                    current_key = key.strip()
                    val = val.strip()

                    # 处理多行标记
                    if val in ('>-', '|-', '>', '|'):
                        in_multiline = True
                        current_value = []
                    else:
                        # 单行值
                        in_multiline = False
                        current_value = [val.strip('"\'')]

                elif in_multiline and current_key:
                    # 多行内容
                    current_value.append(stripped)

            # 保存最后一个键值
            if current_key and current_value:
                value = ' '.join(current_value).strip()
                if current_key == 'name':
                    fields["name"] = value.lower()
                elif current_key == 'description':
                    fields["description"] = value.lower()

    return fields


def check_negative_rules(text: str, category: str) -> bool:
    """
    检查负向规则
    返回 True 表示该分类应被排除
    """
    text_lower = text.lower()
    negative_kws = NEGATIVE_KEYWORDS.get(category, [])

    for kw in negative_kws:
        if kw.lower() in text_lower:
            return True
    return False


def check_force_match(text: str, name: str = "") -> Tuple[str, float, str]:
    """
    检查强制匹配规则
    返回: (分类, 加成分数, 匹配描述) 或 (None, 0, "")
    """
    for pattern, category, bonus, description in FORCE_MATCH_RULES:
        # 对于 api-gateway 规则，只在 name 字段匹配
        if 'api' in pattern.lower() and 'gateway' in pattern.lower():
            if re.search(pattern, name, re.IGNORECASE):
                return category, bonus, description
        elif re.search(pattern, text, re.IGNORECASE):
            return category, bonus, description
    return None, 0, ""


def calculate_category_score(text: str, keywords: Dict[str, List[str]], category: str) -> Tuple[float, bool]:
    """
    计算某个类别的得分
    返回: (得分, 是否被负向规则排除)
    """
    score = 0.0
    text_lower = text.lower()

    # 先检查负向规则
    if check_negative_rules(text, category):
        return 0.0, True  # 被排除，得分为0

    # 强关键词（权重 3）
    for kw in keywords.get("strong", []):
        if kw.lower() in text_lower:
            score += 3

    # 中关键词（权重 1）
    for kw in keywords.get("medium", []):
        if kw.lower() in text_lower:
            score += 1

    return score, False


def classify_skill(fields: Dict[str, str]) -> Tuple[str, float, str]:
    """
    分类单个 skill
    返回: (类别, 置信度, 理由)
    """
    # 合并所有文本用于强制匹配检测
    all_text = f"{fields.get('name', '')} {fields.get('description', '')} {fields.get('content', '')}"

    # Step 1: 检查强制匹配规则
    skill_name = fields.get('name', '')
    force_category, force_bonus, force_description = check_force_match(all_text, skill_name)
    if force_category and force_bonus >= 5:
        # 强制匹配，高置信度直接返回
        return force_category, 0.95, force_description

    scores = {}
    excluded_categories = set()

    # 计算各字段权重
    field_weights = {
        "description": 2.0,  # description 权重最高
        "name": 1.5,         # name 次高
        "content": 1.0       # 内容基础权重
    }

    # Step 2: 计算各分类得分（同时检查负向规则）
    for category, keywords in CATEGORY_KEYWORDS.items():
        total_score = 0.0

        for field, weight in field_weights.items():
            if fields.get(field):
                score, excluded = calculate_category_score(fields[field], keywords, category)
                if excluded:
                    excluded_categories.add(category)
                    total_score = 0.0
                    break
                total_score += score * weight

        # 如果被负向规则排除，得分为0
        if category in excluded_categories:
            scores[category] = 0.0
        else:
            scores[category] = total_score

    # Step 3: 应用强制匹配加成
    if force_category and force_category not in excluded_categories:
        scores[force_category] += force_bonus

    # Step 4: 找到最高分（排除被负向规则排除的分类）
    valid_scores = {k: v for k, v in scores.items() if k not in excluded_categories}

    if not valid_scores or max(valid_scores.values()) < 2:
        # 没有有效分类或得分太低，归入其他
        return "其他", 0.3, "未找到明确的分类关键词"

    max_score = max(valid_scores.values())

    # 找到最高分类
    best_categories = [cat for cat, score in valid_scores.items() if score == max_score]

    if len(best_categories) > 1:
        # 多个分类同分，按优先级选择
        for cat in CATEGORY_PRIORITY:
            if cat in best_categories:
                best_category = cat
                break
    else:
        best_category = best_categories[0]

    # 计算置信度
    sorted_scores = sorted(valid_scores.values(), reverse=True)
    second_score = sorted_scores[1] if len(sorted_scores) > 1 else 0
    confidence = min(1.0, max_score / (max_score + second_score + 1))

    # 生成理由
    matched_keywords = []
    for kw in CATEGORY_KEYWORDS[best_category].get("strong", []):
        if kw.lower() in fields.get("description", "").lower() or kw.lower() in fields.get("name", "").lower():
            matched_keywords.append(kw)
            if len(matched_keywords) >= 3:
                break

    # 生成更规范的分类理由（简洁风格）
    if matched_keywords:
        # 将关键词转换为简洁描述
        reason = generate_concise_reason(best_category, matched_keywords, fields)
    else:
        # 尝试从中关键词获取
        medium_matched = []
        for kw in CATEGORY_KEYWORDS[best_category].get("medium", []):
            if kw.lower() in fields.get("description", "").lower() or kw.lower() in fields.get("name", "").lower():
                medium_matched.append(kw)
                if len(medium_matched) >= 2:
                    break
        if medium_matched:
            reason = generate_concise_reason(best_category, medium_matched, fields)
        else:
            reason = f"{best_category}工具"

    return best_category, round(confidence, 2), reason


def generate_concise_reason(category: str, keywords: list, fields: dict) -> str:
    """根据关键词生成简洁的分类理由"""
    desc = fields.get("description", "").lower()
    name = fields.get("name", "").lower()
    text = f"{desc} {name}"

    # 分类相关的关键词映射到简洁描述
    reason_map = {
        "开发与自动化": {
            "playwright": "浏览器自动化",
            "browser": "浏览器自动化",
            "selenium": "浏览器自动化",
            "puppeteer": "浏览器自动化",
            "mcp": "MCP 服务器",
            "server": "服务器工具",
            "api": "API 工具",
            "sdk": "SDK 开发工具",
            "agent": "AI agent 框架",
            "memory": "AI agent 记忆系统",
            "evolver": "AI agent 进化引擎",
            "self-improving": "AI agent 自我改进",
            "automation": "自动化工具",
            "automated": "自动化工具",
            "workflow": "工作流自动化",
            "docker": "Docker 容器管理",
            "container": "容器管理",
            "kubernetes": "Kubernetes 容器编排",
            "git": "Git 版本控制",
            "github": "GitHub 开发工具",
            "test": "测试工具",
            "testing": "测试工具",
            "cli": "CLI 命令行工具",
            "skill": "Skill 开发工具",
            "eval": "性能评估工具",
            "benchmark": "基准测试工具"
        },
        "文档与内容创作": {
            "docx": "Word 文档处理",
            "word": "Word 文档处理",
            "document": "文档处理",
            "pdf": "PDF 文档处理",
            "pptx": "PPT 演示文稿",
            "powerpoint": "PPT 演示文稿",
            "excel": "Excel 表格处理",
            "xlsx": "Excel 表格处理",
            "image": "图像处理",
            "video": "视频处理",
            "audio": "音频处理",
            "design": "设计工具",
            "ui": "UI 设计",
            "ux": "UX 设计",
            "graph": "图表绘制",
            "diagram": "流程图绘制",
            "markdown": "Markdown 转换",
            "convert": "格式转换"
        },
        "搜索与研究": {
            "search": "网络搜索",
            "tavily": "AI 搜索",
            "brave": "Brave 搜索",
            "google": "Google 搜索",
            "baidu": "百度搜索",
            "bing": "Bing 搜索",
            "research": "深度研究",
            "analysis": "分析工具",
            "rss": "RSS 订阅监控",
            "blog": "博客监控",
            "watcher": "内容监控",
            "crawler": "网页爬虫"
        },
        "金融数据": {
            "stock": "股票分析",
            "股票": "股票分析",
            "fund": "基金分析",
            "基金": "基金分析",
            "portfolio": "投资组合分析",
            "投资": "投资分析",
            "tushare": "金融数据获取",
            "akshare": "A股数据分析",
            "quant": "量化分析",
            "量化": "量化交易",
            "finance": "金融数据分析",
            "财经": "财经数据",
            "retirement": "退休规划",
            "养老": "养老规划"
        },
        "通讯与协作": {
            "email": "邮件管理",
            "mail": "邮件管理",
            "gmail": "Gmail 邮件",
            "outlook": "Outlook 邮件",
            "slack": "Slack 协作",
            "discord": "Discord 协作",
            "feishu": "飞书协作",
            "飞书": "飞书协作",
            "notion": "Notion 协作",
            "obsidian": "Obsidian 笔记",
            "trello": "Trello 项目管理",
            "jira": "Jira 项目管理",
            "notes": "笔记管理",
            "笔记": "笔记管理"
        },
        "其他": {
            "weather": "天气查询",
            "gaming": "游戏平台",
            "sonos": "智能音箱控制",
            "marketing": "营销工具",
            "analytics": "数据分析"
        }
    }

    # 查找匹配的简洁描述
    cat_map = reason_map.get(category, {})
    for kw in keywords:
        for key, reason in cat_map.items():
            if key in kw.lower() or kw.lower() in key:
                return reason

    # 根据分类返回默认描述
    default_reasons = {
        "开发与自动化": "开发工具",
        "文档与内容创作": "内容创作工具",
        "搜索与研究": "搜索研究工具",
        "金融数据": "金融数据工具",
        "通讯与协作": "通讯协作工具",
        "其他": "工具"
    }
    return default_reasons.get(category, "工具")


def classify_skills(input_path: str, output_path: str = None):
    """分类所有 skills"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    skills = data.get('skills', [])
    classification = {cat: {"count": 0, "skills": []} for cat in CATEGORY_KEYWORDS.keys()}
    statistics = {cat: 0 for cat in CATEGORY_KEYWORDS.keys()}

    for skill in skills:
        # 读取 skill 内容
        skill_file = skill.get('file', '')
        content = ""

        if skill_file and Path(skill_file).exists():
            try:
                with open(skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"警告: 无法读取 {skill_file}: {e}")

        # 提取字段并分类
        fields = extract_text_fields(content)
        if not fields["name"]:
            fields["name"] = skill.get('name', 'unknown')

        category, confidence, reason = classify_skill(fields)

        # 添加到分类结果
        classification[category]["skills"].append({
            "name": skill.get('name', 'unknown'),
            "description": fields.get("description", "") if fields.get("description") else "",
            "file": skill_file,
            "confidence": confidence,
            "classification_reason": reason
        })
        classification[category]["count"] += 1
        statistics[category] += 1

    # 构建输出
    result = {
        "scan_time": data.get('scan_time', datetime.now().isoformat()),
        "source_path": data.get('source_path', ''),
        "total_skills": len(skills),
        "total_directories": data.get('total_directories', len(skills)),
        "validation": data.get('validation', {"passed": True, "message": ""}),
        "classification": classification,
        "statistics": statistics
    }

    # 输出
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"分类结果已保存到: {output_path}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python classify_skills.py <扫描结果json> [--output 输出路径]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = None

    if len(sys.argv) > 3 and sys.argv[2] == '--output':
        output_path = sys.argv[3]

    classify_skills(input_path, output_path)


if __name__ == '__main__':
    main()
