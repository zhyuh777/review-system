import os, json, re

BASE = '/Users/zzzzed/opencodes/electest/universal_review/scan/output'
TARGET = '/Users/zzzzed/opencodes/electest/universal_review/scan'

def classify(text):
    t = text.strip()
    if re.match(r'^项目', t): return 'title'
    if '思考练习' in t or '思考与练习' in t:
        return 'title' if len(t) < 30 else 'fill'
    if re.match(r'^[一二三四五六七八九十\d]+[、.．]\s*(单选|填空|判断|简答|问答|计算|操作)', t):
        return 'heading'
    lines = t.split('\n')
    has_abcd = any(re.match(r'^[A-D][.、．\s]', l.strip()) for l in lines if l.strip())
    if has_abcd: return 'choice'
    if t.startswith('（') or t.startswith('(') or t.startswith('〈') or t.startswith('《'):
        if len(t) < 70:
            return 'tf' if ('正确' in t or '错误' in t) else 'fill'
        return 'fill'
    return 'fill'

def build_data():
    subjects = []
    for pdf, dirname in [
        ('夸克扫描王_思考练习.pdf', '思考练习'),
        ('夸克扫描王_思考与练习题1.pdf', '思考与练习题1'),
    ]:
        qdir = os.path.join(BASE, dirname, 'questions')
        qs = sorted([d for d in os.listdir(qdir) if d.startswith('q_')],
                    key=lambda x: int(x.split('_')[1]))
        questions = []
        for qd in qs:
            qpath = os.path.join(qdir, qd)
            with open(os.path.join(qpath, 'text.txt'), 'r', encoding='utf-8') as f:
                text = f.read().strip()
            with open(os.path.join(qpath, 'info.txt'), 'r', encoding='utf-8') as f:
                info = f.read()
            page = 1
            m = re.search(r'Page:?\s*(\d+)', info)
            if m: page = int(m.group(1))
            has_diagram = any(f.startswith('diagram') for f in os.listdir(qpath))
            tp = classify(text)
            qid = int(qd.split('_')[1])
            questions.append({
                'id': qid,
                'text': text,
                'type': tp,
                'page': page,
                'diagram': has_diagram,
            })
        subjects.append({
            'name': '传感器技术' if '思考练习' in dirname else '单片机技术',
            'icon': '📡' if '思考练习' in dirname else '💻',
            'dir': dirname,
            'total': len(questions),
            'pages': len(set(q['page'] for q in questions)),
            'questions': questions,
        })
        print(f'{dirname}: {len(questions)} questions, '
              f'types={dict((t,sum(1 for q in questions if q["type"]==t)) for t in set(q["type"] for q in questions))}')
    # Write JS
    with open(os.path.join(TARGET, 'questions.js'), 'w', encoding='utf-8') as f:
        f.write('// 自动生成 — 由 extraction output 构建\n')
        f.write('var SUBJECTS = ' + json.dumps(subjects, ensure_ascii=False, indent=2) + ';\n')
    print(f'\nWrote {sum(s["total"] for s in subjects)} questions to questions.js')

if __name__ == '__main__':
    build_data()
