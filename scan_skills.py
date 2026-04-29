#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills 扫描脚本 - 自动扫描指定目录下的所有 skills
支持 SKILL.md / skill.md 大小写兼容
支持大规模扫描（分批处理，内存优化）
"""

import os
import json
import sys
import io
from pathlib import Path
from datetime import datetime, timezone
import time

# 修复 Windows 下编码问题
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def get_local_time():
    """获取本地时间，格式：2026-04-21T13:41:00+08:00"""
    now = datetime.now()
    tz_offset = time.timezone // -3600
    tz_str = f"+{tz_offset:02d}:00" if tz_offset >= 0 else f"{tz_offset:03d}:00"
    return now.strftime(f"%Y-%m-%dT%H:%M:%S{tz_str}")


def find_skill_files(directory):
    """
    扫描目录下的所有 skill 文件
    返回: [(目录名, 文件路径, 文件类型), ...]
    """
    results = []
    dir_path = Path(directory)

    if not dir_path.exists():
        print(f"错误: 目录不存在 - {directory}")
        return results, [], []

    subdirs = [d for d in dir_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
    # 支持多种文件名变体：SKILL.md, skill.md, skills.md, SKILLS.md
    skill_filenames = ['SKILL.md', 'skill.md', 'Skill.md', 'skills.md', 'SKILLS.md', 'Skills.md']
    fallback_filename = 'README.md'
    missing_dirs = []

    for subdir in sorted(subdirs):
        found = False

        for filename in skill_filenames:
            skill_file = subdir / filename
            if skill_file.exists():
                results.append((subdir.name, str(skill_file), 'SKILL.md'))
                found = True
                break

        if not found:
            readme_file = subdir / fallback_filename
            if readme_file.exists():
                results.append((subdir.name, str(readme_file), 'README.md'))
                found = True

        if not found:
            missing_dirs.append(subdir.name)

    return results, missing_dirs, [d.name for d in subdirs]


def scan_in_batches(skill_files, batch_size=20):
    """
    分批扫描 skills，避免内存溢出
    返回: generator，每批返回 (batch_index, batch_results)
    """
    total = len(skill_files)
    for i in range(0, total, batch_size):
        batch = skill_files[i:i + batch_size]
        batch_results = []
        for name, path, file_type in batch:
            content = read_skill_content(path)
            batch_results.append({
                'name': name,
                'path': path,
                'file_type': file_type,
                'content': content
            })
        yield i // batch_size, batch_results, i + len(batch), total


def read_skill_content(file_path, max_lines=200):
    """
    读取 skill 文件内容，限制行数避免内存问题
    大规模扫描时只读取前 max_lines 行
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = []
            for i, line in enumerate(f):
                if i >= max_lines:
                    break
                lines.append(line)
            return ''.join(lines)
    except Exception as e:
        print(f"警告: 无法读取文件 {file_path}: {e}")
        return None


def extract_description(content):
    """从 SKILL.md 内容中提取 description 字段"""
    if not content:
        return ""

    # 尝试从 YAML frontmatter 提取
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            for line in frontmatter.split('\n'):
                if line.startswith('description:'):
                    return line.replace('description:', '', 1).strip().strip('"\'')

    # 尝试从第一个段落提取
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('---'):
            return line[:200]

    return ""


def validate_scan(total_dirs, found_skills, missing_dirs):
    """验证扫描完整性"""
    if not missing_dirs:
        return True, f"[OK] 验证通过: 所有 {total_dirs} 个目录都包含 skill 文件"
    else:
        return False, f"[警告] 发现 {total_dirs} 个目录，但只找到 {found_skills} 个 skill 文件\n遗漏的目录: {', '.join(missing_dirs)}"


def main():
    if len(sys.argv) < 2:
        print("用法: python scan_skills.py <目录路径> [--output json文件路径]")
        sys.exit(1)

    directory = sys.argv[1]
    output_path = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--output' else None

    print(f"正在扫描: {directory}")
    print("-" * 50)

    # 扫描
    skill_files, missing_dirs, all_dirs = find_skill_files(directory)

    # 验证
    passed, message = validate_scan(len(all_dirs), len(skill_files), missing_dirs)
    print(message)

    # 输出结果
    print(f"\n找到 {len(skill_files)} 个 skills:")
    for name, path, file_type in skill_files:
        print(f"  - {name} ({file_type})")

    # 导出 JSON
    if output_path:
        result = {
            "scan_time": get_local_time(),
            "source_path": directory,
            "total_directories": len(all_dirs),
            "total_skills": len(skill_files),
            "validation": {
                "passed": passed,
                "message": message,
                "missing_skills": missing_dirs
            },
            "skills": [
                {"name": name, "file": path, "file_type": file_type}
                for name, path, file_type in skill_files
            ]
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {output_path}")

    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
