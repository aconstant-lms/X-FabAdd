"""Build the two chapter-02 decks that replace "AM technologies" (Nov 2026):

  technology_metal    the metal session: processes, prices, five physical laws for metals
  technology_polymer  the polymer session: processes, six physical laws, maturity index,
                      the exercise "Polymer AM 2022 -> 2026" and its debrief
  technology_unused   everything set aside for now: traditional technologies, metals,
                      other AM processes, parked slides

It runs gen_am_technologies.py (the old one-deck generator, kept as the source of the existing
slides), adds the new slides from slides_polymer_new.py, then writes one claude.ai Slides project
per deck under build/<deck>/project.

  python gen_technology_decks.py build [--k02 PATH]     # slides + manifest of pictures to upload
  python gen_technology_decks.py relink uploaded.json    # put the uploaded /_blob/ ids in the slides

Pictures: an artifact's /_blob/ ids belong to that artifact, so each deck gets its own upload.
build/manifest.json lists, per deck, the local file of every picture the slides use.
uploaded.json maps {deck: {local file: "/_blob/<id>"}} after the upload.
"""
import json, re, sys, glob, shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FIG = REPO / "02_technologies" / "figures"
BUILD = HERE / "build"

POLY = """cover-polymer
d14ebe40 shape-process groups-paths part-2 photopoly vpp-example-carbon mjt mex shl pbf injection
vpp-prices-intro poly-pyramid poly-ashby poly-prices poly-makers
part-3 addressing box part-4 clocks part-5 interfaces
part-laws law-light law-threshold law-viscosity law-jetting law-sintering law-yield law-rate law-questions potentials
part-maturity poly-landscape mi-def mi-levels mi-rubric-tech mi-rubric-ind mi-2022
part-exercise ex-mission ex-groups ex-timeline ex-canvas ex-bets ex-research ex-wall ex-duel
part-debrief poly-readiness poly-status-2026 vpp-volumetric vpp-volumetric-two vpp-prices vpp-makers poly-market
db-patterns db-takeuchi db-transfer
part-refs references references-web references-new references-physics""".split()
POLY_SECTIONS = {"s0": ("Cover", "cover-polymer"), "s2": ("Part 2: AM processes for polymers", "d14ebe40"),
                 "s3": ("Part 3: A morphological box", "part-3"), "s4": ("Part 4: Clocks", "part-4"),
                 "s5": ("Part 5: The layer interface", "part-5"), "s6": ("Part 6: Six physical laws", "part-laws"),
                 "s7": ("Part 7: Maturity", "part-maturity"), "s8": ("Part 8: Exercise", "part-exercise"),
                 "s9": ("Part 9: Debrief, 2022 to 2026", "part-debrief"), "s10": ("Part 10: References", "part-refs")}
UNUSED = """cover-unused
part-1 materials groups convention case-1 case-2 case-3 case-4 case-5 case-6 heat-scales hip
part-other paste micro lcvd ecam vpp-example-template
part-8 ashby-tree pm geometry twins vpp part-6 part-7""".split()
UNUSED_SECTIONS = {"s0": ("Cover", "cover-unused"), "s1": ("Part 1: Traditional technologies", "part-1"),
                   "s3": ("Other AM processes", "part-other"),
                   "s4": ("Parked slides", "part-8")}
METAL = """cover-metal
part-2-metals shape-process groups-paths metal-processes pbf ded cold bjt pm lpbf-prices bj-machines
part-3 addressing box part-4 clocks part-5 interfaces
part-mlaws mlaw-melt mlaw-stress mlaw-fatigue mlaw-post mlaw-rate mlaw-questions potentials
part-mrefs references-metals references-mphysics""".split()
METAL_SECTIONS = {"s0": ("Cover", "cover-metal"), "s2": ("Part 2: AM processes for metals", "part-2-metals"),
                  "s3": ("Part 3: A morphological box", "part-3"), "s4": ("Part 4: Clocks", "part-4"),
                  "s5": ("Part 5: The layer interface", "part-5"), "s6": ("Part 6: Five physical laws for metals", "part-mlaws"),
                  "s7": ("Part 7: References", "part-mrefs")}
DECKS = {"technology_polymer": ("AM technologies: polymers", POLY, POLY_SECTIONS, "cover-polymer"),
         "technology_metal": ("AM technologies: metals", METAL, METAL_SECTIONS, "cover-metal"),
         "technology_unused": ("AM technologies: slides set aside", UNUSED, UNUSED_SECTIONS, "cover-unused")}


def run_generators(k02):
    all_dir = BUILD / "all" / "project"
    (all_dir / "slides").mkdir(parents=True, exist_ok=True)
    src = (HERE / "gen_am_technologies.py").read_text()
    src = src.replace("R=Path('/home/claude/deck02/project')", f"R=Path({str(all_dir)!r})")
    src = src.replace("/home/claude/deck02/raw/", str(HERE / "raw") + "/")
    ns = {"__name__": "gen_old"}
    exec(compile(src, "gen_am_technologies.py", "exec"), ns)
    ns["K02"] = k02
    # slides that exist only in the live deck (no generator code), kept verbatim in raw/
    for f in ("twins.html",):
        (all_dir / "slides" / f).write_text((HERE / "raw" / f).read_text())
    exec(compile((HERE / "slides_polymer_new.py").read_text(), "slides_polymer_new.py", "exec"), ns)
    exec(compile((HERE / "slides_metal_new.py").read_text(), "slides_metal_new.py", "exec"), ns)
    return ns, all_dir


def file_for(key, ns):
    P = ns["P"]
    if key in P:
        return FIG / f"{P[key]}.png"
    if key == "carbon":
        return FIG / "02_h04_carbon_clip_animation.gif"
    if key == "k02":
        return Path(ns["K02"])
    hits = glob.glob(str(FIG / f"02_{key}_*.gif"))
    if hits:
        return Path(hits[0])
    raise KeyError(key)


def build(k02):
    ns, all_dir = run_generators(k02)
    rev = {}
    for k, v in ns["A"].items():
        rev.setdefault(v, k)
    old = json.loads((all_dir / "deck.json").read_text())
    manifest = {}
    for deck, (title, order, secs, cover) in DECKS.items():
        out = BUILD / deck / "project"
        if out.exists():
            shutil.rmtree(out)
        (out / "slides").mkdir(parents=True)
        pics = {}
        for sid in order:
            html = (all_dir / "slides" / f"{sid}.html").read_text()
            for ref in re.findall(r"/_blob/([A-Za-z0-9_-]+)", html):
                pics[ref] = str(file_for(rev[ref], ns))
            (out / "slides" / f"{sid}.html").write_text(html)
        d = {k: old[k] for k in ("v", "createdOnFiles", "lists", "faces", "designSystems", "attachments")}
        d.update(title=title, order=order, cover=cover,
                 sections={k: {"description": t, "start": s} for k, (t, s) in secs.items()})
        (out / "deck.json").write_text(json.dumps(d, indent=1, ensure_ascii=False))
        manifest[deck] = pics
        print(deck, len(order), "slides,", len(set(pics.values())), "pictures")
    (BUILD / "manifest.json").write_text(json.dumps(manifest, indent=1))
    for f in sorted((all_dir / "slides").glob("*.html")):
        t = f.read_text(); n = len(re.findall(r"<(?!/)[a-zA-Z]", t))
        if n > 190 or ("EXED" not in t and not f.stem.startswith("cover")):
            print("CHECK", f.stem, n)


def relink(uploaded):
    up = json.loads(Path(uploaded).read_text())
    man = json.loads((BUILD / "manifest.json").read_text())
    for deck, pics in man.items():
        out = BUILD / deck / "project" / "slides"
        for f in out.glob("*.html"):
            t = f.read_text()
            for ref, path in pics.items():
                t = t.replace(f"/_blob/{ref}\"", f"{up[deck][path]}\"")
            f.write_text(t)
            left = re.findall(r"/_blob/NEW-[A-Za-z0-9_]+", t)
            if left:
                print("UNLINKED", deck, f.stem, left)
        print("relinked", deck)


if __name__ == "__main__":
    if sys.argv[1] == "build":
        k02 = sys.argv[sys.argv.index("--k02") + 1] if "--k02" in sys.argv else str(FIG / "02_k02_ampower_polymer_landscape.jpg")
        build(k02)
    else:
        relink(sys.argv[2])
