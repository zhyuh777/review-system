import fitz
import pytesseract
from PIL import Image, ImageFilter
import re
import os
import shutil
from collections import defaultdict

BASE = '/Users/zzzzed/opencodes/electest/universal_review/scan'
OUTPUT = os.path.join(BASE, 'output')

PDFS = [
    '夸克扫描王_思考练习.pdf',
    '夸克扫描王_思考与练习题1.pdf',
]

DPI = 300


def pdf_name_clean(fname):
    return fname.replace('.pdf', '').replace('夸克扫描王_', '')


def render_page(pdf_path, page_num):
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    mat = fitz.Matrix(DPI / 72, DPI / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def is_project_heading(line):
    line = line.strip()
    if re.match(r'^项目[一二三四五六七八九十\d]', line):
        return True
    if re.match(r'^项目\s*\d+', line):
        return True
    return False


def detect_questions_from_ocr(ocr_data):
    lines = []
    for i, text in enumerate(ocr_data['text']):
        txt = text.strip()
        if not txt:
            continue
        x = ocr_data['left'][i]
        y = ocr_data['top'][i]
        w = ocr_data['width'][i]
        h = ocr_data['height'][i]
        conf = int(ocr_data['conf'][i]) if ocr_data['conf'][i] != '-1' else 0
        lines.append({
            'text': txt,
            'x': x, 'y': y, 'w': w, 'h': h,
            'conf': conf,
            'cx': x + w // 2,
            'cy': y + h // 2,
        })

    lines.sort(key=lambda l: (l['y'], l['x']))

    grouped = []
    current_line = None
    for l in lines:
        if current_line is None:
            current_line = dict(l)
            current_line['text'] = l['text']
        else:
            dy = abs(l['y'] - current_line['y'])
            if dy < 20 and l['x'] > current_line['x']:
                current_line['text'] += ' ' + l['text']
                current_line['w'] = max(current_line['w'], l['x'] + l['w'] - current_line['x'])
                current_line['h'] = max(current_line['h'], l['y'] + l['h'] - current_line['y'])
            else:
                grouped.append(current_line)
                current_line = dict(l)
                current_line['text'] = l['text']
    if current_line:
        grouped.append(current_line)

    questions = []
    in_question = False
    q_num = 0
    current_q = {'lines': [], 'bbox': None, 'num': 0, 'type': ''}

    question_patterns = [
        (r'^(\d+)[、\.\s]', '单选题'),
        (r'^[（(](\d+)[)）]', '子题'),
        (r'^(单项选择题?|选择题)', '题型'),
        (r'^(填空题)', '题型'),
        (r'^(判断题)', '题型'),
        (r'^(简答题)', '题型'),
        (r'^(问答题)', '题型'),
        (r'^(上机操作题)', '题型'),
    ]

    for l in grouped:
        txt = l['text']
        matched = False
        for pat, qtype in question_patterns:
            m = re.match(pat, txt)
            if m:
                if current_q['lines']:
                    questions.append(current_q)
                q_num += 1
                current_q = {'lines': [l], 'bbox': None, 'num': q_num, 'type': qtype}
                matched = True
                break

        if not matched:
            if current_q['lines']:
                current_q['lines'].append(l)

    if current_q['lines']:
        questions.append(current_q)

    return questions, grouped


def extract_diagrams(img, ocr_data, question_bbox):
    import cv2
    import numpy as np

    qx, qy, qw, qh = question_bbox
    question_img = np.array(img.crop((qx, qy, qx + qw, qy + qh)))

    gray = cv2.cvtColor(question_img, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    diagrams = []
    min_area = 2000
    img_area = qw * qh

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area or area > img_area * 0.8:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        aspect = w / h if h > 0 else 0
        if aspect < 0.2 or aspect > 5:
            continue
        diagram_img = question_img[y:y + h, x:x + w]
        diagrams.append({
            'img': Image.fromarray(cv2.cvtColor(diagram_img, cv2.COLOR_RGB2BGR)),
            'bbox': (x, y, w, h),
            'area': area,
        })

    diagrams.sort(key=lambda d: -d['area'])
    return diagrams


def merge_adjacent_boxes(boxes, y_thresh=30):
    if not boxes:
        return []
    sorted_boxes = sorted(boxes, key=lambda b: b[1])
    merged = [sorted_boxes[0]]
    for b in sorted_boxes[1:]:
        last = merged[-1]
        if abs(b[1] - last[1]) < y_thresh:
            merged[-1] = (
                min(last[0], b[0]),
                min(last[1], b[1]),
                max(last[2], b[2]),
                max(last[3], b[3]),
            )
        else:
            merged.append(b)
    return merged


def process_pdf(pdf_name):
    pdf_path = os.path.join(BASE, pdf_name)
    clean_name = pdf_name_clean(pdf_name)
    out_dir = os.path.join(OUTPUT, clean_name)
    pages_dir = os.path.join(out_dir, 'pages')
    questions_dir = os.path.join(out_dir, 'questions')

    for d in [out_dir, pages_dir, questions_dir]:
        os.makedirs(d, exist_ok=True)

    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    doc.close()

    all_questions = []
    global_q_idx = 0

    for page_num in range(total_pages):
        print(f'[{pdf_name}] Processing page {page_num + 1}/{total_pages}...')

        img = render_page(pdf_path, page_num)
        page_img_path = os.path.join(pages_dir, f'page_{page_num + 1:03d}.png')
        img.save(page_img_path)

        ocr_result = pytesseract.image_to_data(img, lang='chi_sim', output_type=pytesseract.Output.DICT)
        full_text = pytesseract.image_to_string(img, lang='chi_sim')

        text_path = os.path.join(pages_dir, f'page_{page_num + 1:03d}.txt')
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        questions_on_page, _ = detect_questions_from_ocr(ocr_result)

        page_w, page_h = img.size

        if not questions_on_page:
            q_idx = global_q_idx
            global_q_idx += 1
            q_dir = os.path.join(questions_dir, f'q_{q_idx + 1:03d}')
            os.makedirs(q_dir, exist_ok=True)
            img.save(os.path.join(q_dir, 'page.png'))
            with open(os.path.join(q_dir, 'text.txt'), 'w', encoding='utf-8') as f:
                f.write(full_text)
            with open(os.path.join(q_dir, 'info.txt'), 'w', encoding='utf-8') as f:
                f.write(f'Source: Page {page_num + 1}\n')
            continue

        for qi, q in enumerate(questions_on_page):
            lines = q['lines']
            if not lines:
                continue

            min_x = min(l['x'] for l in lines)
            min_y = min(l['y'] for l in lines)
            max_x = max(l['x'] + l['w'] for l in lines)
            max_y = max(l['y'] + l['h'] for l in lines)

            padding = 20
            crop_x = max(0, min_x - padding)
            crop_y = max(0, min_y - padding)
            crop_x2 = min(page_w, max_x + padding)
            crop_y2 = min(page_h, max_y + padding)

            if qi + 1 < len(questions_on_page):
                next_lines = questions_on_page[qi + 1]['lines']
                next_min_y = min(l['y'] for l in next_lines) - padding
                crop_y2 = min(page_h, next_min_y)

            q_text = '\n'.join(l['text'] for l in lines)

            q_idx = global_q_idx
            global_q_idx += 1
            q_dir = os.path.join(questions_dir, f'q_{q_idx + 1:03d}')
            os.makedirs(q_dir, exist_ok=True)

            q_crop = img.crop((crop_x, crop_y, crop_x2, crop_y2))
            q_crop.save(os.path.join(q_dir, 'question.png'))

            with open(os.path.join(q_dir, 'text.txt'), 'w', encoding='utf-8') as f:
                f.write(q_text)

            with open(os.path.join(q_dir, 'info.txt'), 'w', encoding='utf-8') as f:
                f.write(f'Source: Page {page_num + 1}\n')
                f.write(f'Type: {q["type"]}\n')
                f.write(f'Question #{q["num"]}\n')
                f.write(f'Crop: ({crop_x}, {crop_y}) - ({crop_x2}, {crop_y2})\n')

            question_bbox = (crop_x, crop_y, crop_x2 - crop_x, crop_y2 - crop_y)
            diagrams = extract_diagrams(img, ocr_result, question_bbox)

            for di, diag in enumerate(diagrams):
                diag_img = diag['img']
                if diag_img.size[0] > 50 and diag_img.size[1] > 50:
                    diag_img.save(os.path.join(q_dir, f'diagram_{di + 1}.png'))

            all_questions.append({
                'idx': q_idx,
                'page': page_num + 1,
                'text': q_text,
                'type': q['type'],
                'num': q['num'],
                'diagrams': len(diagrams),
            })

    print(f'[{pdf_name}] Done! {len(all_questions)} questions extracted.')
    return all_questions


def generate_summary(all_results):
    summary_path = os.path.join(OUTPUT, 'summary.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('=' * 60 + '\n')
        f.write('扫描PDF题目提取结果汇总\n')
        f.write('=' * 60 + '\n\n')
        for pdf_name, questions in all_results:
            f.write(f'📄 {pdf_name}\n')
            f.write(f'   共提取 {len(questions)} 道题目\n\n')
            for q in questions:
                f.write(f'  Q{q["idx"] + 1:03d} [Page {q["page"]}] [{q["type"]}] '
                        f'{q["text"][:80]}...\n')
                if q['diagrams'] > 0:
                    f.write(f'       (包含 {q["diagrams"]} 张附图)\n')
            f.write('\n')


def main():
    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)

    all_results = []
    for pdf_name in PDFS:
        print(f'\n{"=" * 60}')
        print(f'Processing: {pdf_name}')
        print('=' * 60)
        questions = process_pdf(pdf_name)
        all_results.append((pdf_name, questions))

    generate_summary(all_results)
    print(f'\nDone! All output saved to: {OUTPUT}')


if __name__ == '__main__':
    main()
