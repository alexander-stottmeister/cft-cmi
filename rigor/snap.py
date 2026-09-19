#!/usr/bin/env python
"""Render a PDF page (or a clipped region) to PNG for citation screenshots.
Usage: snap.py <pdf> <page(1-based)> <out.png> [--clip x0 y0 x1 y1 (fractions of page, 0..1)] [--dpi 170] [--find "text"]
--find prints the bounding boxes (fractions) of text matches on that page, to help choose a clip."""
import sys, argparse, pymupdf
ap = argparse.ArgumentParser(); ap.add_argument('pdf'); ap.add_argument('page', type=int); ap.add_argument('out')
ap.add_argument('--clip', nargs=4, type=float); ap.add_argument('--dpi', type=int, default=170); ap.add_argument('--find')
a = ap.parse_args()
doc = pymupdf.open(a.pdf); pg = doc[a.page-1]; W, H = pg.rect.width, pg.rect.height
if a.find:
    for r in pg.search_for(a.find): print(f"match: x0={r.x0/W:.3f} y0={r.y0/H:.3f} x1={r.x1/W:.3f} y1={r.y1/H:.3f}")
clip = pymupdf.Rect(a.clip[0]*W, a.clip[1]*H, a.clip[2]*W, a.clip[3]*H) if a.clip else None
pix = pg.get_pixmap(dpi=a.dpi, clip=clip); pix.save(a.out); print(f"saved {a.out} ({pix.width}x{pix.height})")
