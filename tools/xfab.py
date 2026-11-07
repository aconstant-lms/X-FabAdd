#!/usr/bin/env python3
"""X-FabAdd slide/figure toolkit.

Figures live in  NN_chapter/figures/  (the source of truth).
Decks live in    NN_chapter/slides/*.pptx.
Each picture in a deck carries its repo path in its *alt text*
(e.g. "02_technologies/figures/02_lpbf_schematic.png"); that is the link.

Commands (run from anywhere; paths are resolved against the repo root):

  extract    DECK                pull embedded pictures out into figures/, set alt text
  sync       DECK... [--check]   refresh pictures from figures/, fill placeholders
  add-slide  DECK --title T --figure PATH [--notes N] [--caption C] [--after K]
  rename     OLD NEW             rename a figure, update every deck + index
  footer     DECK [--chapter "02 Technologies"] [--year 2027]
  status                         missing / unused figures across all decks

Every command (except --check) rewrites the chapter figures/index.csv files.
"""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import io
import re
import subprocess
import sys
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

REPO = Path(__file__).resolve().parent.parent
FIG_RE = re.compile(r"^(\d\d_[^/]+)/figures/[^/]+\.(png|jpe?g|gif|bmp|tiff?|emf|wmf)$", re.I)
INDEX_COLS = ["file", "slides", "caption", "source", "credit", "license", "notes"]
FOOTER_NAME = "XFabAdd footer"
FOOTER_TEMPLATE = "EXED Polytechnique - Additive Manufacturing - {chapter} by Andrei Constantinescu {year}"


# ---------------------------------------------------------------- helpers
def rel(p: Path) -> str:
    return p.resolve().relative_to(REPO).as_posix()


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def chapter_of(path: Path) -> str | None:
    parts = Path(rel(path)).parts
    return parts[0] if parts and re.match(r"^\d\d_", parts[0]) else None


def chapter_label(chapter: str) -> str:
    num, _, name = chapter.partition("_")
    name = name.replace("_", " ")
    return f"{num} {name[:1].upper()}{name[1:]}"


def all_decks() -> list[Path]:
    return sorted(p for p in REPO.glob("[0-9][0-9]_*/slides/*.pptx") if not p.name.startswith("~$"))


def iter_pictures(shapes):
    """Yield every picture shape, descending into groups."""
    for sh in shapes:
        if sh._element.tag == qn("p:grpSp"):
            yield from iter_pictures(sh.shapes)
        elif sh._element.tag == qn("p:pic"):
            yield sh


def get_alt(pic) -> str:
    return pic._element.nvPicPr.cNvPr.get("descr", "") or ""


def set_alt(pic, text: str) -> None:
    pic._element.nvPicPr.cNvPr.set("descr", text)


def image_size(data: bytes):
    try:
        from PIL import Image
        with Image.open(io.BytesIO(data)) as im:
            return im.size
    except Exception:
        return None


def fit_box(box, img_wh):
    """Contain img_wh inside box=(l,t,w,h), centred. Returns new box."""
    l, t, w, h = box
    if not img_wh or not w or not h:
        return box
    iw, ih = img_wh
    s = min(w / iw, h / ih)
    nw, nh = int(iw * s), int(ih * s)
    return (l + (w - nw) // 2, t + (h - nh) // 2, nw, nh)


def placeholder_png(label: str) -> bytes:
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGB", (1600, 900), (225, 225, 225))
    d = ImageDraw.Draw(im)
    d.rectangle([8, 8, 1591, 891], outline=(150, 150, 150), width=6)
    try:
        f1, f2 = ImageFont.load_default(size=72), ImageFont.load_default(size=36)
    except TypeError:
        f1 = f2 = ImageFont.load_default()
    d.text((800, 380), "FIGURE TO COME", fill=(110, 110, 110), font=f1, anchor="mm")
    d.text((800, 500), label, fill=(110, 110, 110), font=f2, anchor="mm")
    buf = io.BytesIO()
    im.save(buf, "PNG")
    return buf.getvalue()


def swap_image(slide, pic, image_file) -> None:
    """Point `pic` at a new image (path or file-like), keep frame, contain-fit, drop crop."""
    blip = pic._element.blipFill.find(qn("a:blip"))
    old = blip.get(qn("r:embed"))
    _, new = slide.part.get_or_add_image_part(image_file)
    blip.set(qn("r:embed"), new)
    src = pic._element.blipFill.find(qn("a:srcRect"))
    if src is not None:
        pic._element.blipFill.remove(src)
    if old and old != new:
        slide.part.drop_rel(old)


def slide_no(prs, slide) -> int:
    return list(prs.slides).index(slide) + 1


# ---------------------------------------------------------------- index.csv
def read_index(chapter: str) -> dict[str, dict]:
    f = REPO / chapter / "figures" / "index.csv"
    if not f.exists():
        return {}
    with f.open(newline="", encoding="utf-8") as fh:
        return {r["file"]: {c: r.get(c, "") or "" for c in INDEX_COLS} for r in csv.DictReader(fh)}


def write_index(chapter: str, rows: dict[str, dict]) -> None:
    f = REPO / chapter / "figures" / "index.csv"
    f.parent.mkdir(parents=True, exist_ok=True)
    with f.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, INDEX_COLS)
        w.writeheader()
        for k in sorted(rows):
            w.writerow(rows[k])


def scan_usage() -> dict[str, list[str]]:
    """repo path -> ["deck.pptx:3", ...] for every picture alt text in every deck."""
    use: dict[str, list[str]] = {}
    for deck in all_decks():
        prs = Presentation(deck)
        for i, s in enumerate(prs.slides, 1):
            for pic in iter_pictures(s.shapes):
                a = get_alt(pic)
                if FIG_RE.match(a):
                    use.setdefault(a, []).append(f"{deck.name}:{i}")
    return use


def refresh_indexes(captions: dict[str, str] | None = None) -> None:
    use = scan_usage()
    captions = captions or {}
    chapters = {p.parent.name for p in REPO.glob("[0-9][0-9]_*/figures")}
    for ch in sorted(chapters):
        rows = read_index(ch)
        figdir = REPO / ch / "figures"
        for f in figdir.iterdir():
            if f.is_file() and not f.name.startswith(".") and f.name != "index.csv":
                rows.setdefault(f.name, {c: "" for c in INDEX_COLS} | {"file": f.name})
        for key in list(use) + list(captions):
            if key.startswith(f"{ch}/figures/"):
                name = key.split("/")[-1]
                rows.setdefault(name, {c: "" for c in INDEX_COLS} | {"file": name})
        for name, row in rows.items():
            key = f"{ch}/figures/{name}"
            row["slides"] = "; ".join(sorted(set(use.get(key, []))))
            if captions.get(key) and not row["caption"]:
                row["caption"] = captions[key]
        write_index(ch, rows)


# ---------------------------------------------------------------- commands
def cmd_extract(a):
    deck = Path(a.deck).resolve()
    ch = a.chapter or chapter_of(deck)
    if not ch:
        sys.exit("Cannot tell the chapter; pass --chapter 02_technologies")
    figdir = REPO / ch / "figures"
    figdir.mkdir(parents=True, exist_ok=True)
    prefix = ch[:2]
    known = {sha1(f.read_bytes()): f for f in figdir.iterdir()
             if f.is_file() and f.name not in ("index.csv",) and not f.name.startswith(".")}
    prs = Presentation(deck)
    captions, n_new, n_linked = {}, 0, 0
    for i, s in enumerate(prs.slides, 1):
        k = 0
        for pic in iter_pictures(s.shapes):
            alt = get_alt(pic)
            if FIG_RE.match(alt) and (REPO / alt).exists():
                continue
            try:
                blob, ext = pic.image.blob, pic.image.ext.lower()
            except Exception:
                print(f"  slide {i}: picture without embedded image, skipped")
                continue
            ext = "jpg" if ext == "jpeg" else ext
            h = sha1(blob)
            if h in known:
                target = known[h]
                n_linked += 1
            else:
                k += 1
                target = figdir / f"{prefix}_s{i:02d}_{k:02d}.{ext}"
                while target.exists():
                    k += 1
                    target = figdir / f"{prefix}_s{i:02d}_{k:02d}.{ext}"
                target.write_bytes(blob)
                known[h] = target
                n_new += 1
            path = rel(target)
            if alt and not FIG_RE.match(alt) and not re.fullmatch(r"[^\s/]+\.\w{3,4}", alt.strip()):
                captions.setdefault(path, alt.strip())
            set_alt(pic, path)
    prs.save(deck)
    refresh_indexes(captions)
    print(f"{deck.name}: {n_new} new figure(s) in {ch}/figures, {n_linked} re-used")


def cmd_sync(a):
    total_missing = 0
    for d in a.decks:
        deck = Path(d).resolve()
        prs = Presentation(deck)
        changed, missing = [], []
        for i, s in enumerate(prs.slides, 1):
            for pic in iter_pictures(s.shapes):
                alt = get_alt(pic)
                if not FIG_RE.match(alt):
                    continue
                f = REPO / alt
                if not f.exists():
                    missing.append(f"slide {i}: {alt}")
                    continue
                data = f.read_bytes()
                try:
                    same = sha1(pic.image.blob) == sha1(data)
                except Exception:
                    same = False
                if same:
                    continue
                changed.append(f"slide {i}: {alt}")
                if a.check:
                    continue
                box = (pic.left, pic.top, pic.width, pic.height)
                swap_image(s, pic, str(f))
                if not a.stretch:
                    l, t, w, h = fit_box(box, image_size(data))
                    pic.left, pic.top, pic.width, pic.height = Emu(l), Emu(t), Emu(w), Emu(h)
        if changed and not a.check:
            prs.save(deck)
        verb = "to update" if a.check else "updated"
        print(f"{deck.name}: {len(changed)} {verb}, {len(missing)} missing")
        for c in changed:
            print(f"   ~ {c}")
        for m in missing:
            print(f"   ? {m}")
        total_missing += len(missing)
    if not a.check:
        refresh_indexes()
    if a.check and total_missing:
        sys.exit(1)


def _title_bottom(slide, prs):
    t = slide.shapes.title
    if t is not None and t.top is not None:
        return t.top + t.height
    return int(prs.slide_height * 0.18)


def _copy_footer(prs, new_slide):
    for s in prs.slides:
        if s is new_slide:
            continue
        for sh in s.shapes:
            if sh.name == FOOTER_NAME:
                new_slide.shapes._spTree.append(copy.deepcopy(sh._element))
                return True
    return False


def _move_slide(prs, slide, position):
    lst = prs.slides._sldIdLst
    ids = list(lst)
    el = ids[[i for i, s in enumerate(prs.slides) if s is slide][0]]
    lst.remove(el)
    lst.insert(position, el)


def cmd_add_slide(a):
    deck = Path(a.deck).resolve()
    prs = Presentation(deck)
    fig = a.figure.replace("\\", "/")
    if not FIG_RE.match(fig):
        sys.exit(f"--figure must look like NN_chapter/figures/name.png, got {fig!r}")
    layout = None
    if a.layout:
        layout = next((l for l in prs.slide_layouts if l.name.lower() == a.layout.lower()), None)
        if layout is None:
            sys.exit("Layouts in this deck: " + ", ".join(l.name for l in prs.slide_layouts))
    elif a.like:
        layout = prs.slides[a.like - 1].slide_layout
    else:
        layout = next((l for l in prs.slide_layouts if l.name.lower() == "title only"), None) \
            or (prs.slides[-1].slide_layout if len(prs.slides) else prs.slide_layouts[0])
    s = prs.slides.add_slide(layout)
    if s.shapes.title is not None:
        s.shapes.title.text = a.title
    # remove empty non-title placeholders, remember a picture placeholder's box
    pic_box = None
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 0:
            continue
        if ph.placeholder_format.type is not None and "PICTURE" in str(ph.placeholder_format.type):
            pic_box = (ph.left, ph.top, ph.width, ph.height)
        if "FOOTER" in str(ph.placeholder_format.type) or "SLIDE_NUMBER" in str(ph.placeholder_format.type):
            continue
        ph._element.getparent().remove(ph._element)
    W, H = prs.slide_width, prs.slide_height
    if pic_box is None:
        top = _title_bottom(s, prs) + int(H * 0.03)
        bottom = int(H * (0.82 if a.caption else 0.88))
        pic_box = (int(W * 0.06), top, int(W * 0.88), bottom - top)
    f = REPO / fig
    if f.exists():
        data = f.read_bytes()
        src = str(f)
    else:
        data = placeholder_png(fig)
        src = io.BytesIO(data)
        print(f"  {fig} not found yet: placeholder inserted (run `sync` once it exists)")
    l, t, w, h = fit_box(pic_box, image_size(data))
    pic = s.shapes.add_picture(src, Emu(l), Emu(t), Emu(w), Emu(h))
    set_alt(pic, fig)
    pic.name = Path(fig).stem
    if a.caption:
        tb = s.shapes.add_textbox(Emu(int(W * 0.06)), Emu(int(H * 0.83)), Emu(int(W * 0.88)), Emu(int(H * 0.05)))
        p = tb.text_frame.paragraphs[0]
        p.text = a.caption
        p.font.size = Pt(12)
        p.font.italic = True
    if a.notes:
        s.notes_slide.notes_text_frame.text = a.notes
    _copy_footer(prs, s)
    if a.after is not None:
        _move_slide(prs, s, a.after)
    prs.save(deck)
    refresh_indexes({fig: a.caption} if a.caption else None)
    print(f"{deck.name}: slide added at position {slide_no(prs, s)} with {fig}")


def cmd_rename(a):
    old, new = a.old.replace("\\", "/"), a.new.replace("\\", "/")
    if "/" not in new:
        new = str(Path(old).parent / new).replace("\\", "/")
    if not FIG_RE.match(old) or not FIG_RE.match(new):
        sys.exit("Both paths must look like NN_chapter/figures/name.ext")
    src, dst = REPO / old, REPO / new
    if dst.exists():
        sys.exit(f"{new} already exists")
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        r = subprocess.run(["git", "-C", str(REPO), "mv", old, new], capture_output=True)
        if r.returncode:
            src.rename(dst)
    n = 0
    for deck in all_decks():
        prs = Presentation(deck)
        hit = False
        for s in prs.slides:
            for pic in iter_pictures(s.shapes):
                if get_alt(pic) == old:
                    set_alt(pic, new)
                    hit = True
                    n += 1
        if hit:
            prs.save(deck)
    # carry the index row over
    oc, nc = old.split("/")[0], new.split("/")[0]
    orow = read_index(oc)
    row = orow.pop(Path(old).name, None)
    write_index(oc, orow)
    if row:
        nrow = read_index(nc)
        nrow[Path(new).name] = row | {"file": Path(new).name}
        write_index(nc, nrow)
    refresh_indexes()
    print(f"{old} -> {new}: {n} picture(s) relinked")


def cmd_footer(a):
    deck = Path(a.deck).resolve()
    ch = chapter_of(deck)
    label = a.chapter or (chapter_label(ch) if ch else None)
    if not label:
        sys.exit('Pass --chapter "02 Technologies"')
    text = (a.template or FOOTER_TEMPLATE).format(chapter=label, year=a.year)
    prs = Presentation(deck)
    W, H = prs.slide_width, prs.slide_height
    for i, s in enumerate(prs.slides, 1):
        if a.skip_first and i == 1:
            continue
        sh = next((x for x in s.shapes if x.name == FOOTER_NAME), None)
        if sh is None:
            sh = s.shapes.add_textbox(Emu(int(W * 0.02)), Emu(H - Emu(Pt(a.size * 2.6))),
                                      Emu(int(W * 0.7)), Emu(Pt(a.size * 2)))
            sh.name = FOOTER_NAME
        tf = sh.text_frame
        tf.clear()
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(a.size)
        p.font.color.rgb = RGBColor.from_string(a.color)
    prs.save(deck)
    print(f'{deck.name}: footer "{text}" on {len(prs.slides) - (1 if a.skip_first else 0)} slide(s)')


def cmd_status(a):
    use = scan_usage()
    files = {rel(f) for f in REPO.glob("[0-9][0-9]_*/figures/*")
             if f.is_file() and f.name != "index.csv" and not f.name.startswith(".")}
    missing = sorted(k for k in use if k not in files)
    unused = sorted(f for f in files if f not in use)
    print(f"{len(all_decks())} deck(s), {len(files)} figure file(s), {len(use)} linked")
    for m in missing:
        print(f"  missing: {m}   ({', '.join(use[m])})")
    for u in unused:
        print(f"  unused:  {u}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("extract", help="move embedded pictures into figures/ and link them")
    p.add_argument("deck")
    p.add_argument("--chapter", help="e.g. 02_technologies (default: from the deck's folder)")
    p.set_defaults(fn=cmd_extract)

    p = sub.add_parser("sync", help="refresh deck pictures from figures/")
    p.add_argument("decks", nargs="+")
    p.add_argument("--check", action="store_true", help="report only, change nothing (exit 1 if missing)")
    p.add_argument("--stretch", action="store_true", help="fill the old frame instead of keeping proportions")
    p.set_defaults(fn=cmd_sync)

    p = sub.add_parser("add-slide", help="append a slide with a figure")
    p.add_argument("deck")
    p.add_argument("--title", required=True)
    p.add_argument("--figure", required=True, help="NN_chapter/figures/name.png (may not exist yet)")
    p.add_argument("--notes", help="speaker notes")
    p.add_argument("--caption", help="small caption under the figure (also stored in index.csv)")
    p.add_argument("--layout", help="layout name in the deck (default: 'Title Only')")
    p.add_argument("--like", type=int, help="use the layout of slide K")
    p.add_argument("--after", type=int, help="insert after slide K (0 = first)")
    p.set_defaults(fn=cmd_add_slide)

    p = sub.add_parser("rename", help="rename a figure and relink every deck")
    p.add_argument("old")
    p.add_argument("new", help="new path, or just a new file name")
    p.set_defaults(fn=cmd_rename)

    p = sub.add_parser("footer", help="put the EXED footer on every slide")
    p.add_argument("deck")
    p.add_argument("--chapter", help='label, e.g. "02 Technologies" (default: from folder)')
    p.add_argument("--year", default="2027")
    p.add_argument("--template", help="default: " + FOOTER_TEMPLATE)
    p.add_argument("--size", type=float, default=8, help="font size in pt (default 8)")
    p.add_argument("--color", default="7F7F7F")
    p.add_argument("--skip-first", action="store_true", help="leave the title slide alone")
    p.set_defaults(fn=cmd_footer)

    p = sub.add_parser("status", help="missing and unused figures")
    p.set_defaults(fn=cmd_status)

    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
