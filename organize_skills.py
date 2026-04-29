#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills 归类整理脚本
读取分类结果，将 skills 文件夹按照分类归类整理
"""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


def load_classification_result(json_path: str) -> dict:
    """加载分类结果 JSON 文件"""
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def organize_skills(
    classification_data: dict,
    source_base: str,
    output_base: str,
    mode: str = "copy",
    dry_run: bool = False
) -> Dict[str, int]:
    """
    根据 classification 结果整理 skills 文件夹

    Args:
        classification_data: 分类结果数据
        source_base: skills 源目录
        output_base: 输出目录
        mode: "copy" 复制或 "move" 移动
        dry_run: 仅预览，不执行实际操作

    Returns:
        统计信息字典
    """
    source_path = Path(source_base)
    output_path = Path(output_base)

    stats = {
        "total": 0,
        "success": 0,
        "failed": 0,
        "skipped": 0
    }

    # 获取分类数据
    classification = classification_data.get('classification', {})

    # 按一级分类和二级分类整理
    for primary_cat, cat_data in classification.items():
        if not isinstance(cat_data, dict):
            continue

        skills = cat_data.get('skills', [])

        for skill in skills:
            stats["total"] += 1
            skill_name = skill.get('name', 'unknown')
            skill_file = skill.get('file', '')
            secondary_cat = skill.get('secondary_category', '')

            if not skill_file:
                print(f"[跳过] {skill_name}: 未找到源文件路径")
                stats["skipped"] += 1
                continue

            # 构建目标路径: 输出目录/一级分类/二级分类/skill名称
            if secondary_cat:
                target_dir = output_path / primary_cat / secondary_cat
            else:
                target_dir = output_path / primary_cat

            target_path = target_dir / skill_name

            # 获取源路径（skill 文件夹）
            source_skill_path = Path(skill_file).parent

            if not source_skill_path.exists():
                print(f"[跳过] {skill_name}: 源目录不存在 {source_skill_path}")
                stats["skipped"] += 1
                continue

            if dry_run:
                print(f"[预览] {skill_name} -> {target_path}")
                stats["success"] += 1
                continue

            # 创建目标目录
            try:
                target_dir.mkdir(parents=True, exist_ok=True)

                # 检查目标是否已存在
                if target_path.exists():
                    print(f"[跳过] {skill_name}: 目标已存在")
                    stats["skipped"] += 1
                    continue

                # 执行复制或移动
                if mode == "move":
                    shutil.move(str(source_skill_path), str(target_path))
                    print(f"[移动] {skill_name} -> {target_path}")
                else:
                    shutil.copytree(str(source_skill_path), str(target_path))
                    print(f"[复制] {skill_name} -> {target_path}")

                stats["success"] += 1

            except Exception as e:
                print(f"[失败] {skill_name}: {e}")
                stats["failed"] += 1

    return stats


def generate_summary_report(
    classification_data: dict,
    output_base: str,
    stats: Dict[str, int]
) -> str:
    """生成整理结果摘要报告"""
    output_path = Path(output_base)
    report_path = output_path / "organize_summary.md"

    lines = [
        "# Skills 分类整理报告",
        f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## 整理统计",
        f"- 总数: {stats['total']}",
        f"- 成功: {stats['success']}",
        f"- 跳过: {stats['skipped']}",
        f"- 失败: {stats['failed']}",
        f"\n## 目录结构",
        "```",
    ]

    # 生成目录树
    classification = classification_data.get('classification', {})
    for primary_cat, cat_data in classification.items():
        if not isinstance(cat_data, dict):
            continue
        count = cat_data.get('count', 0)
        if count > 0:
            lines.append(f"{primary_cat}/ ({count})")

            # 统计二级分类
            secondary_stats = {}
            for skill in cat_data.get('skills', []):
                sec = skill.get('secondary_category', '')
                if sec:
                    secondary_stats[sec] = secondary_stats.get(sec, 0) + 1

            for sec, sec_count in secondary_stats.items():
                lines.append(f"├── {sec}/ ({sec_count})")

    lines.append("```")

    # 写入文件
    report_content = "\n".join(lines)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)

    return str(report_path)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='根据分类结果整理 skills 文件夹',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # 预览整理效果（不执行实际操作）
  python organize_skills.py classification.json -o ./organized_skills --dry-run

  # 复制模式（默认，保留原文件）
  python organize_skills.py classification.json -o ./organized_skills

  # 移动模式（删除原文件）
  python organize_skills.py classification.json -o ./organized_skills --mode move
"""
    )

    parser.add_argument('classification_json', help='分类结果 JSON 文件路径')
    parser.add_argument('-o', '--output', required=True, help='输出目录')
    parser.add_argument('--mode', choices=['copy', 'move'], default='copy',
                        help='整理模式: copy(复制) 或 move(移动)，默认 copy')
    parser.add_argument('--dry-run', action='store_true',
                        help='预览模式，不执行实际操作')

    args = parser.parse_args()

    # 加载分类结果
    print(f"加载分类结果: {args.classification_json}")
    classification_data = load_classification_result(args.classification_json)

    # 获取源目录（从分类结果中读取）
    source_base = classification_data.get('source_path', '')
    if not source_base:
        print("错误: 分类结果中未找到源目录路径")
        sys.exit(1)

    print(f"源目录: {source_base}")
    print(f"输出目录: {args.output}")
    print(f"模式: {args.mode}")
    print(f"预览模式: {'是' if args.dry_run else '否'}")
    print("-" * 50)

    # 执行整理
    stats = organize_skills(
        classification_data,
        source_base,
        args.output,
        mode=args.mode,
        dry_run=args.dry_run
    )

    # 打印统计
    print("-" * 50)
    print(f"整理完成:")
    print(f"  总数: {stats['total']}")
    print(f"  成功: {stats['success']}")
    print(f"  跳过: {stats['skipped']}")
    print(f"  失败: {stats['failed']}")

    # 生成摘要报告（非预览模式）
    if not args.dry_run:
        report_path = generate_summary_report(classification_data, args.output, stats)
        print(f"\n摘要报告: {report_path}")


if __name__ == '__main__':
    main()
