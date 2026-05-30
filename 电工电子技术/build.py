#!/usr/bin/env python3
"""构建电工电子技术复习系统"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE, 'source.html'), encoding='utf-8') as f:
    html = f.read()

with open(os.path.join(BASE, 'questions.json'), encoding='utf-8') as f:
    qb = json.load(f)

qjson = json.dumps(qb, ensure_ascii=False)
html = html.replace('__QB_DATA__', qjson)

out = os.path.join(BASE, '电工电子技术刷题平台.html')
with open(out, 'w', encoding='utf-8') as f:
    f.write(html)

print(f'✓ {os.path.basename(out)} ({len(qb)}题)')
