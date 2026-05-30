"""
PDF题目提取程序
从扫描版PDF中提取每道题目的文本和附图，按题目组织到独立文件夹。
"""
import fitz
import pytesseract
from PIL import Image
import re
import os
import shutil
import cv2
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
OUTPUT = os.path.join(BASE, 'output')

PDFS = [
    '夸克扫描王_思考练习.pdf',
    '夸克扫描王_思考与练习题1.pdf',
]

DPI = 250


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


def ocr_page(img):
    data = pytesseract.image_to_data(img, lang='chi_sim', output_type=pytesseract.Output.DICT)
    text = pytesseract.image_to_string(img, lang='chi_sim')
    return data, text


def merge_ocr_words_to_lines(words, y_thresh=18):
    """Group OCR words into text lines by y-position proximity."""
    if not words:
        return []

    words.sort(key=lambda w: w['y'] * 10000 + w['x'])
    lines = [[words[0]]]
    for w in words[1:]:
        if abs(w['y'] - lines[-1][-1]['y']) < y_thresh:
            lines[-1].append(w)
        else:
            lines.append([w])

    result = []
    for line in lines:
        line.sort(key=lambda w: w['x'])
        xs = [w['x'] for w in line]
        ys = [w['y'] for w in line]
        ws = [w['w'] for w in line]
        hs = [w['h'] for w in line]
        text = ''.join(w['text'] for w in line)
        if text.strip():
            result.append({
                'text': text,
                'x': min(xs), 'y': min(ys),
                'w': max(xs[i] + ws[i] for i in range(len(line))) - min(xs),
                'h': max(ys[i] + hs[i] for i in range(len(line))) - min(ys),
            })
    return result


def find_question_lines(text_blocks):
    """Identify which text blocks are question markers."""
    question_lines = []
    for b in text_blocks:
        t = b['text'].strip()
        is_question = bool(re.match(
            r'^[（(〈《<\[{]?[\d一二三四五六七八九十]+[)）.．、〉》>\]}]', t
        ))
        is_heading = bool(re.match(
            r'^[一二三四五六七八九十\d]+[、.．]\s*'
            r'(填空题|单项选择题|选择题|判断题|简答题|问答题|计算题|上机操作题)',
            t
        ))
        is_exercise = '思考练习' in t or '思考与练习题' in t
        is_project = bool(re.match(r'^项目[一二三四五六七八九十\d]', t))

        if is_question or is_heading or is_exercise or is_project:
            question_lines.append(b)
    return question_lines


def extract_diagrams(img_cv, region_bbox):
    """Detect embedded diagrams in a question image region."""
    x, y, w, h = region_bbox
    if w < 80 or h < 80:
        return []

    region = img_cv[y:y + h, x:x + w]
    rh, rw = region.shape[:2]

    gray = cv2.cvtColor(region, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    kernel = np.ones((4, 4), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=3)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    diagrams = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 8000 or area > rw * rh * 0.5:
            continue
        bx, by, bw, bh = cv2.boundingRect(cnt)
        aspect = bw / bh if bh > 0 else 0
        if aspect < 0.3 or aspect > 3.0:
            continue
        if bw < 40 or bh < 40:
            continue
        cov = area / (bw * bh)
        if cov < 0.08 or cov > 0.9:
            continue

        sub = region[by:by + bh, bx:bx + bw]
        sub_gray = cv2.cvtColor(sub, cv2.COLOR_RGB2GRAY)
        if np.std(sub_gray) < 15:
            continue

        sub_bgr = cv2.cvtColor(sub, cv2.COLOR_RGB2BGR)
        diagrams.append(Image.fromarray(sub_bgr))

    diagrams.sort(key=lambda img: -img.size[0] * img.size[1])
    uniq = []
    seen = set()
    for img in diagrams:
        key = (img.size[0] // 20, img.size[1] // 20)
        if key not in seen:
            uniq.append(img)
            seen.add(key)
    return uniq[:6]


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

    global_q_idx = 0

    for page_num in range(total_pages):
        print(f'  Page {page_num + 1}/{total_pages}...')
        img = render_page(pdf_path, page_num)
        pw, ph = img.size
        img.save(os.path.join(pages_dir, f'page_{page_num + 1:03d}.png'))

        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        ocr_data, full_text = ocr_page(img)

        with open(os.path.join(pages_dir, f'page_{page_num + 1:03d}.txt'),
                  'w', encoding='utf-8') as f:
            f.write(full_text)

        words = []
        for i, txt in enumerate(ocr_data['text']):
            t = txt.strip()
            if not t:
                continue
            conf = int(ocr_data['conf'][i])
            if conf < 0:
                continue
            words.append({
                'text': t,
                'x': ocr_data['left'][i],
                'y': ocr_data['top'][i],
                'w': ocr_data['width'][i],
                'h': ocr_data['height'][i],
            })

        text_blocks = merge_ocr_words_to_lines(words)
        question_lines = find_question_lines(text_blocks)

        if not question_lines:
            global_q_idx += 1
            q_dir = os.path.join(questions_dir, f'page_{page_num + 1:03d}')
            os.makedirs(q_dir, exist_ok=True)
            img.save(os.path.join(q_dir, 'page.png'))
            with open(os.path.join(q_dir, 'text.txt'), 'w', encoding='utf-8') as f:
                f.write(full_text)
            continue

        for qi, qb in enumerate(question_lines):
            x1 = max(0, qb['x'] - 20)
            y1 = max(0, qb['y'] - 20)
            x2 = min(pw, qb['x'] + qb['w'] + 20)
            y2 = min(ph, qb['y'] + qb['h'] + 20)

            if qi + 1 < len(question_lines):
                y2 = min(ph, question_lines[qi + 1]['y'] - 20)

            for b in text_blocks:
                if b['y'] > y1 and b['y'] < y2 and b is not qb:
                    x2 = max(x2, min(pw, b['x'] + b['w'] + 20))
                    y2 = max(y2, min(ph, b['y'] + b['h'] + 20))

            crop_w = x2 - x1
            crop_h = y2 - y1
            if crop_w < 60 or crop_h < 30:
                continue

            global_q_idx += 1
            q_dir = os.path.join(questions_dir, f'q_{global_q_idx:03d}')
            os.makedirs(q_dir, exist_ok=True)

            img.crop((x1, y1, x2, y2)).save(os.path.join(q_dir, 'question.png'))

            q_text = qb['text']
            with open(os.path.join(q_dir, 'text.txt'), 'w', encoding='utf-8') as f:
                f.write(q_text)

            with open(os.path.join(q_dir, 'info.txt'), 'w', encoding='utf-8') as f:
                f.write(f'Page: {page_num + 1}\n')
                f.write(f'Text: {q_text}\n')

            diagrams = extract_diagrams(img_cv, (x1, y1, crop_w, crop_h))
            for di, diag_img in enumerate(diagrams):
                if diag_img.size[0] > 50 and diag_img.size[1] > 50:
                    diag_img.save(os.path.join(q_dir, f'diagram_{di + 1}.png'))

    print(f'  Done! {global_q_idx} questions from {pdf_name}')


def generate_report(all_results):
    with open(os.path.join(OUTPUT, 'summary.txt'), 'w', encoding='utf-8') as f:
        f.write('=' * 60 + '\n')
        f.write('PDF题目提取结果汇总\n')
        f.write('=' * 60 + '\n\n')
        for pdf_name, q_count in all_results:
            f.write(f'{pdf_name}: {q_count} 道题目\n\n')


def main():
    if os.path.exists(OUTPUT):
        shutil.rmtree(OUTPUT)

    all_results = []
    for pdf_name in PDFS:
        print(f'\nProcessing: {pdf_name}')
        process_pdf(pdf_name)
        all_results.append((pdf_name, ''))

    print(f'\nDone! Output: {OUTPUT}')


if __name__ == '__main__':
    main()
