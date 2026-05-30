#!/usr/bin/env python3
"""构建传感器·单片机·物联网复习系统"""
import json, os, re

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, 'source.html'), encoding='utf-8') as f:
    html = f.read()

with open(os.path.join(BASE, 'subjects.json'), encoding='utf-8') as f:
    subjects = json.load(f)

sjson = json.dumps(subjects, ensure_ascii=False)
html = html.replace('__SUBJECTS_DATA__', sjson)

out = os.path.join(BASE, '..', '传感器单片机物联网复习系统.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

total = sum(len(s['questions']) for s in subjects)
print(f'✓ {os.path.basename(out)} ({len(subjects)}科目, {total}题)')
