/* plot.js — the small SVG plotting layer every module of this site shares.
   Vanilla ES module: no framework, no bundler, no network request.

   const p = new Plot(svgElement, {xScale:'log', xDomain:[1e-3,20], yDomain:[0,1]});
   p.onRender(() => { p.axes(); p.curve(pts, {stroke:'var(--series-1)'}); });
   p.render();                                  // and again on every resize
*/

const NS = 'http://www.w3.org/2000/svg';

export function el(name, attrs, parent) {
  const n = document.createElementNS(NS, name);
  for (const k in attrs) if (attrs[k] !== undefined && attrs[k] !== null) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}

/** "nice" linear ticks covering [lo,hi] with about `count` of them. */
export function linTicks(lo, hi, count = 6) {
  if (!(hi > lo)) return [lo];
  const raw = (hi - lo) / count;
  const mag = Math.pow(10, Math.floor(Math.log10(raw)));
  const step = [1, 2, 2.5, 5, 10].map(m => m * mag).find(s => s >= raw * 0.999) || 10 * mag;
  const out = [];
  for (let t = Math.ceil(lo / step) * step; t <= hi * (1 + 1e-12); t += step) out.push(+t.toPrecision(12));
  return out;
}

/** decade ticks for a log axis; minor ticks are returned flagged. */
export function logTicks(lo, hi) {
  const out = [];
  const a = Math.floor(Math.log10(lo)), b = Math.ceil(Math.log10(hi));
  for (let d = a; d <= b; d++) {
    for (const m of [1, 2, 3, 4, 5, 6, 7, 8, 9]) {
      const v = m * Math.pow(10, d);
      if (v < lo * (1 - 1e-12) || v > hi * (1 + 1e-12)) continue;
      out.push({ v, major: m === 1 });
    }
  }
  return out;
}

export function fmt(v, sig = 4) {
  if (v === null || v === undefined || !isFinite(v)) return '—';
  const a = Math.abs(v);
  if (a !== 0 && (a < 1e-3 || a >= 1e5)) return v.toExponential(Math.max(0, sig - 1)).replace('e', '×10^');
  return String(+v.toPrecision(sig));
}

export class Plot {
  constructor(svg, opts = {}) {
    this.svg = svg;
    this.o = Object.assign({
      aspect: 0.58, minH: 180, maxH: 420,
      margin: { l: 54, r: 14, t: 14, b: 38 },
      xScale: 'linear', yScale: 'linear',
      xDomain: [0, 1], yDomain: [0, 1],
      xLabel: '', yLabel: '', xTickCount: 6, yTickCount: 5
    }, opts);
    this.root = el('g', {}, svg);
    svg.classList.add('plot');
    this._render = () => {};
    this.W = 640; this.H = 360;
    if (typeof ResizeObserver !== 'undefined') {
      this._ro = new ResizeObserver(() => this.render());
      this._ro.observe(svg.parentNode || svg);
    } else {
      window.addEventListener('resize', () => this.render());
    }
  }

  onRender(fn) { this._render = fn; return this; }

  domain(xDomain, yDomain) {
    if (xDomain) this.o.xDomain = xDomain;
    if (yDomain) this.o.yDomain = yDomain;
    return this;
  }

  measure() {
    const host = this.svg.parentNode;
    const w = Math.max(240, Math.round((host && host.clientWidth) || this.svg.clientWidth || 640));
    const h = Math.min(this.o.maxH, Math.max(this.o.minH, Math.round(w * this.o.aspect)));
    this.W = w; this.H = h;
    this.svg.setAttribute('viewBox', `0 0 ${w} ${h}`);
    this.svg.setAttribute('width', w);
    this.svg.setAttribute('height', h);
  }

  render() {
    // A re-render rebuilds the subtree, so a focused handle would lose focus and
    // the next arrow key would go to <body>.  Remember it by key and restore it.
    const active = this.root.ownerDocument && this.root.ownerDocument.activeElement;
    const key = active && this.root.contains(active)
      ? active.getAttribute('data-handle-key') : null;
    this.measure();
    while (this.root.firstChild) this.root.removeChild(this.root.firstChild);
    this._render(this);
    if (key) {
      const again = this.root.querySelector('[data-handle-key="' + key + '"]');
      if (again && again.focus) again.focus({ preventScroll: true });
    }
    return this;
  }

  get inner() {
    const m = this.o.margin;
    return { x0: m.l, x1: this.W - m.r, y0: this.H - m.b, y1: m.t };
  }

  sx(v) {
    const { x0, x1 } = this.inner, [a, b] = this.o.xDomain;
    const t = this.o.xScale === 'log'
      ? (Math.log(Math.max(v, 1e-300)) - Math.log(a)) / (Math.log(b) - Math.log(a))
      : (v - a) / (b - a);
    return x0 + t * (x1 - x0);
  }
  sy(v) {
    const { y0, y1 } = this.inner, [a, b] = this.o.yDomain;
    const t = this.o.yScale === 'log'
      ? (Math.log(Math.max(v, 1e-300)) - Math.log(a)) / (Math.log(b) - Math.log(a))
      : (v - a) / (b - a);
    return y0 + t * (y1 - y0);
  }
  ix(px) {
    const { x0, x1 } = this.inner, [a, b] = this.o.xDomain, t = (px - x0) / (x1 - x0);
    return this.o.xScale === 'log' ? Math.exp(Math.log(a) + t * (Math.log(b) - Math.log(a))) : a + t * (b - a);
  }
  iy(py) {
    const { y0, y1 } = this.inner, [a, b] = this.o.yDomain, t = (py - y0) / (y1 - y0);
    return this.o.yScale === 'log' ? Math.exp(Math.log(a) + t * (Math.log(b) - Math.log(a))) : a + t * (b - a);
  }

  /** pointer event -> data coordinates, correct under any CSS scaling */
  toData(ev) {
    const r = this.svg.getBoundingClientRect();
    const px = (ev.clientX - r.left) * this.W / r.width;
    const py = (ev.clientY - r.top) * this.H / r.height;
    return { x: this.ix(px), y: this.iy(py), px, py };
  }

  axes(opts = {}) {
    const { x0, x1, y0, y1 } = this.inner, g = el('g', { class: 'axis' }, this.root);
    const grid = el('g', { class: 'grid' }, this.root);
    el('line', { x1: x0, x2: x1, y1: y0, y2: y0 }, g);
    el('line', { x1: x0, x2: x0, y1: y0, y2: y1 }, g);
    const xs = this.o.xScale === 'log'
      ? logTicks(this.o.xDomain[0], this.o.xDomain[1])
      : linTicks(this.o.xDomain[0], this.o.xDomain[1], this.o.xTickCount).map(v => ({ v, major: true }));
    for (const t of xs) {
      const X = this.sx(t.v);
      el('line', { x1: X, x2: X, y1: y0, y2: y0 + (t.major ? 5 : 3) }, g);
      if (t.major) {
        if (opts.grid !== false) el('line', { x1: X, x2: X, y1: y0, y2: y1 }, grid);
        el('text', { x: X, y: y0 + 17, 'text-anchor': 'middle' }, g).textContent = fmt(t.v, 3);
      }
    }
    const ys = this.o.yScale === 'log'
      ? logTicks(this.o.yDomain[0], this.o.yDomain[1]).filter(t => t.major)
      : linTicks(this.o.yDomain[0], this.o.yDomain[1], this.o.yTickCount).map(v => ({ v, major: true }));
    for (const t of ys) {
      const Y = this.sy(t.v);
      el('line', { x1: x0 - 5, x2: x0, y1: Y, y2: Y }, g);
      if (opts.grid !== false) el('line', { x1: x0, x2: x1, y1: Y, y2: Y }, grid);
      el('text', { x: x0 - 8, y: Y + 4, 'text-anchor': 'end' }, g).textContent = fmt(t.v, 3);
    }
    if (this.o.xLabel) el('text', { x: (x0 + x1) / 2, y: this.H - 4, 'text-anchor': 'middle' }, g)
      .textContent = this.o.xLabel;
    if (this.o.yLabel) {
      const t = el('text', { x: 12, y: (y0 + y1) / 2, 'text-anchor': 'middle',
        transform: `rotate(-90 12 ${(y0 + y1) / 2})` }, g);
      t.textContent = this.o.yLabel;
    }
    return this;
  }

  path(pts, attrs = {}) {
    const d = pts.filter(p => isFinite(p[0]) && isFinite(p[1]))
      .map((p, i) => `${i ? 'L' : 'M'}${this.sx(p[0]).toFixed(2)},${this.sy(p[1]).toFixed(2)}`).join('');
    return el('path', Object.assign({ class: 'curve', d }, attrs), this.root);
  }
  curve(pts, o = {}) {
    return this.path(pts, { stroke: o.stroke || 'var(--series-1)', 'stroke-width': o.width || 2,
      'stroke-dasharray': o.dash, opacity: o.opacity });
  }
  /** a filled band between two same-x series: the certified bracket */
  band(lo, hi, o = {}) {
    const d = lo.map((p, i) => `${i ? 'L' : 'M'}${this.sx(p[0]).toFixed(2)},${this.sy(p[1]).toFixed(2)}`).join('')
      + hi.slice().reverse().map(p => `L${this.sx(p[0]).toFixed(2)},${this.sy(p[1]).toFixed(2)}`).join('') + 'Z';
    return el('path', { d, fill: o.fill || 'var(--series-1)', opacity: o.opacity ?? 0.16, stroke: 'none' }, this.root);
  }
  dots(pts, o = {}) {
    const g = el('g', {}, this.root);
    for (const p of pts) {
      const X = this.sx(p[0]), Y = this.sy(p[1]);
      if (!isFinite(X) || !isFinite(Y)) continue;
      if (p[2]) {                                  // symmetric error bar in y
        const lo = this.sy(p[1] - p[2]), hi = this.sy(p[1] + p[2]);
        el('line', { x1: X, x2: X, y1: lo, y2: hi, stroke: o.stroke || 'var(--series-1)', 'stroke-width': 1.4 }, g);
        el('line', { x1: X - 3.5, x2: X + 3.5, y1: lo, y2: lo, stroke: o.stroke || 'var(--series-1)', 'stroke-width': 1.4 }, g);
        el('line', { x1: X - 3.5, x2: X + 3.5, y1: hi, y2: hi, stroke: o.stroke || 'var(--series-1)', 'stroke-width': 1.4 }, g);
      }
      if (o.shape === 'square') {
        const r = o.r || 3.4;
        el('rect', { x: X - r, y: Y - r, width: 2 * r, height: 2 * r, fill: o.fill || 'var(--panel)',
          stroke: o.stroke || 'var(--series-1)', 'stroke-width': o.width || 1.6 }, g);
      } else {
        el('circle', { cx: X, cy: Y, r: o.r || 3.4, fill: o.fill || 'var(--series-1)',
          stroke: o.stroke, 'stroke-width': o.width }, g);
      }
    }
    return g;
  }
  hline(y, o = {}) {
    const { x0, x1 } = this.inner;
    return el('line', { x1: x0, x2: x1, y1: this.sy(y), y2: this.sy(y), stroke: o.stroke || 'var(--muted)',
      'stroke-width': o.width || 1.3, 'stroke-dasharray': o.dash || '5 4' }, this.root);
  }
  vline(x, o = {}) {
    const { y0, y1 } = this.inner;
    return el('line', { x1: this.sx(x), x2: this.sx(x), y1: y0, y2: y1, stroke: o.stroke || 'var(--muted)',
      'stroke-width': o.width || 1.3, 'stroke-dasharray': o.dash || '5 4' }, this.root);
  }
  text(x, y, s, o = {}) {
    const t = el('text', { x: this.sx(x) + (o.dx || 0), y: this.sy(y) + (o.dy || 0),
      class: o.small ? 'small' : 'label', 'text-anchor': o.anchor || 'start', fill: o.fill }, this.root);
    t.textContent = s;
    return t;
  }
  legend(items, o = {}) {
    const g = el('g', {}, this.root);
    let y = (o.y ?? this.inner.y1 + 8);
    const x = o.x ?? this.inner.x0 + 8;
    for (const it of items) {
      el('line', { x1: x, x2: x + 18, y1: y, y2: y, stroke: it.stroke, 'stroke-width': it.width || 2,
        'stroke-dasharray': it.dash }, g);
      const t = el('text', { x: x + 24, y: y + 4, class: 'small' }, g);
      t.textContent = it.label;
      y += 15;
    }
    return g;
  }
}

/** Make `node` draggable in data coordinates, and movable with the arrow keys.

    The move listeners live on `window`, not on the node: a module typically
    redraws (and so replaces) its handles on every update, and a listener bound
    to the node would lose the drag on the first move. */
export function draggable(plot, node, opts) {
  const { onMove, step = 0.01, axis = 'x', label, key } = opts || {};
  node.classList.add('handle');
  node.setAttribute('tabindex', '0');
  node.setAttribute('role', 'slider');
  if (label) node.setAttribute('aria-label', label);
  // The focus key must be STABLE across a re-render.  Defaulting it to the label
  // is wrong whenever the label carries the current value, which is exactly what
  // a good aria-label does, so pass `key` for anything value-bearing (P4b).
  const focusKey = key || label;
  if (focusKey) node.setAttribute('data-handle-key', focusKey);
  if (opts && opts.aria) {
    const a = opts.aria;
    if (a.min !== undefined) node.setAttribute('aria-valuemin', String(a.min));
    if (a.max !== undefined) node.setAttribute('aria-valuemax', String(a.max));
    if (a.now !== undefined) node.setAttribute('aria-valuenow', String(a.now));
    if (a.text !== undefined) node.setAttribute('aria-valuetext', String(a.text));
  }
  const emit = ev => { const d = plot.toData(ev); onMove(d.x, d.y, ev); };
  const onPointerMove = ev => { ev.preventDefault(); emit(ev); };
  const stop = () => {
    window.removeEventListener('pointermove', onPointerMove);
    window.removeEventListener('pointerup', stop);
    window.removeEventListener('pointercancel', stop);
  };
  node.addEventListener('pointerdown', ev => {
    ev.preventDefault();
    if (node.focus) node.focus({ preventScroll: true });
    emit(ev);
    window.addEventListener('pointermove', onPointerMove, { passive: false });
    window.addEventListener('pointerup', stop);
    window.addEventListener('pointercancel', stop);
  });
  node.addEventListener('keydown', ev => {
    const big = ev.shiftKey ? 10 : 1;
    let d = 0;
    if (ev.key === 'ArrowLeft' || ev.key === 'ArrowDown') d = -step * big;
    else if (ev.key === 'ArrowRight' || ev.key === 'ArrowUp') d = step * big;
    else return;
    ev.preventDefault();
    onMove(null, null, ev, d, axis);
  });
  return node;
}
