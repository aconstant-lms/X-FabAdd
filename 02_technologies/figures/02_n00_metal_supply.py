"""02_n00 - Metal AM supply chain figures for the technology_metal deck (Nov 2026).

  02_n01_metal_price_vs_volume   machine price vs build volume, colour = region of the maker (Ashby style)
  02_n02_map_world_numbered      metal machine makers outside Europe (numbered rings, colour = process)
  02_n02_map_europe_labels       metal machine makers in Europe (labelled)
  02_n03_powder_prices           powder price ranges per alloy against the bulk metal price
  02_n04_map_world_numbered      powder makers outside Europe (colour = powder route)
  02_n04_map_europe_labels       powder makers in Europe
  02_n05_powder_co2              CO2 footprint, virgin vs recycled feedstock (Davies, Sandvik 2023)
  02_n06_metal_market            AMPOWER metal AM market 2016-2028 and metal PBF units sold
  02_n07_powder_routes           four atomisation routes, schematic (no scale)

Data: ../tables/02_machines_metal_makers.csv, 02_metal_powder_prices.csv, 02_powder_makers.csv,
02_powder_co2.csv, 02_metal_market_ampower.csv.  Usage: python 02_n00_metal_supply.py
"""
import csv
import warnings
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import FancyBboxPatch, Polygon, Circle, Rectangle
from matplotlib.ticker import FuncFormatter
from _printers_common import HERE, INK, GREY, GRID, use_font, usd

warnings.filterwarnings("ignore")
use_font("Inter", 14)
matplotlib.rcParams["svg.fonttype"] = "none"
TAB = HERE.parent / "tables"
rd = lambda f: list(csv.DictReader(open(TAB / f, encoding="utf-8")))
REGION = {"Europe": "#2f5f9e", "USA": "#c4561a", "China": "#1f7a5c", "Asia": "#7b52c7", "Asia-Pacific": "#7b52c7",
          "North America": "#c4561a"}
PROC = {"LPBF": "#2a78d6", "EBM": "#7b52c7", "DED powder (laser)": "#eda100", "DED wire (laser)": "#eda100",
        "DED wire (arc)": "#eb6834", "DED wire (plasma)": "#eb6834", "DED wire (e-beam)": "#eb6834",
        "binder jetting": "#1baf7a", "bound metal extrusion": "#1baf7a", "cold spray": "#a0522d"}
PROC_KEY = {"laser PBF": "#2a78d6", "electron-beam PBF": "#7b52c7", "DED, laser": "#eda100",
            "DED, wire arc / plasma / e-beam": "#eb6834", "binder jetting, extrusion + sintering": "#1baf7a", "cold spray": "#a0522d"}
ROUTE = {"gas": "#2a78d6", "plasma": "#7b52c7", "water": "#566170", "recycling": "#1baf7a", "ultrasonic": "#eda100"}


def route(p):
    p = p.lower()
    if "scrap" in p or "recycl" in p:
        return "recycling"
    if "ultrason" in p:
        return "ultrasonic"
    if "plasma" in p and "gas" not in p:
        return "plasma"
    if p.startswith("water"):
        return "water"
    return "gas"


def save(fig, name, exts=("png", "pdf"), **kw):
    for x in exts:
        fig.savefig(HERE / f"{name}.{x}", dpi=200, **kw)
    plt.close(fig)


# ------------------------------------------------------------------ n01 price vs build volume
M = rd("02_machines_metal_makers.csv")


def vol_l(r):
    x, y, z = float(r["build_x_mm"]), float(r["build_y_mm"]), float(r["build_z_mm"])
    return (np.pi / 4 * x * y if r["round"] == "yes" else x * y) * z / 1e6


fig = plt.figure(figsize=(13, 8.6))
ax = fig.add_axes([0.085, 0.08, 0.62, 0.62]); axq = fig.add_axes([0.085, 0.72, 0.62, 0.26], sharex=ax)
ax.set_xscale("log"); ax.set_yscale("log"); XL, YL = (0.25, 8000), (3e4, 6e6)
ax.set_xlim(*XL); ax.set_ylim(*YL); ax.grid(True, which="major", color=GRID, lw=0.8); ax.set_axisbelow(True)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.set_xlabel("Build volume  (litres, log scale)"); ax.set_ylabel("Machine price  (USD, log scale)")
ax.yaxis.set_major_formatter(FuncFormatter(usd))
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
xs = np.logspace(np.log10(XL[0]), np.log10(XL[1]), 50)
GUIDES = [(2e5, 3.0), (2e4, 4.0), (2e3, 1800)]
for k, _x in GUIDES:
    ax.plot(xs, k * xs, ls=(0, (5, 4)), color="#b9b4a8", lw=1, zorder=0)
fig.canvas.draw()
for k, lx in GUIDES:
    a = ax.transData.transform([(lx, k * lx), (lx * 10, k * lx * 10)])
    ang = np.degrees(np.arctan2(a[1, 1] - a[0, 1], a[1, 0] - a[0, 0]))
    ax.annotate(f"{usd(k)} per litre", (lx, k * lx), xytext=(-4, 5), textcoords="offset points", rotation=ang,
                rotation_mode="anchor", color="#8f8a7e", fontsize=11, style="italic")
OFF = {"EOS M 100": (-9, 8, "right"), "TRUMPF TruPrint 1000": (9, -14), "EOS M 290": (-9, 4, "right"),
       "Nikon SLM Solutions SLM 125": (9, 4), "3D Systems DMP Flex 200": (-9, 14, "right"),
       "Farsoon Technologies FS121M": (9, -4), "Farsoon Technologies FS301M": (0, -20, "center"),
       "Colibrium Additive (GE Aerospace) M2 Series 5": (-9, 10, "right"), "Renishaw RenAM 500Q": (9, -6),
       "Nikon SLM Solutions SLM 280 2.0": (9, 4), "Nikon SLM Solutions SLM 500": (9, 0),
       "TRUMPF TruPrint 5000": (-9, 2, "right"), "EOS M 400-4": (9, 6), "ZRapid Tech iSLM420D": (9, -8),
       "Nikon SLM Solutions NXG XII 600": (-9, 8, "right"), "BLT (Bright Laser Technologies) BLT-S600": (0, -20, "center"),
       "BLT (Bright Laser Technologies) BLT-S800": (9, 2), "Velo3D Sapphire XC 1MZ": (9, 10),
       "Tianhong Laser TH-M800 (LM-M800)": (9, -6), "Markforged (Nano Dimension) PX100": (-9, 0, "right"),
       "Desktop Metal Studio System 2": (9, 0)}
SHORT = {"Colibrium Additive (GE Aerospace)": "Colibrium", "Nikon SLM Solutions": "Nikon SLM", "BLT (Bright Laser Technologies)": "BLT",
         "Farsoon Technologies": "Farsoon", "Markforged (Nano Dimension)": "Markforged", "Tianhong Laser": "Tianhong"}
LBL = {"SLM 280 2.0": "SLM 280", "RenAM 500Q": "500Q", "TH-M800 (LM-M800)": "TH-M800", "Sapphire XC 1MZ": "Sapphire XC 1MZ"}
for r in M:
    if r["plotted"] != "yes":
        continue
    v, lo, hi = vol_l(r), float(r["price_low_usd"]), float(r["price_high_usd"]); c = REGION[r["region"]]
    mk = "o" if r["technology"] == "LPBF" else "s"
    ax.plot([v, v], [lo, hi], color=c, lw=3, alpha=0.55, solid_capstyle="round")
    ax.scatter([v], [np.sqrt(lo * hi)], s=70, marker=mk, color=c, edgecolor="white", lw=1, zorder=4)
    key = f'{r["maker"]} {r["model"]}'; o = OFF.get(key, (9, 0)); ha = o[2] if len(o) > 2 else "left"
    nm = SHORT.get(r["maker"], r["maker"].split(" (")[0]); md = LBL.get(r["model"], r["model"])
    lab = md if md.startswith(("SLM", "BLT", "NXG")) and nm in ("Nikon SLM", "BLT") else f"{nm} {md}"
    lab = ("Nikon " + lab) if nm == "Nikon SLM" and not lab.startswith("Nikon") else lab
    ax.annotate(lab, (v, np.sqrt(lo * hi)),
                xytext=o[:2], textcoords="offset points", ha=ha, va="center", fontsize=11, color=INK,
                path_effects=[pe.withStroke(linewidth=3, foreground="white")])
# quotes strip
axq.set_yscale("linear"); axq.set_ylim(0, 1); axq.axis("off")
axq.text(XL[0] * 1.05, 0.9, "Price on request (build volume only)", fontsize=12, color=GREY, va="top")
q = sorted([r for r in M if r["plotted"] == "quote" and r["technology"] == "LPBF"], key=vol_l)
for j, r in enumerate(q):
    QROW = {"FormUp 350": (0, 0), "M 8K": (0, 0), "DMP Factory 500": (1, 0), "FS1521M": (1, 1), "HBD 1000Pro": (2, 0),
            "EP-M2050": (2, 1), "BLT-S1500": (3, 1)}
    v = vol_l(r); rgt = v > 1500; y = 0.06 + 0.125 * j
    axq.scatter([v], [y], s=60, color=REGION[r["region"]], zorder=4)
    axq.annotate(f'{SHORT.get(r["maker"], r["maker"].split(" (")[0]).split(" ")[0]} {r["model"].replace("HBD ", "")}', (v, y), xytext=(-6 if rgt else 6, 0), textcoords="offset points",
                 fontsize=10.5, va="center", ha="right" if rgt else "left", color=INK)
# legend panel
lg = fig.add_axes([0.74, 0.08, 0.25, 0.62]); lg.axis("off"); lg.set_xlim(0, 1); lg.set_ylim(0, 1); lg.set_autoscale_on(False)
yy = 0.97
lg.text(0, yy, "Maker's home region", fontsize=14, fontweight="bold", color=INK, va="top"); yy -= 0.06
for t, c in [("Europe", REGION["Europe"]), ("USA", REGION["USA"]), ("China", REGION["China"])]:
    lg.scatter([0.03], [yy - 0.012], s=80, color=c); lg.text(0.08, yy, t, fontsize=13, va="top", color=INK); yy -= 0.05
yy -= 0.02
lg.text(0, yy, "● laser PBF   ■ binder jetting / extrusion", fontsize=12, va="top", color=GREY); yy -= 0.07
for t in ["Bar: published price range;", "marker: geometric mean.", "", "Ranges are indicative estimates", "(aggregators, resellers, listings):",
          "makers quote on request.", "", "Chinese large formats (BLT,", "Farsoon, Eplus3D, HBD) reach", "1–4.6 m³ at prices not published.",
          "", "Dashed lines: constant price", "per litre of build volume."]:
    lg.text(0, yy, t, fontsize=12, va="top", color=GREY); yy -= 0.052
save(fig, "02_n01_metal_price_vs_volume")

# ------------------------------------------------------------------ maps (n02 machines, n04 powders)
import geopandas as gpd
SEA, LAND, COAST, HALO, FILL = "#dfe6ee", "#cbc4b4", "#b3ab98", "#eef2f6", "#fbfaf7"
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres")); world = world[world["continent"] != "Antarctica"]
EBOX = (-11, 24, 37, 62)


def world_map(name, pts):
    """pts: (n, colour, lon, lat, (dx, dy))"""
    fig = plt.figure(figsize=(10.4, 3.9)); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(SEA); world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.5)
    ax.set_xlim(-140, 162); ax.set_ylim(-42, 66); ax.set_aspect("auto"); ax.axis("off")
    x0, x1, y0, y1 = EBOX
    ax.plot([x0, x1, x1, x0, x0], [y0, y0, y1, y1, y0], ls=(0, (4, 3)), color="#6b7480", lw=1, zorder=4)
    for n, c, lon, lat, (dx, dy) in pts:
        x, y = lon + dx, lat + dy
        if (dx, dy) != (0, 0):
            ax.plot([lon, x], [lat, y], color=INK, lw=1.2, zorder=4); ax.scatter([lon], [lat], s=16, color=INK, zorder=4)
        ax.scatter([x], [y], s=400, facecolor=FILL, edgecolor=c, linewidth=2.2, zorder=5)
        ax.text(x, y - 0.4, str(n), ha="center", va="center", fontsize=11.5, fontweight="bold", color=c, zorder=6)
    for ext in ("png", "svg"):
        fig.savefig(HERE / f"{name}.{ext}", dpi=200, facecolor=SEA)
    plt.close(fig)


def europe_map(name, pts):
    """pts: (label, colour, lon, lat, (ox, oy), ha)"""
    fig = plt.figure(figsize=(6.0, 7.05)); ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(SEA); world.plot(ax=ax, color=LAND, edgecolor=COAST, linewidth=0.6)
    asp = 1 / np.cos(np.radians(50)); lon0, lon1 = -10.0, 24.0; h = (lon1 - lon0) / asp * 7.05 / 6.0
    ax.set_xlim(lon0, lon1); ax.set_ylim(49.6 - h / 2, 49.6 + h / 2); ax.set_aspect(asp); ax.axis("off")
    for lab, c, lon, lat, (ox, oy), ha in pts:
        ax.scatter([lon], [lat], s=110, facecolor=FILL, edgecolor=c, linewidth=2.2, zorder=5)
        ax.annotate(lab, (lon, lat), xytext=(ox, oy), textcoords="offset points", ha=ha, va="center", fontsize=12,
                    fontweight="semibold", color=INK, zorder=6, path_effects=[pe.withStroke(linewidth=3.4, foreground=HALO)],
                    arrowprops=dict(arrowstyle="-", color=INK, lw=0.8, shrinkA=0, shrinkB=4) if abs(ox) + abs(oy) > 22 else None)
    for ext in ("png", "svg"):
        fig.savefig(HERE / f"{name}.{ext}", dpi=200, facecolor=SEA)
    plt.close(fig)


# machine makers: one ring per maker (first technology listed), outside Europe numbered
WM = [(1, PROC["LPBF"], -121.99, 37.55, (-6, -4)),      # Velo3D
      (2, PROC["binder jetting"], -122.14, 37.44, (-8, 6)),  # HP
      (3, PROC["DED powder (laser)"], -106.65, 35.08, (0, -9)),  # Optomec
      (4, PROC["DED wire (e-beam)"], -87.74, 41.75, (-3, 8)),   # Sciaky
      (5, PROC["binder jetting"], -79.73, 40.33, (4, 9)),   # ExOne / Arc Impact
      (6, PROC["binder jetting"], -71.24, 42.38, (10, 4)),  # Markforged
      (7, PROC["LPBF"], -81.03, 34.92, (4, -9)),           # 3D Systems
      (8, PROC["LPBF"], 108.94, 34.34, (-8, 8)),           # BLT
      (9, PROC["LPBF"], 112.94, 28.23, (-6, -9)),          # Farsoon
      (10, PROC["LPBF"], 120.16, 30.27, (4, -10)),         # Eplus3D
      (11, PROC["LPBF"], 121.47, 31.23, (11, -3)),         # HBD
      (12, PROC["LPBF"], 120.58, 31.30, (7, 6)),           # ZRapid, Tianhong (Suzhou)
      (13, PROC["EBM"], 139.77, 35.68, (8, 6)),            # JEOL
      (14, PROC["cold spray"], 144.96, -37.81, (0, 0))]    # SPEE3D, Titomic
world_map("02_n02_map_world_numbered", WM)
EM = [("EOS, AMCM", PROC["LPBF"], 11.40, 48.10, (16, -14), "left"),
      ("Nikon SLM", PROC["LPBF"], 10.69, 53.87, (14, 6), "left"),
      ("TRUMPF", PROC["LPBF"], 9.07, 48.83, (-14, -12), "right"),
      ("Colibrium", PROC["LPBF"], 11.06, 50.15, (14, 2), "left"),
      ("Renishaw", PROC["LPBF"], -2.35, 51.64, (-14, -8), "right"),
      ("WAAM3D", PROC["DED wire (arc)"], -0.76, 52.04, (-14, 14), "right"),
      ("AddUp", PROC["LPBF"], 3.10, 45.83, (-14, 0), "right"),
      ("Arcam, Freemelt", PROC["EBM"], 12.01, 57.66, (14, 0), "left"),
      ("DMG MORI", PROC["DED powder (laser)"], 8.53, 52.02, (12, -12), "left"),
      ("Gefertec", PROC["DED wire (arc)"], 13.40, 52.52, (14, 0), "left"),
      ("MX3D", PROC["DED wire (arc)"], 4.90, 52.37, (-10, 18), "right"),
      ("Norsk Titanium", PROC["DED wire (plasma)"], 10.26, 60.17, (14, 0), "left"),
      ("Meltio", PROC["DED wire (laser)"], -3.64, 38.09, (14, 6), "left"),
      ("Prima Additive", PROC["DED powder (laser)"], 7.69, 45.07, (14, -6), "left"),
      ("ExOne GmbH", PROC["binder jetting"], 10.86, 48.43, (-30, -26), "right")]
europe_map("02_n02_map_europe_labels", EM)

# powder makers
PM = rd("02_powder_makers.csv")
col = {r["maker"]: ROUTE[route(r["process"])] for r in PM}
WP = [(1, col["Carpenter Additive"], -75.93, 40.34, (6, -8)), (2, col["6K Additive"], -80.39, 40.38, (-6, -9)),
      (3, col["Continuum Powders"], -95.37, 29.76, (0, 0)), (4, col["Colibrium Additive (AP&C)"], -73.84, 45.61, (-6, 9)),
      (5, col["Tekna"], -71.89, 45.40, (8, 6)), (6, col["Equispheres"], -75.70, 45.42, (-14, 4)),
      (7, col["BLT powders"], 108.94, 34.34, (0, 0)), (8, col["AVIMETAL Powder"], 116.40, 39.90, (0, 0)),
      (9, col["Sanyo Special Steel"], 134.69, 34.82, (2, -9)), (10, col["Daido Steel"], 136.91, 35.18, (9, 4))]
world_map("02_n04_map_world_numbered", WP)
EP = [("Sandvik Osprey", col["Sandvik Osprey"], -3.80, 51.66, (10, -20), "left"),
      ("Höganäs", col["Höganäs"], 12.56, 56.20, (14, 0), "left"),
      ("Oerlikon AM", col["Oerlikon AM"], 11.58, 52.20, (14, -4), "left"),
      ("Heraeus", col["Heraeus AMLOY"], 8.92, 50.13, (12, -4), "left"),
      ("Linde AMT", col["Linde AMT"], 11.52, 48.06, (-14, -10), "right"),
      ("m4p", col["m4p material solutions"], 14.17, 46.52, (14, 0), "left"),
      ("Aubert & Duval", col["Aubert & Duval"], 2.81, 45.92, (-14, -4), "right"),
      ("Erasteel", col["Erasteel"], 2.35, 48.85, (-14, 6), "right"),
      ("Outokumpu (Krefeld)", col["Outokumpu"], 6.56, 51.33, (-10, 26), "right"),
      ("Amazemet", col["Amazemet"], 21.01, 52.23, (-8, 16), "right"),
      ("LPW / Carpenter", ROUTE["gas"], -2.73, 53.36, (12, 14), "left")]
europe_map("02_n04_map_europe_labels", EP)

# ------------------------------------------------------------------ n03 powder prices
PP = rd("02_metal_powder_prices.csv")
PP.sort(key=lambda r: float(r["powder_typical_usd_kg"]))
FAM = {"stainless steel": "#566170", "tool steel": "#566170", "aluminium": "#2a78d6", "copper": "#c4561a",
       "nickel superalloy": "#1f7a5c", "cobalt alloy": "#1f7a5c", "titanium": "#7b52c7", "shape-memory": "#7b52c7"}
fig, ax = plt.subplots(figsize=(13, 7.2)); fig.subplots_adjust(left=0.2, right=0.97, top=0.9, bottom=0.12)
ax.set_xscale("log"); ax.set_xlim(1.5, 1500)
for i, r in enumerate(PP):
    lo, hi, ty, b = (float(r[k]) for k in ("powder_low_usd_kg", "powder_high_usd_kg", "powder_typical_usd_kg", "bulk_usd_kg"))
    c = FAM[r["family"]]
    ax.plot([lo, hi], [i, i], color=c, lw=12, alpha=0.35, solid_capstyle="round")
    ax.scatter([ty], [i], s=90, color=c, zorder=4)
    ax.scatter([b], [i], s=80, marker="D", facecolor="white", edgecolor=INK, lw=1.4, zorder=4)
    ax.plot([b, lo], [i, i], color=GREY, lw=0.8, ls=(0, (2, 3)))
    ax.text(hi * 1.12, i, f"×{ty / b:.0f}", va="center", fontsize=13, color=INK, fontweight="bold")
ax.set_yticks(range(len(PP))); ax.set_yticklabels([r["alloy"] for r in PP], fontsize=14)
ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
ax.set_xlabel("Price  (USD per kg, log scale)")
ax.grid(True, axis="x", which="major", color=GRID); ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.text(1.5, len(PP) - 0.1, "◇ bulk metal (ingot, bar, sheet; order of magnitude)    ● typical AM powder    bar: quoted range    ×: powder / bulk",
        fontsize=12.5, color=GREY, va="bottom", transform=ax.transData)
save(fig, "02_n03_powder_prices")

# ------------------------------------------------------------------ n05 CO2
C = rd("02_powder_co2.csv")
fig, ax = plt.subplots(figsize=(11, 6.6)); fig.subplots_adjust(left=0.2, right=0.96, top=0.9, bottom=0.13)
C.sort(key=lambda r: float(r["virgin_t_co2_per_t"]))
for i, r in enumerate(C):
    v, rc = float(r["virgin_t_co2_per_t"]), float(r["recycled_t_co2_per_t"])
    alloy = "powder" in r["element_or_alloy"]
    ax.annotate("", (rc, i), (v, i), arrowprops=dict(arrowstyle="-|>", color="#1f7a5c", lw=2, mutation_scale=16, shrinkA=6, shrinkB=6))
    ax.scatter([v], [i], s=110, color="#a8480f" if not alloy else "#1b2433", zorder=4)
    ax.scatter([rc], [i], s=110, facecolor="white", edgecolor="#1f7a5c", lw=2.2, zorder=4)
    ax.text(v + 0.25, i + 0.05, f"{v:g}", va="center", fontsize=12, color=INK)
    ax.text(rc - 0.25, i + 0.05, f"{rc:g}", va="center", ha="right", fontsize=12, color="#1f7a5c")
ax.set_yticks(range(len(C))); ax.set_yticklabels([r["element_or_alloy"] for r in C], fontsize=14)
ax.set_xlabel("t CO₂ per t of metal (cradle to gate)"); ax.set_xlim(-0.8, 12.5)
ax.grid(True, axis="x", color=GRID); ax.set_axisbelow(True)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_title("● virgin raw material   ○ recycled (scrap) raw material", loc="left", fontsize=13, color=GREY)
save(fig, "02_n05_powder_co2")

# ------------------------------------------------------------------ n06 market
K = rd("02_metal_market_ampower.csv")
fig, (ax, ax2) = plt.subplots(1, 2, figsize=(14, 6.4), gridspec_kw=dict(width_ratios=[1.45, 1]))
fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.12, wspace=0.22)
SEG = [("equipment_beur", "equipment", "#2f5f9e"), ("material_beur", "material", "#1f7a5c"), ("parts_beur", "part manufacturing", "#a8480f")]
for j, r in enumerate(K):
    x = j; b = 0
    fc = r["status"]
    if r["equipment_beur"]:
        for key, lab, c in SEG:
            h = float(r[key])
            ax.bar(x, h, bottom=b, color=c, alpha=0.45 if fc.startswith("forecast") else 1,
                   hatch="//" if fc.startswith("forecast") else None, edgecolor="white", width=0.72, label=lab if j == 0 else None)
            b += h
    else:
        ax.bar(x, float(r["total_beur"]), color="#b9b4a8", width=0.72, edgecolor="white")
    ax.text(x, float(r["total_beur"]) + 0.12, f'{float(r["total_beur"]):.2f}', ha="center", fontsize=12, color=INK)
ax.set_xticks(range(len(K))); ax.set_xticklabels([r["year"] + ("*" if r["status"] == "derived" else "") for r in K], fontsize=12)
ax.set_ylabel("Billion EUR"); ax.set_ylim(0, 9.8)
ax.legend(frameon=False, loc="upper left", fontsize=12)
ax.set_title("Metal AM market (AMPOWER 2024; 2028 = forecast)", loc="left", fontsize=14, color=INK)
for s in ("top", "right"):
    ax.spines[s].set_visible(False); ax2.spines[s].set_visible(False)
ax.text(len(K) - 2.6, 5.2, "* 2024: −2.9 %\n(AMPOWER 2025)", fontsize=11, color=GREY, ha="center")
U = [(r["year"], float(r["pbf_units"])) for r in K if r["pbf_units"]]
ux = [int(y) for y, _ in U]; uy = [v for _, v in U]
ax2.plot(ux[:-1], uy[:-1], "-o", color="#2f5f9e", lw=2.4, ms=8)
ax2.text(2028.3, 2700, "2028 forecast", ha="right", fontsize=11, color=GREY)
ax2.scatter([2028, 2028], [3882, 3195], s=70, facecolor="white", edgecolor="#2f5f9e", lw=2, zorder=4)
ax2.text(2027.8, 3882, "suppliers' view 3882", ha="right", va="center", fontsize=11, color=GREY)
ax2.text(2027.8, 3195, "buyers' view 3195", ha="right", va="center", fontsize=11, color=GREY)
for x, y in zip(ux[:-1], uy[:-1]):
    ax2.text(x, y + 120, f"{y:.0f}", ha="center", fontsize=11, color=INK)
ax2.set_ylim(0, 4400); ax2.set_xlim(2017.5, 2028.6); ax2.set_ylabel("units sold per year")
ax2.set_title("Metal PBF machines sold (AMPOWER 2024)", loc="left", fontsize=14, color=INK)
ax2.grid(True, axis="y", color=GRID); ax2.set_axisbelow(True)
save(fig, "02_n06_metal_market")

# ------------------------------------------------------------------ n07 powder routes (schematic)
fig, axs = plt.subplots(1, 4, figsize=(16, 6.2)); fig.subplots_adjust(left=0.01, right=0.99, top=0.86, bottom=0.02, wspace=0.06)
TIT = ["Gas atomisation (VIGA)", "Electrode induction (EIGA)", "Plasma atomisation (wire)", "Rotating electrode (PREP)"]
MELT, GAS, PL = "#c4561a", "#2a78d6", "#7b52c7"
rng = np.random.default_rng(3)


def spray(ax, x0, y0, spread, n=70, sz=(4, 30), color=INK, cone=True):
    for _ in range(n):
        t = rng.uniform(0.05, 1)
        x = x0 + rng.normal(0, spread * t); y = y0 - t * 5.2
        ax.scatter([x], [y], s=rng.uniform(*sz), color=color, alpha=0.75, lw=0)


for a, t in zip(axs, TIT):
    a.set_xlim(-5, 5); a.set_ylim(-7, 6.6); a.axis("off"); a.set_aspect("equal")
    a.add_patch(FancyBboxPatch((-4.7, -6.8), 9.4, 13.2, boxstyle="round,pad=0,rounding_size=0.4", fc="#fbfaf7", ec="#ddd6c6", lw=1))
    a.set_title(t, fontsize=15, fontweight="bold", color=INK)
# VIGA: crucible, stream, ring nozzle
a = axs[0]
a.add_patch(Polygon([(-2.2, 5.8), (2.2, 5.8), (1.4, 3.2), (-1.4, 3.2)], fc="#d9d3c7", ec=INK, lw=1.5))
a.add_patch(Polygon([(-1.9, 5.3), (1.9, 5.3), (1.3, 3.5), (-1.3, 3.5)], fc=MELT, ec="none"))
a.plot([0, 0], [3.2, 1.6], color=MELT, lw=4)
for s in (-1, 1):
    a.add_patch(Rectangle((s * 1.1 - 0.4, 1.3), 0.8, 0.6, fc=GAS))
    a.annotate("", (s * 0.15, 0.6), (s * 1.1, 1.3), arrowprops=dict(arrowstyle="-|>", color=GAS, lw=2))
spray(a, 0, 0.6, 1.3)
a.text(-4.4, -6.5, "vacuum induction melt; Ar or N₂ jets\nmost alloys · 15–150 µm · satellites", fontsize=11.5, color=GREY)
# EIGA: rotating bar into induction coil
a = axs[1]
a.add_patch(Rectangle((-0.6, 2.6), 1.2, 3.4, fc="#9aa3ad", ec=INK, lw=1.5))
a.add_patch(Polygon([(-0.6, 2.6), (0.6, 2.6), (0, 1.6)], fc="#9aa3ad", ec=INK, lw=1.5))
for yy in (1.9, 2.4, 2.9):
    a.add_patch(Rectangle((-1.5, yy - 0.12), 3.0, 0.24, fc="none", ec=MELT, lw=2.5))
a.annotate("", (0.9, 5.2), (-0.9, 5.2), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5, connectionstyle="arc3,rad=0.4"))
a.plot([0, 0], [1.6, 0.9], color=MELT, lw=3)
for s in (-1, 1):
    a.annotate("", (s * 0.15, 0.4), (s * 1.3, 1.0), arrowprops=dict(arrowstyle="-|>", color=GAS, lw=2))
spray(a, 0, 0.4, 1.2)
a.text(-4.4, -6.5, "rotating bar melted by a coil, no crucible\nTi and reactive alloys · no inclusions", fontsize=11.5, color=GREY)
# plasma atomisation: wire fed into 3 plasma torches
a = axs[2]
a.plot([0, 0], [6.0, 1.6], color="#9aa3ad", lw=5)
for ang in (-35, 0, 35):
    th = np.radians(ang - 90); ex, ey = 2.6 * np.cos(th + np.pi), 1.4 + 2.6 * np.sin(th + np.pi)
    a.annotate("", (0, 1.4), (ex * 1.0 if ang else 2.6, ey if ang else 1.4), arrowprops=dict(arrowstyle="-|>", color=PL, lw=4))
a.add_patch(Circle((0, 1.4), 0.35, fc=PL, alpha=0.5))
spray(a, 0, 1.0, 1.0, sz=(4, 22))
a.text(-4.4, -6.5, "plasma torches melt a Ti wire tip\nvery spherical, low oxygen · costly wire", fontsize=11.5, color=GREY)
# PREP: rotating electrode, plasma arc, centrifugal droplets
a = axs[3]
a.add_patch(Rectangle((-4.0, 0.9), 4.6, 1.0, fc="#9aa3ad", ec=INK, lw=1.5))
a.annotate("", (-3.2, 2.5), (-3.2, 0.3), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.5, connectionstyle="arc3,rad=-0.6"))
a.annotate("", (0.7, 1.4), (2.6, 1.4), arrowprops=dict(arrowstyle="-|>", color=PL, lw=4))
for k in range(26):
    th = rng.uniform(0, 2 * np.pi); r = rng.uniform(1.0, 3.6)
    a.scatter([0.7 + r * np.cos(th) * 0.35], [1.4 + r * np.sin(th)], s=rng.uniform(10, 40), color=INK, alpha=0.75, lw=0)
a.text(-1.9, -3.0, "bar spun at 10–30 000 rpm", ha="center", fontsize=12, color=INK)
a.text(-4.4, -6.5, "centrifugal droplets, no gas inside\nfew pores · coarse (50–250 µm)", fontsize=11.5, color=GREY)
save(fig, "02_n07_powder_routes")
print("ok")
