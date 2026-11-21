// Lessons of the planetary systems: tappe (one per slide), extended explanations, exercises.
// Codice: PolyForm Noncommercial 1.0.0, https://polyformproject.org/licenses/noncommercial/1.0.0
// Required Notice: Copyright 2026 Marzio De Corato (https://github.com/marzione00/Lab_Geo)
import fs from 'node:fs';
import path from 'node:path';

const LINK = /^(?:#(?:lezione-|esercizi-|laboratorio\/|modulo-|sistema-)[\w/?=&%.,{}":-]*|https:\/\/[^\s<>"]+)$/;

// Inline markdown → nodes: text, {t:'m'} math, {t:'c'} code, {t:'b'}, {t:'i'}, {t:'a'}.
export function inline(text) {
  const out = [];
  let i = 0,
    buf = '';
  const flush = () => {
    if (buf) out.push(buf);
    buf = '';
  };
  const close = (mark, from) => {
    const j = text.indexOf(mark, from);
    if (j < 0) throw Error('Marcatura non chiusa (' + mark + '): ' + text.slice(Math.max(0, from - 30), from + 30));
    return j;
  };
  while (i < text.length) {
    const c = text[i];
    if (c === '\\' && i + 1 < text.length && '$*`[]\\'.includes(text[i + 1])) {
      buf += text[i + 1];
      i += 2;
    } else if (c === '$') {
      const j = close('$', i + 1);
      flush();
      out.push({ t: 'm', v: text.slice(i + 1, j) });
      i = j + 1;
    } else if (c === '`') {
      const j = close('`', i + 1);
      flush();
      out.push({ t: 'c', v: text.slice(i + 1, j) });
      i = j + 1;
    } else if (text.startsWith('**', i)) {
      const j = close('**', i + 2);
      flush();
      out.push({ t: 'b', c: inline(text.slice(i + 2, j)) });
      i = j + 2;
    } else if (c === '*') {
      const j = close('*', i + 1);
      flush();
      out.push({ t: 'i', c: inline(text.slice(i + 1, j)) });
      i = j + 1;
    } else if (c === '[') {
      const m = /^\[([^\]]+)\]\(([^)\s]+)\)/.exec(text.slice(i));
      if (!m) throw Error('Collegamento non valido: ' + text.slice(i, i + 60));
      if (!LINK.test(m[2])) throw Error('Destinazione non ammessa: ' + m[2]);
      flush();
      out.push({ t: 'a', h: m[2], c: inline(m[1]) });
      i += m[0].length;
    } else {
      buf += c;
      i++;
    }
  }
  flush();
  return out;
}

// Blocks: paragraphs, ### headings, - lists, $$ display math $$.
export function blocks(text) {
  const out = [];
  for (const chunk of text.split(/\n\s*\n/)) {
    const raw = chunk.trim();
    if (!raw) continue;
    if (raw.startsWith('### ')) out.push({ t: 'h', c: inline(raw.slice(4).trim()) });
    else if (raw.startsWith('$$')) {
      if (!raw.endsWith('$$') || raw.length < 4) throw Error('Formula non chiusa: ' + raw.slice(0, 40));
      out.push({ t: 'math', v: raw.slice(2, -2).trim() });
    } else if (raw.startsWith('- ')) {
      const items = raw.split(/\n(?=- )/).map(item =>
        inline(
          item
            .slice(2)
            .replace(/\s*\n\s*/g, ' ')
            .trim(),
        ),
      );
      out.push({ t: 'ul', items });
    } else if (/^#/.test(raw)) throw Error('Intestazione non ammessa: ' + raw.split('\n')[0]);
    else out.push({ t: 'p', c: inline(raw.replace(/\s*\n\s*/g, ' ')) });
  }
  return out;
}

// Explanations continue the text of the slide: paragraphs and display formulas only, no headings or lists.
function prose(list, where) {
  const other = list.find(b => b.t !== 'p' && b.t !== 'math');
  if (other) throw Error('Solo paragrafi e formule nel testo (' + where + '): trovato ' + other.t);
  return list;
}

export function explanations(source, slides) {
  const parts = source.split(/^## /m),
    notes = {};
  for (const part of parts.slice(1)) {
    const [head, ...body] = part.split('\n');
    const m = /^(\d+) · (.+)$/.exec(head.trim());
    if (!m) throw Error('Intestazione di tappa non valida: ' + head);
    const page = Number(m[1]),
      slide = slides[page - 1];
    if (!slide) throw Error('Tappa inesistente: ' + page);
    if (slide.title !== m[2]) throw Error('Titolo della tappa ' + page + ' diverso dalla slide: ' + m[2]);
    if (notes[page]) throw Error('Tappa ripetuta: ' + page);
    notes[page] = prose(blocks(body.join('\n')), 'tappa ' + page);
  }
  return { intro: prose(blocks(parts[0]), 'introduzione'), notes };
}

const safe = v =>
  JSON.stringify(v)
    .replace(/</g, '\\u003c')
    .replace(/[\u2028\u2029]/g, c => '\\u' + c.charCodeAt(0).toString(16));

// Project files for the R runtime of the browser: text as strings, binary data in base64.
function projectFiles(dir, list) {
  const decoder = new TextDecoder('utf-8', { fatal: true });
  return Object.fromEntries(
    list.map(f => {
      const buf = fs.readFileSync(path.join(dir, f));
      try {
        return [f, decoder.decode(buf)];
      } catch {
        return [f, { b64: buf.toString('base64') }];
      }
    }),
  );
}

// Links of the slides: site routes, local materials or HTTPS pages; a tappa must exist.
function checkLinks(root, id, lesson, nodes) {
  for (const n of nodes) {
    if (typeof n !== 'object') continue;
    if (n.t === 'a') {
      const tappa = /^#lezione-([A-Z]\d{2})\/(\d+)$/.exec(n.h);
      if (!/^(https:\/\/|#[a-z]|materiali\/[\w./-]+$|assets\/[\w./-]+$)/.test(n.h))
        throw Error('Collegamento non ammesso in ' + id + ': ' + n.h);
      if (tappa && (tappa[1] !== id || Number(tappa[2]) > lesson.pages)) throw Error('Tappa inesistente: ' + n.h);
      if (/^(materiali|assets)\//.test(n.h) && !fs.existsSync(path.join(root, n.h)))
        throw Error('File collegato assente: ' + n.h);
    }
    checkLinks(root, id, lesson, n.c || []);
  }
}

// Files, code and links of a lesson.
function checkLesson(root, id, lesson) {
  const exists = p => fs.existsSync(path.join(root, p));
  if (!exists(lesson.slides[0].image)) throw Error('Copertina assente: ' + id);
  for (const s of lesson.slides) {
    checkLinks(root, id, lesson, s.recall || []);
    for (const it of [...s.items, ...(s.code || [])]) {
      const cells = [...(it.head || []), ...(it.rows || [])].flat().flatMap(cell => cell.c);
      checkLinks(root, id, lesson, [...(it.c || []), ...cells]);
      if (it.t === 'code' && !lesson.code[it.file]) throw Error('Codice assente: ' + it.file);
      if (it.t === 'figure' && !exists(it.src)) throw Error('Figura assente: ' + it.src);
    }
  }
  for (const f of [lesson.pdf, lesson.workbook, lesson.download].filter(Boolean))
    if (!exists(f)) throw Error('File della lezione assente: ' + f);
}

export function buildLessons(root, out) {
  const config = JSON.parse(fs.readFileSync(path.join(root, 'lezioni/lezioni.json'), 'utf8'));
  const index = {};
  fs.mkdirSync(path.join(out, 'assets/lessons'), { recursive: true });
  for (const [id, cfg] of Object.entries(config)) {
    const read = p => fs.readFileSync(path.join(root, p), 'utf8');
    const lesson = JSON.parse(read('content/lezioni/' + id + '.json'));
    const exFile = 'content/esercizi/' + id + '.json';
    const exercises = fs.existsSync(path.join(root, exFile)) ? JSON.parse(read(exFile)) : null;
    const mdFile = 'content/lezioni/' + id + '.md';
    const { intro, notes } = fs.existsSync(path.join(root, mdFile))
      ? explanations(read(mdFile), lesson.slides)
      : { intro: [], notes: {} };
    const files = projectFiles(path.join(root, cfg.source), lesson.project.files);
    checkLesson(root, id, lesson);
    const data = { ...lesson, intro, notes, exercises, project: { ...lesson.project, files } };
    fs.writeFileSync(
      path.join(out, 'assets/lessons', id + '.js'),
      'window.GEO_LESSONS=window.GEO_LESSONS||{};window.GEO_LESSONS.' + id + '=' + safe(data) + ';\n',
    );
    index[id] = {
      title: lesson.title,
      planet: lesson.planet,
      world: lesson.world,
      exercisesWorld: lesson.exercisesWorld,
      pages: lesson.pages,
      explained: Object.keys(notes).map(Number),
      sections: lesson.sections,
      cards: exercises ? exercises.cards.length : 0,
    };
  }
  fs.writeFileSync(path.join(out, 'assets/lesson-index.js'), 'window.GEO_LESSON_INDEX=' + safe(index) + ';\n');
  return index;
}
