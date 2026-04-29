#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills 二级分类脚本 - 基于一级分类结果进行细分
包含优先级规则、负向规则、强制匹配和置信度计算
"""

import json
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# 二级分类关键词定义（权重：strong=3, medium=1）
# 包含优先级和特殊规则
SECONDARY_CATEGORIES = {
    "开发与自动化": {
        # 优先级：AI Agent框架 > 浏览器自动化 > 开发工具
        "priority": ["AI Agent框架", "浏览器自动化", "开发工具"],
        "categories": {
            "AI Agent框架": {
                "strong": [
                    "agent", "agents", "智能体", "memory", "记忆",
                    "evolver", "evolving", "self-improving",
                    "multi-agent", "proactive", "learning", "进化", "反思",
                    "capability", "byteRover", "记忆系统"
                ],
                "medium": [
                    "context", "persistent", "knowledge", "communication", "protocol"
                ]
            },
            "浏览器自动化": {
                "strong": [
                    "playwright", "puppeteer", "selenium", "browser",
                    "headless", "navigate", "click", "form fill",
                    "stagehand", "browser-use", "browser automation",
                    "网页", "浏览器"
                ],
                "medium": [
                    "web", "page", "scrape", "extract", "dom", "screenshot"
                ]
            },
            "开发工具": {
                "strong": [
                    "mcp", "mcporter", "mcp server",
                    "tool builder", "api gateway", "api tool",
                    "skill classifier", "skill creator", "skills 分类",
                    "skill development", "create skills", "skill performance",
                    "cli tool", "command line", "sdk", "developer tool"
                ],
                "medium": [
                    "server", "builder", "api", "framework"
                ]
            }
        }
    },
    "文档与内容创作": {
        # 优先级：媒体与设计 > 文档生成与编辑（图表/可视化优先归设计）
        "priority": ["媒体与设计", "文档生成与编辑"],
        "categories": {
            "媒体与设计": {
                "strong": [
                    "image", "video", "audio", "图像", "视频", "音频",
                    "graph", "diagram", "chart", "可视化", "visualization",
                    "whisper", "speech", "图像生成", "视频生成", "graphic",
                    "画图", "生成图", "架构图", "流程图", "svg", "png"
                ],
                "medium": [
                    "design", "ui", "ux", "render", "visual", "creative",
                    "generate-image", "media", "art"
                ]
            },
            "文档生成与编辑": {
                "strong": [
                    "docx", "word", "pdf", "pptx", "powerpoint", "ppt",
                    "excel", "xlsx", "spreadsheet", "document", "文档",
                    "表格", "演示", "报告", "合同"
                ],
                "medium": [
                    "create", "edit", "template", "format", "fill",
                    "腾讯文档", "convert"
                ]
            }
        }
    },
    "搜索与研究": {
        # 优先级：深度研究 > Web搜索
        "priority": ["深度研究", "Web搜索"],
        "categories": {
            "深度研究": {
                "strong": [
                    "deep-research", "research", "analysis", "analyze",
                    "rss", "blog", "watcher", "monitor", "研究", "分析",
                    "整合", "报告", "追踪"
                ],
                "medium": [
                    "summary", "summarize", "digest", "report", "investigate"
                ]
            },
            "Web搜索": {
                "strong": [
                    "search", "tavily", "brave", "google", "baidu", "bing",
                    "duckduckgo", "exa", "serper", "搜索引擎", "搜索",
                    "web search", "multi-search"
                ],
                "medium": [
                    "web", "query", "find", "lookup", "retrieve"
                ]
            }
        }
    },
    "金融数据": {
        # 优先级：基金投资 > 量化数据
        "priority": ["基金投资", "量化数据"],
        "categories": {
            "基金投资": {
                "strong": [
                    "fund", "基金", "portfolio", "持仓", "资产配置",
                    "retirement", "养老", "退休", "财务自由",
                    "investment", "投资", "诊断", "doctor", "盈米", "qieman"
                ],
                "medium": [
                    "return", "收益", "风险", "allocation", "配置"
                ]
            },
            "量化数据": {
                "strong": [
                    "tushare", "akshare", "quant", "量化",
                    "finance api", "金融数据", "数据源", "数据获取",
                    "historical data", "历史数据"
                ],
                "medium": [
                    "stock", "股票", "market", "行情", "api"
                ]
            }
        }
    },
    "通讯与协作": {
        # 优先级：通讯平台 > 笔记协作
        "priority": ["通讯平台", "笔记协作"],
        "categories": {
            "通讯平台": {
                "strong": [
                    "email", "mail", "gmail", "outlook", "imap", "smtp",
                    "slack", "discord", "teams", "telegram", "feishu", "飞书",
                    "邮件", "消息", "即时通讯", "messaging"
                ],
                "medium": [
                    "send", "receive", "message", "chat", "通知", "channel"
                ]
            },
            "笔记协作": {
                "strong": [
                    "notion", "obsidian", "trello", "jira", "notes",
                    "笔记", "项目管理", "知识库", "apple notes",
                    "workspace", "kanban", "看板"
                ],
                "medium": [
                    "page", "database", "card", "board", "task", "todo"
                ]
            }
        }
    },
    "其他": {
        "priority": [],
        "categories": {}
    }
}

# 负向规则：当检测到这些关键词时，排除该二级分类
# 格式: {一级分类: {二级分类: [排除关键词列表]}}
SECONDARY_NEGATIVE_KEYWORDS = {
    "开发与自动化": {
        "AI Agent框架": [
            "playwright", "selenium", "browser", "浏览器",
            "mcp server", "api gateway"
        ],
        "浏览器自动化": [
            "agent memory", "记忆系统", "evolver", "self-improving",
            "mcp server", "api tool"
        ],
        "开发工具": [
            "agent memory", "记忆系统", "browser automation",
            "playwright", "selenium", "浏览器自动化"
        ]
    },
    "文档与内容创作": {
        "媒体与设计": [
            "docx", "word 文档", "pdf 文档", "excel", "表格",
            "pptx", "powerpoint", "演示文稿"
        ],
        "文档生成与编辑": [
            "图像生成", "视频处理", "音频转换", "image generation",
            "video processing", "audio", "whisper"
        ]
    },
    "搜索与研究": {
        "深度研究": [
            "search engine", "搜索引擎", "tavily", "brave search",
            "google search", "web search api"
        ],
        "Web搜索": [
            "deep research", "深度研究", "research analysis",
            "rss monitor", "blog watcher", "信息整合"
        ]
    },
    "金融数据": {
        "基金投资": [
            "tushare", "akshare", "quant api", "量化接口",
            "historical data", "历史数据获取"
        ],
        "量化数据": [
            "portfolio", "投资组合", "retirement", "退休规划",
            "fund report", "基金日报", "持仓诊断"
        ]
    },
    "通讯与协作": {
        "通讯平台": [
            "notion", "obsidian", "笔记", "知识库",
            "项目管理", "kanban", "trello", "jira"
        ],
        "笔记协作": [
            "email", "邮件", "gmail", "slack", "discord",
            "即时通讯", "messaging"
        ]
    }
}

# 强制匹配规则：当检测到这些精确模式时，强制归入指定二级分类
# 格式: {一级分类: [(正则模式, 二级分类, 置信度加成, 人类可读描述)]}
SECONDARY_FORCE_MATCH_RULES = {
    "开发与自动化": [
        # Skill 开发工具（最高优先级）
        (r'\bskill[- ]?classifier\b', "开发工具", 6, "包含 skill-classifier"),
        (r'\bskill[- ]?creator\b', "开发工具", 6, "包含 skill-creator"),
        (r'\bskills?\b.*\b分类\b', "开发工具", 6, "包含 skills 分类"),
        (r'\bclassify\b.*\bskills?\b', "开发工具", 6, "包含 classify skills"),
        (r'\bcreate\s+new\s+skills?\b', "开发工具", 6, "包含 create new skill(s)"),
        (r'\bskill\b.*\bperformance\b', "开发工具", 6, "包含 skill performance"),
        # API Gateway（只在名称中匹配）
        (r'\bapi[- ]?gateway\b', "开发工具", 6, "包含 api-gateway"),
        # AI Agent 框架
        (r'\bagent\b.*\bmemory\b', "AI Agent框架", 5, "包含 agent memory"),
        (r'\bmemory\b.*\bsystem\b', "AI Agent框架", 5, "包含 memory system"),
        (r'\bself[- ]improving\b', "AI Agent框架", 5, "包含 self-improving"),
        (r'\bevolver\b', "AI Agent框架", 5, "包含 evolver"),
        (r'\bmulti[- ]agent\b', "AI Agent框架", 5, "包含 multi-agent"),
        # 浏览器自动化
        (r'\bplaywright\b', "浏览器自动化", 5, "包含 playwright"),
        (r'\bselenium\b', "浏览器自动化", 5, "包含 selenium"),
        (r'\bpuppeteer\b', "浏览器自动化", 5, "包含 puppeteer"),
        (r'\bbrowser[- ]?use\b', "浏览器自动化", 5, "包含 browser-use"),
        (r'\bbrowser\s+automation\b', "浏览器自动化", 5, "包含 browser automation"),
        # 开发工具（MCP、CLI、SDK）
        (r'\bmcp\b.*\bserver\b', "开发工具", 5, "包含 mcp server"),
        (r'\bmcporter\b', "开发工具", 5, "包含 mcporter"),
    ],
    "文档与内容创作": [
        (r'\bdiagram\b.*\b(create|generate|draw)\b', "媒体与设计", 5, "包含 diagram create/generate/draw"),
        (r'\b架构图\b', "媒体与设计", 5, "包含 架构图"),
        (r'\b流程图\b', "媒体与设计", 5, "包含 流程图"),
        (r'\b可视化\b', "媒体与设计", 5, "包含 可视化"),
        (r'\b画图\b', "媒体与设计", 5, "包含 画图"),
        (r'\bgraph\b.*\b(generate|create|draw)\b', "媒体与设计", 5, "包含 graph generate/create/draw"),
        (r'\bimage\b.*\b(generate|create)\b', "媒体与设计", 5, "包含 image generate/create"),
        (r'\bvideo\b.*\b(process|edit)\b', "媒体与设计", 5, "包含 video process/edit"),
        (r'\bwhisper\b', "媒体与设计", 5, "包含 whisper"),
        (r'\bdocx\b.*\b(create|generate|edit)\b', "文档生成与编辑", 5, "包含 docx create/generate/edit"),
        # PDF 规则：避免匹配文件路径如 pdf.co 或 pdf-co
        (r'\bpdf\s+(create|generate|edit|document)\b', "文档生成与编辑", 5, "包含 pdf create/generate/edit/document"),
        (r'\bcreate\s+pdf\b', "文档生成与编辑", 5, "包含 create pdf"),
        (r'\bgenerate\s+pdf\b', "文档生成与编辑", 5, "包含 generate pdf"),
        (r'\.docx\b', "文档生成与编辑", 4, "包含 .docx 文件扩展名"),
        (r'\.pdf\b', "文档生成与编辑", 3, "包含 .pdf 文件扩展名"),
        (r'\bword\s+document\b', "文档生成与编辑", 5, "包含 word document"),
        (r'\bexcel\b', "文档生成与编辑", 4, "包含 excel"),
        (r'\bxlsx\b', "文档生成与编辑", 4, "包含 xlsx"),
        (r'\bpptx\b', "文档生成与编辑", 4, "包含 pptx"),
        (r'\bpowerpoint\b', "文档生成与编辑", 4, "包含 powerpoint"),
        (r'\b周报\b', "文档生成与编辑", 5, "包含 周报"),
        (r'\breport\b.*\b(pdf|docx)\b', "文档生成与编辑", 5, "包含 report pdf/docx"),
    ],
    "搜索与研究": [
        (r'\bdeep[- ]research\b', "深度研究", 5, "包含 deep-research"),
        (r'\bresearch\b.*\banalysis\b', "深度研究", 5, "包含 research analysis"),
        (r'\brss\b.*\b(monitor|watcher)\b', "深度研究", 5, "包含 rss monitor/watcher"),
        (r'\bblog\b.*\bwatcher\b', "深度研究", 5, "包含 blog watcher"),
        (r'\b研究\b.*\b分析\b', "深度研究", 5, "包含 研究 分析"),
        (r'\bweb[- ]?search\b', "Web搜索", 5, "包含 web-search"),
        (r'\bsearch\b.*\bengine\b', "Web搜索", 5, "包含 search engine"),
        (r'\btavily\b', "Web搜索", 5, "包含 tavily"),
        (r'\bbrave\b.*\bsearch\b', "Web搜索", 5, "包含 brave search"),
        (r'\b搜索引擎\b', "Web搜索", 5, "包含 搜索引擎"),
    ],
    "金融数据": [
        (r'\bfund\b.*\b(report|daily|analysis)\b', "基金投资", 5, "包含 fund report/daily/analysis"),
        (r'\b基金\b.*\b(日报|分析|诊断)\b', "基金投资", 5, "包含 基金日报/分析/诊断"),
        (r'\bportfolio\b.*\b(analysis|doctor)\b', "基金投资", 5, "包含 portfolio analysis/doctor"),
        (r'\b投资组合\b.*\b(分析|诊断)\b', "基金投资", 5, "包含 投资组合 分析/诊断"),
        (r'\bretirement\b.*\bplanner\b', "基金投资", 5, "包含 retirement planner"),
        (r'\b退休规划\b', "基金投资", 5, "包含 退休规划"),
        (r'\b盈米\b', "基金投资", 5, "包含 盈米"),
        (r'\bqieman\b', "基金投资", 5, "包含 qieman"),
        (r'\btushare\b', "量化数据", 5, "包含 tushare"),
        (r'\bakshare\b', "量化数据", 5, "包含 akshare"),
        (r'\bquant\b.*\bapi\b', "量化数据", 5, "包含 quant api"),
        (r'\b量化\b.*\b(数据|接口)\b', "量化数据", 5, "包含 量化 数据/接口"),
    ],
    "通讯与协作": [
        (r'\bemail\b.*\b(send|client)\b', "通讯平台", 6, "包含 email send/client"),
        (r'\bgmail\b', "通讯平台", 6, "包含 gmail"),
        (r'\bslack\b', "通讯平台", 6, "包含 slack"),
        (r'\bdiscord\b', "通讯平台", 6, "包含 discord"),
        (r'\boutlook\b', "通讯平台", 6, "包含 outlook"),
        (r'\b飞书\b', "通讯平台", 6, "包含 飞书"),
        (r'\bfeishu\b', "通讯平台", 6, "包含 feishu"),
        (r'\b邮件\b', "通讯平台", 6, "包含 邮件"),
        (r'\bnotion\b', "笔记协作", 5, "包含 notion"),
        (r'\bobsidian\b', "笔记协作", 5, "包含 obsidian"),
        (r'\btrello\b', "笔记协作", 5, "包含 trello"),
        (r'\bjira\b', "笔记协作", 5, "包含 jira"),
        (r'\b笔记\b', "笔记协作", 5, "包含 笔记"),
        (r'\b知识库\b', "笔记协作", 5, "包含 知识库"),
    ]
}


def check_secondary_negative_rules(text: str, primary_category: str, secondary_category: str) -> bool:
    """
    检查二级分类负向规则
    返回 True 表示该二级分类应被排除
    """
    text_lower = text.lower()
    negative_rules = SECONDARY_NEGATIVE_KEYWORDS.get(primary_category, {})
    negative_kws = negative_rules.get(secondary_category, [])

    for kw in negative_kws:
        if kw.lower() in text_lower:
            return True
    return False


def check_secondary_force_match(text: str, primary_category: str, name: str = "") -> Tuple[Optional[str], float, str]:
    """
    检查二级分类强制匹配规则
    返回: (二级分类, 加成分数, 人类可读描述) 或 (None, 0, "")
    """
    rules = SECONDARY_FORCE_MATCH_RULES.get(primary_category, [])

    for pattern, secondary_cat, bonus, description in rules:
        # 对于 api-gateway 规则，只在 name 字段匹配
        if 'api' in pattern.lower() and 'gateway' in pattern.lower():
            if re.search(pattern, name, re.IGNORECASE):
                return secondary_cat, bonus, description
        elif re.search(pattern, text, re.IGNORECASE):
            return secondary_cat, bonus, description
    return None, 0, ""


def calculate_secondary_score(text: str, keywords: Dict[str, List[str]],
                               primary_category: str, secondary_category: str) -> Tuple[float, bool]:
    """
    计算二级分类得分
    返回: (得分, 是否被负向规则排除)
    """
    score = 0.0
    text_lower = text.lower()

    # 先检查负向规则
    if check_secondary_negative_rules(text, primary_category, secondary_category):
        return 0.0, True  # 被排除，得分为0

    for kw in keywords.get("strong", []):
        if kw.lower() in text_lower:
            score += 3

    for kw in keywords.get("medium", []):
        if kw.lower() in text_lower:
            score += 1

    return score, False


def calculate_secondary_confidence(scores: Dict[str, float], best_category: str) -> float:
    """
    计算二级分类置信度
    公式: 最高分 / (最高分 + 次高分 + 1)
    """
    if not scores:
        return 0.0

    sorted_scores = sorted(scores.values(), reverse=True)
    max_score = sorted_scores[0]
    second_score = sorted_scores[1] if len(sorted_scores) > 1 else 0

    if max_score == 0:
        return 0.0

    confidence = max_score / (max_score + second_score + 1)
    return min(1.0, confidence)


def apply_special_rules(primary_category: str, text: str, scores: Dict[str, float]) -> Optional[str]:
    """应用特殊规则处理模糊情况"""

    if primary_category == "文档与内容创作":
        # 图表/可视化优先归媒体与设计
        visual_keywords = ["graph", "diagram", "chart", "可视化", "visualization", "架构图", "流程图"]
        for kw in visual_keywords:
            if kw.lower() in text.lower():
                return "媒体与设计"

        # PDF + document 优先归文档生成与编辑
        if "pdf" in text.lower() and "document" in text.lower():
            return "文档生成与编辑"

    return None


def subclassify_skill(name: str, description: str, primary_category: str) -> Tuple[str, str, float]:
    """
    二级分类
    返回: (二级分类, 分类理由, 置信度)
    """
    text = f"{name} {description}".lower()

    if primary_category not in SECONDARY_CATEGORIES:
        return "", "无二级分类", 0.0

    cat_config = SECONDARY_CATEGORIES[primary_category]
    sub_categories = cat_config.get("categories", {})
    priority = cat_config.get("priority", [])

    if not sub_categories:
        return "", "无二级分类", 0.0

    # Step 1: 检查强制匹配规则
    force_secondary, force_bonus, force_description = check_secondary_force_match(text, primary_category, name)
    if force_secondary and force_bonus >= 5:
        # 强制匹配，高置信度直接返回
        return force_secondary, f"强制匹配: {force_description}", 0.95

    # Step 2: 计算各二级分类得分（同时检查负向规则）
    scores = {}
    excluded_categories = set()

    for sub_cat, keywords in sub_categories.items():
        score, excluded = calculate_secondary_score(text, keywords, primary_category, sub_cat)
        if excluded:
            excluded_categories.add(sub_cat)
            scores[sub_cat] = 0.0
        else:
            scores[sub_cat] = score

    # Step 3: 应用强制匹配加成
    if force_secondary and force_secondary not in excluded_categories:
        scores[force_secondary] += force_bonus

    # Step 4: 找最高分（排除被负向规则排除的分类）
    valid_scores = {k: v for k, v in scores.items() if k not in excluded_categories}

    if not valid_scores or max(valid_scores.values()) < 1:
        # 没有有效分类或得分太低，使用优先级第一个作为默认
        default_sub = priority[0] if priority else list(sub_categories.keys())[0]
        return default_sub, "默认分类", 0.3

    max_score = max(valid_scores.values())

    # 找最高分分类
    best_subs = [sub for sub, score in valid_scores.items() if score == max_score]

    if len(best_subs) > 1:
        # 多个同分，按优先级选择
        for sub in priority:
            if sub in best_subs:
                best_sub = sub
                break
        else:
            best_sub = best_subs[0]
    else:
        best_sub = best_subs[0]

    # Step 5: 应用特殊规则
    special_result = apply_special_rules(primary_category, text, valid_scores)
    if special_result and special_result not in excluded_categories:
        best_sub = special_result

    # Step 6: 计算置信度
    confidence = calculate_secondary_confidence(valid_scores, best_sub)

    # Step 7: 生成理由
    keywords = sub_categories.get(best_sub, {})
    matched = []
    for kw in keywords.get("strong", []):
        if kw.lower() in text:
            matched.append(kw)
            if len(matched) >= 2:
                break

    if matched:
        reason = f"匹配: {', '.join(matched)}"
    else:
        medium_matched = []
        for kw in keywords.get("medium", []):
            if kw.lower() in text:
                medium_matched.append(kw)
                if len(medium_matched) >= 2:
                    break
        if medium_matched:
            reason = f"特征: {', '.join(medium_matched)}"
        else:
            reason = "默认分类"

    return best_sub, reason, round(confidence, 2)


def subclassify(input_path: str, output_path: str = None):
    """处理一级分类结果，添加二级分类"""
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    classification = data.get('classification', {})
    sub_statistics = {}

    for primary_cat, cat_data in classification.items():
        if not isinstance(cat_data, dict):
            continue

        skills = cat_data.get('skills', [])
        sub_statistics[primary_cat] = {}

        for skill in skills:
            name = skill.get('name', '')
            description = skill.get('description', '')

            sub_cat, sub_reason, confidence = subclassify_skill(name, description, primary_cat)

            skill['secondary_category'] = sub_cat
            skill['secondary_reason'] = sub_reason
            skill['secondary_confidence'] = confidence

            if sub_cat:
                sub_statistics[primary_cat][sub_cat] = sub_statistics[primary_cat].get(sub_cat, 0) + 1

    data['secondary_statistics'] = sub_statistics
    data['scan_time'] = datetime.now().isoformat()

    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"二级分类结果已保存到: {output_path}")
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))

    return data


def main():
    if len(sys.argv) < 2:
        print("用法: python subclassify.py <一级分类json> [--output 输出路径]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = None

    if len(sys.argv) > 3 and sys.argv[2] == '--output':
        output_path = sys.argv[3]

    subclassify(input_path, output_path)


if __name__ == '__main__':
    main()
