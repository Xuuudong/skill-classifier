#!/usr/bin/env python3
"""
分类报告生成脚本 - 支持响应式设计和悬停动画效果
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def get_current_beijing_time():
    """自动获取当前北京时间并格式化"""
    now = datetime.now()
    return now.strftime('%Y-%m-%d %H:%M:%S'), now.strftime('%Y-%m-%dT%H:%M:%S')


def format_scan_time(scan_time):
    """将时间格式化为友好的显示格式"""
    if not scan_time:
        return "未知时间"

    try:
        if 'T' in scan_time:
            parts = scan_time.split('T')
            date_part = parts[0]
            time_part = parts[1].split('+')[0].split('-')[0].split('.')[0]
            time_part = time_part[:5] if len(time_part) >= 5 else time_part
            return f"{date_part} {time_part} (北京时间)"
        return scan_time
    except:
        return scan_time


def generate_html_report(data, output_path):
    """生成 HTML 分类报告（响应式设计 + 悬停动画）"""

    stats = data.get('statistics', {})
    total = data.get('total_skills', 0)

    # 自动获取当前北京时间
    display_time, iso_time = get_current_beijing_time()
    scan_time = f"{display_time[:16]} (北京时间)"

    # 更新 JSON 中的时间
    data['scan_time'] = iso_time

    # 如果输出路径是默认路径，添加时间戳避免覆盖
    if output_path.endswith('skills-classification-report.html'):
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = output_path.replace('.html', f'_{timestamp}.html')

    category_colors = {
        '开发与自动化': ('#3B82F6', '#60A5FA'),
        '文档与内容创作': ('#EC4899', '#F472B6'),
        '搜索与研究': ('#10B981', '#34D399'),
        '金融数据': ('#06B6D4', '#22D3EE'),
        '通讯与协作': ('#8B5CF6', '#A78BFA'),
        '其他': ('#6B7280', '#9CA3AF')
    }

    category_icons = {
        '开发与自动化': '🛠️',
        '文档与内容创作': '📄',
        '搜索与研究': '🔍',
        '金融数据': '💰',
        '通讯与协作': '💬',
        '其他': '📦'
    }

    # 二级分类颜色
    sub_category_colors = {
        'AI Agent框架': '#7C3AED',
        '浏览器自动化': '#1E40AF',
        'MCP工具': '#3B82F6',
        '文档生成与编辑': '#BE185D',
        '媒体与设计': '#059669',
        'Web搜索': '#047857',
        '深度研究': '#B45309',
        '基金投资': '#0E7490',
        '量化数据': '#1D4ED8',
        '通讯平台': '#6D28D9',
        '笔记协作': '#DB2777'
    }

    # 计算饼图
    pie_slices = []
    offset = 0
    circumference = 251.3

    for cat, count in stats.items():
        if count > 0:
            slice_len = (count / total) * circumference if total > 0 else 0
            colors = category_colors.get(cat, ('#999', '#999'))
            pie_slices.append({
                'dasharray': f"{slice_len:.1f} {circumference}",
                'dashoffset': offset,
                'color1': colors[0]
            })
            offset -= slice_len

    # 生成图例 HTML（含二级分类）
    secondary_stats = data.get('secondary_statistics', {})

    # 定义所有二级分类
    all_secondary = {
        "开发与自动化": ["AI Agent框架", "浏览器自动化", "MCP工具"],
        "文档与内容创作": ["文档生成与编辑", "媒体与设计"],
        "搜索与研究": ["Web搜索", "深度研究"],
        "金融数据": ["基金投资", "量化数据"],
        "通讯与协作": ["通讯平台", "笔记协作"],
        "其他": []
    }

    legend_html = ""
    for cat in ['开发与自动化', '文档与内容创作', '搜索与研究', '金融数据', '通讯与协作', '其他']:
        colors = category_colors.get(cat, ('#999', '#999'))
        icon = category_icons.get(cat, '📁')
        cat_id = cat.replace('与', '-').replace(' ', '-')
        cat_count = stats.get(cat, 0)

        # 获取二级分类统计
        sub_stats = secondary_stats.get(cat, {})
        sub_cats = all_secondary.get(cat, [])

        # 生成二级分类项
        sub_items = ""
        for sub_cat in sub_cats:
            sub_count = sub_stats.get(sub_cat, 0)
            sub_color = sub_category_colors.get(sub_cat, colors[0])
            sub_items += f'<div class="legend-sub-item"><span class="legend-sub-dot" style="background: {sub_color};"></span><span class="legend-sub-text">{sub_cat}</span><span class="legend-sub-count">{sub_count}</span></div>'

        legend_html += f'''
        <div class="legend-item" onclick="toggleCategory('{cat_id}')">
            <div class="legend-color" style="background: linear-gradient(135deg, {colors[0]} 0%, {colors[1]} 100%);"></div>
            <div class="legend-content">
                <div class="legend-main"><span class="legend-text">{icon} {cat}</span><span class="legend-count">{cat_count}</span></div>
                <div class="legend-sub-list">{sub_items}</div>
            </div>
        </div>'''

    # 生成分类部分 HTML
    category_html = ""
    for cat in ['开发与自动化', '文档与内容创作', '搜索与研究', '金融数据', '通讯与协作', '其他']:
        skills = data.get('classification', {}).get(cat, {}).get('skills', [])
        count = len(skills)
        colors = category_colors.get(cat, ('#999', '#999'))
        icon = category_icons.get(cat, '📁')
        cat_id = cat.replace('与', '-').replace(' ', '-')

        # 构建技能列表
        skills_html = ""
        if skills:
            for skill in skills:
                desc = skill.get('description', '')
                if len(desc) > 150:
                    desc = desc[:150] + '...'
                sub_cat = skill.get('secondary_category', '')
                sub_color = sub_category_colors.get(sub_cat, colors[0])
                sub_badge = f'<span class="sub-cat-badge" style="background: {sub_color};">{sub_cat}</span>' if sub_cat else ''
                skills_html += f'''
                <div class="skill-item" style="border-left: 4px solid {sub_color};">
                    <div class="skill-name">{skill.get('name', 'Unknown')} {sub_badge}</div>
                    <div class="skill-desc">{desc}</div>
                    <div class="skill-reason">分类依据: {skill.get('classification_reason', '')}</div>
                </div>'''
        else:
            skills_html = '<div class="empty-category">暂无此类别的 skills</div>'

        category_html += f'''
        <div class="category-section">
            <div class="category-header" style="background: linear-gradient(135deg, {colors[0]} 0%, {colors[1]} 100%);" onclick="toggleCategory('{cat_id}')">
                <div class="category-icon">{icon}</div>
                <span class="category-title">{cat}</span>
                <span class="category-count">{count} 个</span>
                <span class="toggle-icon" id="icon-{cat_id}">▼</span>
            </div>
            <div class="skill-list" id="list-{cat_id}">
                {skills_html}
            </div>
        </div>'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Skills 分类报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }}

        /* 桌面端样式 */
        @media (min-width: 769px) {{
            body {{
                padding: 40px 30px;
            }}
            .container {{
                max-width: 1200px;
                margin: 0 auto;
            }}
            .header h1 {{
                font-size: 2.5rem;
            }}
            .header .subtitle {{
                font-size: 1.1rem;
            }}
            .chart-container {{
                flex-direction: row;
                gap: 40px;
            }}
            .pie-section {{
                flex-shrink: 0;
            }}
            .pie-chart {{
                width: 180px;
                height: 180px;
            }}
            .legend {{
                flex: 1;
                max-width: 480px;
            }}
            .legend-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            .category-header {{
                padding: 20px 25px;
            }}
            .skill-list {{
                padding: 20px 25px;
            }}
            .controls {{
                gap: 16px;
            }}
            .btn {{
                padding: 14px 24px;
                font-size: 0.95rem;
            }}
        }}

        /* 移动端样式 */
        @media (max-width: 768px) {{
            body {{
                padding: 15px 12px;
            }}
            .header {{
                margin-bottom: 20px;
            }}
            .header h1 {{
                font-size: 1.75rem;
                margin-bottom: 8px;
            }}
            .header .subtitle {{
                font-size: 0.85rem;
                line-height: 1.5;
            }}
            .stats-card {{
                padding: 20px 15px;
                margin-bottom: 20px;
                border-radius: 12px;
            }}
            .stats-header {{
                margin-bottom: 15px;
            }}
            .stats-header h2 {{
                font-size: 1.2rem;
            }}
            .chart-container {{
                gap: 20px;
            }}
            .pie-chart {{
                width: 150px;
                height: 150px;
            }}
            .pie-center .number {{
                font-size: 1.5rem;
            }}
            .legend {{
                max-width: 100%;
            }}
            .legend-grid {{
                grid-template-columns: 1fr;
                gap: 8px;
            }}
            .legend-item {{
                padding: 10px 12px;
            }}
            .validation {{
                padding: 10px;
                font-size: 0.8rem;
            }}
            .controls {{
                flex-direction: row;
                gap: 12px;
                margin: 15px 0;
            }}
            .btn {{
                padding: 12px 18px;
                font-size: 0.9rem;
                flex: 1;
                justify-content: center;
            }}
            .category-section {{
                margin-bottom: 12px;
                border-radius: 12px;
            }}
            .category-header {{
                padding: 15px;
                gap: 10px;
            }}
            .category-icon {{
                width: 40px;
                height: 40px;
                font-size: 1.2rem;
            }}
            .category-title {{
                font-size: 1.1rem;
            }}
            .category-count {{
                padding: 4px 12px;
                font-size: 0.85rem;
            }}
            .skill-list {{
                padding: 15px;
            }}
            .skill-item {{
                padding: 12px 15px;
                margin-bottom: 10px;
            }}
            .skill-name {{
                font-size: 1rem;
            }}
            .skill-desc {{
                font-size: 0.85rem;
            }}
            .skill-reason {{
                padding: 6px 10px;
                font-size: 0.75rem;
            }}
            .footer {{
                margin-top: 20px;
                font-size: 0.8rem;
            }}
        }}

        .header {{
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }}

        .header h1 {{
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }}

        .header .subtitle {{
            opacity: 0.9;
        }}

        .controls {{
            display: flex;
            justify-content: center;
            gap: 16px;
            margin: 25px 0;
        }}

        .btn {{
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 600;
            transition: all 0.25s ease;
            display: flex;
            align-items: center;
            gap: 8px;
            position: relative;
            overflow: hidden;
        }}

        .btn::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(255,255,255,0.1);
            opacity: 0;
            transition: opacity 0.25s;
        }}

        .btn:hover::before {{
            opacity: 1;
        }}

        .btn-expand {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }}

        .btn-collapse {{
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            box-shadow: 0 4px 15px rgba(240, 147, 251, 0.4);
        }}

        .btn:hover {{
            transform: translateY(-3px);
        }}

        .btn-expand:hover {{
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
        }}

        .btn-collapse:hover {{
            box-shadow: 0 8px 25px rgba(240, 147, 251, 0.5);
        }}

        .btn:active {{
            transform: translateY(-1px);
        }}

        .btn:active {{
            transform: translateY(0);
        }}

        .stats-card {{
            background: white;
            border-radius: 16px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            padding: 25px;
        }}

        .stats-header {{
            text-align: center;
            margin-bottom: 25px;
        }}

        .stats-header h2 {{
            color: #333;
            font-size: 1.4rem;
            margin-bottom: 8px;
        }}

        .total-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 6px 18px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.9rem;
        }}

        .validation {{
            background: { '#dcfce7' if data.get('validation', {}).get('passed', True) else '#fef3c7' };
            padding: 12px 16px;
            border-radius: 8px;
            margin-bottom: 20px;
            text-align: center;
            color: { '#166534' if data.get('validation', {}).get('passed', True) else '#92400e' };
            font-size: 0.9rem;
        }}

        .chart-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 30px;
        }}

        .pie-section {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .pie-chart {{
            position: relative;
            margin-bottom: 8px;
        }}

        .pie-chart svg {{
            transform: rotate(-90deg);
            filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
        }}

        .pie-center {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
        }}

        .pie-center .number {{
            font-size: 2rem;
            font-weight: 700;
            color: #333;
        }}

        .pie-center .label {{
            font-size: 0.85rem;
            color: #666;
            margin-top: 2px;
        }}

        .legend {{
            width: 100%;
            max-width: 500px;
        }}

        .legend-grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            padding: 12px 14px;
            background: #f8f9fa;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.25s ease;
            border: 1px solid transparent;
        }}

        .legend-item:hover {{
            background: #ffffff;
            border-color: #e0e0e0;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}

        .legend-color {{
            width: 14px;
            height: 14px;
            border-radius: 4px;
            margin-right: 10px;
            flex-shrink: 0;
        }}

        .legend-text {{
            flex: 1;
            font-weight: 500;
            color: #333;
            font-size: 0.9rem;
        }}

        .legend-count {{
            background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
            padding: 3px 10px;
            border-radius: 10px;
            font-weight: 600;
            color: #555;
            font-size: 0.85rem;
            min-width: 36px;
            text-align: center;
        }}

        .category-section {{
            background: white;
            border-radius: 16px;
            margin-bottom: 15px;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}

        .category-header {{
            display: flex;
            align-items: center;
            gap: 15px;
            cursor: pointer;
            user-select: none;
            transition: all 0.2s;
        }}

        .category-header:hover {{
            opacity: 0.95;
            filter: brightness(1.05);
        }}

        .category-header:active {{
            filter: brightness(0.98);
        }}

        .category-icon {{
            background: rgba(255,255,255,0.2);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .category-title {{
            color: white;
            font-weight: 600;
        }}

        .category-count {{
            margin-left: auto;
            background: rgba(255,255,255,0.2);
            color: white;
            border-radius: 20px;
            font-weight: 600;
        }}

        .toggle-icon {{
            color: white;
            font-size: 0.9rem;
            transition: transform 0.3s;
        }}

        .toggle-icon.collapsed {{
            transform: rotate(-90deg);
        }}

        .skill-list {{
            max-height: 500px;
            overflow-y: auto;
            transition: max-height 0.3s ease-out, padding 0.3s ease-out;
        }}

        .skill-list.collapsed {{
            max-height: 0;
            padding: 0 25px !important;
        }}

        .skill-list::-webkit-scrollbar {{
            width: 6px;
        }}

        .skill-list::-webkit-scrollbar-track {{
            background: #f1f1f1;
            border-radius: 3px;
        }}

        .skill-list::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 3px;
        }}

        .skill-list::-webkit-scrollbar-thumb:hover {{
            background: #a1a1a1;
        }}

        /* Skill 悬停上浮动画 */
        .skill-item {{
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px 20px;
            margin-bottom: 12px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}

        .skill-item:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            background: #ffffff;
        }}

        .skill-item:active {{
            transform: translateY(-2px);
        }}

        .skill-name {{
            font-size: 1.1rem;
            font-weight: 600;
            color: #333;
            margin-bottom: 6px;
        }}

        .skill-desc {{
            color: #666;
            font-size: 0.9rem;
            margin-bottom: 10px;
            line-height: 1.5;
        }}

        .skill-reason {{
            background: #e3f2fd;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
            color: #1565c0;
        }}

        .sub-cat-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.7rem;
            color: white;
            margin-left: 8px;
            font-weight: 500;
        }}

        .legend-item {{
            display: flex;
            align-items: flex-start;
            padding: 12px 14px;
            background: #f8f9fa;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.25s ease;
            border: 1px solid transparent;
        }}

        .legend-content {{
            flex: 1;
            margin-left: 10px;
        }}

        .legend-main {{
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .legend-sub-list {{
            margin-top: 8px;
            padding-top: 8px;
            border-top: 1px solid #e5e7eb;
        }}

        .legend-sub-item {{
            display: flex;
            align-items: center;
            padding: 4px 0;
            font-size: 0.85rem;
        }}

        .legend-sub-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
            flex-shrink: 0;
        }}

        .legend-sub-text {{
            flex: 1;
            color: #4b5563;
        }}

        .legend-sub-count {{
            font-size: 0.8rem;
            color: #6b7280;
            background: #e5e7eb;
            padding: 1px 8px;
            border-radius: 10px;
            min-width: 24px;
            text-align: center;
        }}

        .empty-category {{
            padding: 30px;
            text-align: center;
            color: #999;
            font-style: italic;
        }}

        .validation {{
            background: { '#dcfce7' if data.get('validation', {}).get('passed', True) else '#fef3c7' };
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            color: { '#166534' if data.get('validation', {}).get('passed', True) else '#92400e' };
        }}

        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.8);
            margin-top: 30px;
            font-size: 0.9rem;
        }}

        /* 移动端触摸优化 */
        @media (hover: none) and (pointer: coarse) {{
            .skill-item {{
                transition: background 0.2s;
            }}
            .skill-item:active {{
                transform: none;
                background: #e9ecef;
            }}
            .legend-item:hover {{
                transform: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Skills 分类报告</h1>
            <p class="subtitle">扫描路径: {data.get('source_path', '')} | 扫描时间: {scan_time} | 共 {total} 个 Skills</p>
        </div>

        <div class="stats-card">
            <div class="stats-header">
                <h2>📊 分类统计</h2>
                <span class="total-badge">共 {total} 个 Skills</span>
            </div>
            <div class="validation">{data.get('validation', {}).get('message', '')}</div>
            <div class="chart-container">
                <div class="pie-section">
                    <div class="pie-chart">
                        <svg viewBox="0 0 100 100" width="100%" height="100%">
                            {''.join([f'<circle cx="50" cy="50" r="40" fill="none" stroke="{s["color1"]}" stroke-width="20" stroke-dasharray="{s["dasharray"]}" stroke-dashoffset="{s["dashoffset"]}"/>' for s in pie_slices])}
                        </svg>
                        <div class="pie-center">
                            <div class="number">{total}</div>
                            <div class="label">总计</div>
                        </div>
                    </div>
                </div>
                <div class="legend">
                    <div class="legend-grid">
                        {legend_html}
                    </div>
                </div>
            </div>
        </div>

        <div class="controls">
            <button class="btn btn-expand" onclick="expandAll()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="17 8 12 3 7 8"/>
                    <line x1="12" y1="3" x2="12" y2="15"/>
                </svg>
                全部展开
            </button>
            <button class="btn btn-collapse" onclick="collapseAll()">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                    <polyline points="7 10 12 15 17 10"/>
                    <line x1="12" y1="15" x2="12" y2="3"/>
                </svg>
                全部折叠
            </button>
        </div>

        {category_html}

        <div class="footer">
            <p>Skills Classification Report | Generated by skill-classifier</p>
        </div>
    </div>

    <script>
        function toggleCategory(catId) {{
            const list = document.getElementById('list-' + catId);
            const icon = document.getElementById('icon-' + catId);
            if (list && icon) {{
                list.classList.toggle('collapsed');
                icon.classList.toggle('collapsed');
            }}
        }}

        function expandAll() {{
            document.querySelectorAll('.skill-list').forEach(el => el.classList.remove('collapsed'));
            document.querySelectorAll('.toggle-icon').forEach(el => el.classList.remove('collapsed'));
        }}

        function collapseAll() {{
            document.querySelectorAll('.skill-list').forEach(el => el.classList.add('collapsed'));
            document.querySelectorAll('.toggle-icon').forEach(el => el.classList.add('collapsed'));
        }}
    </script>
</body>
</html>'''

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML 报告已生成: {output_path}")


def main():
    if len(sys.argv) < 3:
        print("用法: python generate_report.py <json数据文件> <输出html路径>")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2]

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    generate_html_report(data, output_path)

    # 同时更新 JSON 文件中的时间
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"JSON 文件已更新: {json_path}")
    print(f"HTML 报告: {output_path}")


if __name__ == '__main__':
    main()
