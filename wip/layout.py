"""Laws of Malaysia reprint PDFs (Attorney General's Chambers) -> provisions. gitlaw-MY.

The reprints are typeset alike (Times; PyMuPDF reads their text layer):
- running heads (act title, page number, "[Article 3]") sit in the top 72 pt of every page: dropped;
- NOTES pages (the editor's amendment notes, a line "NOTES" at the top) are kept apart: read_notes();
- footnotes ("*This Part has been amended by ... not yet in force") are set in 8 pt or less: dropped, and so are
  the asterisk markers that point to them;
- small capitals are a font "...-SC700" whose lower-case letters are set smaller: they are read as capitals
  ("Article 160a" -> "Article 160A", "Part" -> "PART" is avoided by keeping the full-size first letter case:
  only letters set smaller than the span's full size are raised);
- a provision starts at a bold number at the start of a line ("49a." -> 49A), with its bold heading on the
  line(s) before; PART and CHAPTER headings are centred small-capital lines;
- the schedules start after a page that reads "SCHEDULES"; each starts at a centred bold small-capital line
  "First Schedule" etc. and is one unit;
- a paragraph starts with a tab or a label, after a vertical gap wider than 1.45 lines, or when a line starts
  left of the paragraph's first line; other lines are joined to it with one space.
"""
import re
import unicodedata

import fitz

SC = 'SC700'
ORD = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth', 'eleventh',
       'twelfth', 'thirteenth', 'fourteenth']
ROMAN = {'I': 1, 'V': 5, 'X': 10, 'L': 50}


def roman(s):
    n = 0
    for a, b in zip(s, s[1:] + ' '):
        v = ROMAN[a]
        n += -v if ROMAN.get(b, 0) > v else v
    return n


def span_text(s, full):
    t = s['text']
    if SC in s['font'] and s['size'] < full - 1.5:
        t = t.upper()
    return t


def norm(t):
    t = t.replace(' ', ' ').replace(' ', '\t').replace(' ', '\t').replace(' ', ' ')
    t = t.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    t = t.replace('–', '-').replace('', '')
    t = unicodedata.normalize('NFC', t)
    return t


def is_running_head(spans, size, y):
    """Act title (italic), page number, or "[Article 3]" / "[Second Schedule]" (small capitals, 10 pt)."""
    vis = [x for x in spans if x['text'].strip()]
    if not vis:
        return True
    t = ''.join(x['text'] for x in vis).strip()
    if y < 60:
        return True                                      # act title and page number band
    return SC in vis[0]['font'] and size <= 10.5 and ('[' in t or ']' in t)


def page_footnotes(page):
    """Footnote lines (8 pt and smaller) of a provisions page, joined, for review and for decisions."""
    out = []
    for bl in page.get_text('dict')['blocks']:
        for l in bl.get('lines', []):
            spans = [x for x in l['spans'] if x['text']]
            if spans and max(x['size'] for x in spans) <= 8.6 and l['bbox'][1] > 70:
                out.append(norm(''.join(span_text(x, max(y['size'] for y in spans)) for x in spans)))
    return ' '.join(' '.join(out).split())


def page_lines(page):
    """[(x, y, size, bold, sc_first, text)] for one page, lines at one height merged, heads/footnotes dropped."""
    raw = []
    for bl in page.get_text('dict')['blocks']:
        for l in bl.get('lines', []):
            spans = [s for s in l['spans'] if s['text']]
            if not spans:
                continue
            size = max(s['size'] for s in spans)
            y = l['bbox'][1]
            if y < 70 and is_running_head(spans, size, y):
                continue
            vis = [s for s in spans if s['text'].strip()]
            if vis and SC in vis[0]['font'] and size <= 10.5 and vis[0]['text'].strip().startswith('[')                     and ''.join(s['text'] for s in vis).strip().endswith(']'):
                continue                                 # running reference "[Article 38]" lower on a page
            raw.append([l['bbox'][0], y, size, spans])
    raw.sort(key=lambda r: (round(r[1] / 3), r[0]))
    merged = []
    for r in raw:
        if merged and abs(merged[-1][1] - r[1]) < 3:
            merged[-1][3] = merged[-1][3] + r[3]
            merged[-1][2] = max(merged[-1][2], r[2])
        else:
            merged.append(r)
    out = []
    for x, y, size, spans in merged:
        if size <= 8.6:
            continue                                     # footnotes and notes
        txt = norm(''.join(span_text(s, size) for s in spans))
        if not txt.strip():
            continue
        # x of the first visible character
        for s in spans:
            if s['text'].strip():
                x = s['bbox'][0]
                break
        first = next((s for s in spans if s['text'].strip(' 	*')), None) or             next(s for s in spans if s['text'].strip())
        bold = 'Bold' in first['font']
        allbold = all('Bold' in s['font'] for s in spans if s['text'].strip(' 	*'))
        out.append({'x': x, 'y': y, 'size': size, 'bold': bold, 'allbold': allbold,
                    'sc': SC in first['font'], 'lead_tab': txt[:1] == '\t' or spans[0]['text'][:1] == '\t',
                    'text': txt, 'spans': spans})
    return out


def is_notes_page(page):
    for bl in page.get_text('dict')['blocks']:
        for l in bl.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if 60 < l['bbox'][1] < 110 and t == 'NOTES':
                return True
    return False


def clean(t):
    t = re.sub(r'(?<=[\w\)\]\.,;:])\*+', '', t)          # footnote markers after a word
    t = re.sub(r'(^|(?<=[\s\(\[]))\*+(?=\S)', '', t)       # markers before a word
    t = re.sub(r'[ \t]+', ' ', t).strip()
    t = t.replace('( ', '(').replace(' )', ')') if False else t
    return t


ART_RE = re.compile(r'^[\s*]*(\d+[A-Z]*)\.(?=\s|$)')


def body_pages(doc):
    """Page indexes of the provisions: from the page with the first bold "1." to the LIST OF AMENDMENTS."""
    start = None
    for i in range(4, doc.page_count):
        if any(ln['bold'] and re.match(r'^1\.(\s|$)', ln['text'].strip()) for ln in page_lines(doc[i])):
            start = i
            break
    for i in range(start + 1, doc.page_count):
        if re.search(r'^\s*LIST OF AMENDMENTS\s*$', doc[i].get_text(), re.M):
            return start, i
    return start, doc.page_count


def ord_index(word):
    return ORD.index(word.lower()) + 1


def parse(pdf_bytes, body_size=12.0):
    """Ordered list of units {key, label, kind, heading, lines[]} from a reprint."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    start, end = body_pages(doc)
    units = []
    cur = None
    para = None            # current paragraph dict {x, text}
    pending_heading = []
    part = None
    in_schedules = False
    centre_block = None    # collecting a PART / CHAPTER title
    last_y = None
    last_size = None

    def close_para():
        nonlocal para
        if para is not None and cur is not None:
            cur['lines'].append(clean(para['text']))
        para = None

    def new_unit(key, label, kind, heading=None):
        nonlocal cur
        close_para()
        cur = {'key': key, 'label': label, 'kind': kind, 'heading': heading, 'lines': []}
        units.append(cur)

    for pi in range(start, end):
        page = doc[pi]
        if is_notes_page(page):
            continue
        lines = page_lines(page)
        pw = page.rect.width
        last_y = None
        for ln in lines:
            t = ln['text']
            ts = clean(t)
            if not ts:
                continue
            centred = abs((ln['x'] + (pw - ln['x'])) / 2 - pw / 2) < 1 and False
            # centred lines: start well right of the text block and are short
            is_centre = ln['x'] > 120 and len(ts) < 70 and not ln['lead_tab']
            if not in_schedules and ts == 'SCHEDULES' and ln['size'] > 13:
                close_para()
                in_schedules = True
                cur = None
                continue
            if in_schedules and ts == 'SCHEDULES':
                continue
            m_sch = re.match(r'^(\w+) Schedule$', ts)
            if in_schedules and m_sch and m_sch.group(1).lower() in ORD and ln['bold'] and ln['sc']:
                n = ord_index(m_sch.group(1))
                new_unit(f'sch-{n:02d}', f'{m_sch.group(1)} Schedule', 'schedule')
                cur['lines'].append('# ' + ts)
                last_y, last_size = ln['y'], ln['size']
                continue
            m_part = re.match(r'^PART ([IVXL]+)(?:\s*[-—]\s*(.*))?$', ts.upper()) if (ln['sc'] or is_centre) else None
            m_ch = re.match(r'^CHAPTER (\d+)(?:\s*[-—]\s*(.*))?$', ts.upper()) if (ln['sc'] or is_centre) else None
            if not in_schedules and is_centre and (m_part or m_ch):
                if m_part:
                    part = roman(m_part.group(1))
                    new_unit(f'part-{part:02d}', f'Part {m_part.group(1)}', 'part')
                    cur['lines'].append('# ' + re.sub(r'^PART', 'Part', ts.upper()))
                else:
                    new_unit(f'part-{part:02d}-chapter-{int(m_ch.group(1)):02d}', f'Part {part}, Chapter {m_ch.group(1)}',
                             'chapter')
                    cur['lines'].append('# ' + ts)
                centre_block = cur
                last_y, last_size = ln['y'], ln['size']
                continue
            if not in_schedules and centre_block is not None and cur is centre_block and is_centre and not ln['bold']:
                close_para()
                para = {'x': ln['x'], 'text': ts}
                last_y, last_size = ln['y'], ln['size']
                continue
            if not in_schedules and ln['allbold'] and not ART_RE.match(t):
                # an article heading (may run over two lines)
                close_para()
                if pending_heading and last_y is not None and ln['y'] - last_y < 1.45 * ln['size']:
                    pending_heading[-1] += ' ' + ts
                else:
                    pending_heading = [ts]
                centre_block = None
                last_y, last_size = ln['y'], ln['size']
                continue
            m_art = ART_RE.match(t) if (not in_schedules and ln['bold']) else None
            if m_art:
                num = m_art.group(1)
                mm = re.match(r'^(\d+)([A-Z]*)$', num)
                key = f'art-{int(mm.group(1)):03d}{mm.group(2).lower()}'
                head = ' '.join(pending_heading) if pending_heading else None
                pending_heading = []
                new_unit(key, f'Art. {num}', 'art', head)
                cur['lines'].append(f'# Article {num}' + (f'. {head}' if head else ''))
                centre_block = None
                rest = t[m_art.end():]
                para = {'x': ln['x'], 'text': f'{num}. ' + rest.strip()}
                last_y, last_size = ln['y'], ln['size']
                continue
            if cur is None:
                last_y, last_size = ln['y'], ln['size']
                continue
            centre_block = None if not in_schedules else centre_block
            gap = (ln['y'] - last_y) if last_y is not None else None
            starts = ln['lead_tab'] or re.match(r'^\s*(\(\w{1,5}\)|\d+[A-Z]*\.)(\s|$)', t) or ln['allbold'] \
                or (in_schedules and (ln['bold'] or is_centre))
            new = (para is None or starts or (gap is not None and gap > 1.45 * ln['size'])
                   or (para is not None and ln['x'] < para['x'] - 2))
            if new:
                close_para()
                para = {'x': ln['x'], 'text': ts}
            else:
                if para['text'].endswith('-') or para['text'].endswith('—'):
                    para['text'] += ts
                else:
                    para['text'] += ' ' + ts
            last_y, last_size = ln['y'], ln['size']
    close_para()
    out = []
    for u in units:
        lines = [l for l in u['lines'] if l]
        u['text'] = '\n'.join(lines) + '\n'
        out.append(u)
    return out


def read_notes(pdf_bytes):
    """The text of every NOTES page, as one string with page breaks (for crediting changes)."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    parts = []
    for i in range(doc.page_count):
        if is_notes_page(doc[i]):
            parts.append(norm(doc[i].get_text()))
    return '\n'.join(parts)
