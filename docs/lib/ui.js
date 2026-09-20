/* ui.js — the parts every module shares: theme, status badges, the
   "where this comes from" line, and a loader that refuses to show a number
   without the file and line it came from.

   No analytics, no external request: the only network access is the page
   fetching its own docs/data/*.json from the same origin. */

/** Blob links into the repository.  Nothing is fetched from here at runtime;
    it is where a reader goes to check a digit. */
export const REPO = 'https://github.com/alexander-stottmeister/cft-cmi/blob/main/';

const STATUS_TEXT = {
  proved: 'a complete structured proof',
  refereed: 'a complete structured proof an independent referee pass accepted',
  certified: 'a rigorous bound from ball arithmetic or a spectral window',
  numerical: 'measured, with an error bar; not a theorem',
  conditional: 'holds only under the hypotheses named beside it',
  conjectural: 'believed, with partial evidence; not proved',
  open: 'unsettled'
};

// ------------------------------------------------------------------ theme
export function initTheme(button) {
  const root = document.documentElement;
  const read = () => { try { return localStorage.getItem('cftcmi-theme'); } catch (e) { return null; } };
  const write = v => { try { localStorage.setItem('cftcmi-theme', v); } catch (e) {} };
  const current = () => root.getAttribute('data-theme')
    || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  const label = () => { if (button) button.textContent = current() === 'dark' ? 'Light theme' : 'Dark theme'; };
  const stored = read();
  if (stored === 'dark' || stored === 'light') root.setAttribute('data-theme', stored);
  label();
  if (button) {
    button.hidden = false;
    button.addEventListener('click', () => {
      const next = current() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      write(next);
      label();
      document.dispatchEvent(new CustomEvent('themechange', { detail: next }));
    });
  }
}

/** Tell the stylesheet that the module really loaded, so the enhanced view may
    replace the static one.  Called only after a module has initialised. */
export const enableJS = () => document.documentElement.classList.add('has-js');

// ------------------------------------------------------------------ badges
export function badge(status, hypotheses) {
  const b = document.createElement('span');
  b.className = 'badge ' + status;
  b.textContent = hypotheses && hypotheses.length ? 'conditional' : status;
  if (hypotheses && hypotheses.length) {
    b.className = 'badge conditional';
    b.title = 'conditional on ' + hypotheses.join(', ') + ' — ' + (STATUS_TEXT[status] || '');
  } else {
    b.title = STATUS_TEXT[status] || status;
  }
  return b;
}

export function el(tag, attrs = {}, children = []) {
  const n = document.createElement(tag);
  for (const k in attrs) {
    if (k === 'class') n.className = attrs[k];
    else if (k === 'html') n.innerHTML = attrs[k];
    else if (k === 'text') n.textContent = attrs[k];
    else if (attrs[k] !== undefined && attrs[k] !== null) n.setAttribute(k, attrs[k]);
  }
  for (const c of [].concat(children)) if (c) n.appendChild(typeof c === 'string' ? document.createTextNode(c) : c);
  return n;
}

/** "Where this comes from": the document that proves it and the script that
    computed it, as links into the repository. */
export function provenance(items, prefix = 'Where this comes from: ') {
  const p = el('p', { class: 'provenance' }, [prefix]);
  items.forEach((it, i) => {
    if (i) p.appendChild(document.createTextNode(' · '));
    const href = it.href || (REPO + it.path + (it.line ? '#L' + it.line : ''));
    p.appendChild(el('a', { href, rel: 'noopener' }, [it.label || it.path]));
  });
  return p;
}

// ------------------------------------------------------- numbers with a source
export function fmtValue(v, sig = 6) {
  if (v === null || v === undefined || !isFinite(v)) return '—';
  const a = Math.abs(v);
  if (a !== 0 && (a < 1e-4 || a >= 1e6)) {
    const [m, e] = v.toExponential(Math.max(0, sig - 1)).split('e');
    return m + '×10' + sup(Number(e));
  }
  return String(+v.toPrecision(sig));
}
const SUPS = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴',
  5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
const sup = n => String(n).split('').map(c => SUPS[c] || c).join('');

/** Render one record as value, error and source link together.  A record with
    no source is refused: a number without provenance must not reach the page. */
export function renderRecord(rec, opts = {}) {
  if (!rec) return el('span', { class: 'value', text: '—' });
  if (!rec.source) throw new Error('renderRecord: a number with no source may not be displayed');
  const span = el('span', { class: 'value' }, [fmtValue(rec.value, opts.sig || 6)]);
  if (rec.error !== null && rec.error !== undefined) {
    span.appendChild(el('span', { class: 'err' }, [' ± ' + fmtValue(rec.error, 2)]));
  }
  const wrap = el('span', {}, [span, ' ', badge(rec.status), ' ']);
  wrap.appendChild(el('a', {
    class: 'provenance', href: REPO + rec.source + '#L' + rec.line, rel: 'noopener',
    title: rec.label || ''
  }, [rec.source + ':' + rec.line]));
  return wrap;
}

/** a readout cell: label above, value + badge + source below */
export function readoutCell(key, rec, opts) {
  return el('div', { class: 'cell' }, [el('span', { class: 'k', text: key }), renderRecord(rec, opts)]);
}

// --------------------------------------------------------------- data access
export class Data {
  constructor(json) {
    this.json = json;
    this.byId = new Map();
    for (const r of json.records) this.byId.set(r.id, r);
  }
  get(id) {
    const r = this.byId.get(id);
    if (!r) throw new Error('no record "' + id + '" in ' + this.json.module);
    return r;
  }
  series(name) { return this.json.records.filter(r => r.series === name).sort((a, b) => a.x - b.x); }
  xy(name) { return this.series(name).map(r => [r.x, r.value, r.error]); }
}

export async function loadData(path) {
  const res = await fetch(path, { cache: 'no-cache' });
  if (!res.ok) throw new Error('cannot read ' + path + ' (' + res.status + ')');
  return new Data(await res.json());
}

/** Explain, in the page, why the interactive view did not come up. */
export function failNotice(host, err) {
  const p = el('div', { class: 'panel' }, [
    el('p', {}, [el('strong', { text: 'The interactive view did not start. ' }),
      'The text and the figure below are the whole claim; the animation is an enhancement. ']),
    el('p', { class: 'provenance' }, ['Reason: ' + err.message + '. Opening these pages straight from '
      + 'the file system blocks ES modules and local JSON in most browsers; serve the folder instead, '
      + 'for example with "python3 -m http.server" inside docs/. Nothing is ever fetched from another site.'])
  ]);
  host.prepend(p);
}

// --------------------------------------------------------------------- KaTeX
/** Render every [data-tex] element with the vendored KaTeX, if it loaded.
    The element's text content is already a readable fallback, so a page with
    no KaTeX (or no JavaScript at all) still says the same thing. */
export function renderMath(root = document) {
  if (typeof window === 'undefined' || !window.katex) return false;
  for (const n of root.querySelectorAll('[data-tex]')) {
    try {
      window.katex.render(n.getAttribute('data-tex'), n, {
        throwOnError: false, displayMode: n.hasAttribute('data-display'), output: 'html'
      });
    } catch (e) { /* keep the text fallback */ }
  }
  return true;
}
