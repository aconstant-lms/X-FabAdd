# New slides for the technology_metal deck (Nov 2026).
# Executed by gen_technology_decks.py after slides_polymer_new.py, in the namespace of
# gen_am_technologies.py: write(), sec_open(), head(), card(), table(), part(), figbox(),
# formula(), strip(), tbl(), cover() ... and A, P are available.

for _k, _p in {"m01": "02_m01_melt_cool", "m02": "02_m02_residual_stress", "m03": "02_m03_murakami_fatigue",
               "m04": "02_m04_rate_resolution",
               "n01": "02_n01_metal_price_vs_volume", "n02w": "02_n02_map_world_numbered", "n02e": "02_n02_map_europe_labels",
               "n03": "02_n03_powder_prices", "n04w": "02_n04_map_world_numbered", "n04e": "02_n04_map_europe_labels",
               "n05": "02_n05_powder_co2", "n06": "02_n06_metal_market", "n07": "02_n07_powder_routes"}.items():
    A[_k] = f"NEW-{_k}"; P[_k] = _p

cover('cover-metal', 'ADDITIVE MANUFACTURING · TECHNOLOGIES', 'AM technologies: metals',
      'How metal parts are printed by melting or bonding powder and wire, what the machines cost, and the five physical laws that decide density, stress, fatigue, post-processing and speed.', 'f06')

part('part-mlaws', 6, 'Five physical laws for metals', 'A metal part is a weld, thousands of metres long. Five laws decide whether it is dense, straight, strong in fatigue, and affordable.',
     ['Cooling and crystallisation', 'Internal stresses', 'Cycles, defects and fatigue', 'Post-processing: HIP, heat, machining', 'Build rate against resolution'],
     'Same format as the polymer laws: one relation, one order of magnitude, what it decides, what it forbids, and the question to ask of any metal part. FR : lois physiques des métaux. DE: physikalische Gesetze für Metalle.')


def mlaw(i, n, sub, title, k, eq, decides, forbids, ask, source, note, w=1000, h=600):
    right = (f'<div style="flex:1;display:flex;flex-direction:column;gap:16px">{formula(eq)}'
             + card('Decides', decides, TOPS[1]) + card('Forbids', forbids, TOPS[3]) + card('Ask of any metal part', ask, TOPS[2]) + '</div>')
    write(i, sec_open(i, '48px 128px 100px') + head(f'METAL PHYSICS · {n} OF 5', sub, title)
          + f'<div style="display:flex;gap:40px;align-items:flex-start">{figbox(k, w, h)}{right}</div>'
          + src(source) + foot() + notes(note) + '</section>')


mlaw('mlaw-melt', 1, 'COOLING AND CRYSTALLISATION', 'The gradient G and the growth rate R decide which crystals grow, and how fine', 'm01',
     'G / R → shape of the crystals   ·   G · R = dT/dt → size:  λ ≈ A (dT/dt)^(−1/3)',
     'Laser PBF cools at 10⁵–10⁷ K/s: cells below 1 µm, strong as built, with columnar grains along the build direction.',
     'Wrought-like properties straight from the printer: anisotropy and fine, metastable structures need heat treatment. Wrong energy input adds pores (lack of fusion, keyholes).',
     'Which microstructure does the specification ask for, and which heat treatment gets there from the as-built state?',
     'Kurz & Fisher, Fundamentals of Solidification (1998); DebRoy et al., Prog. Mater. Sci. 92 (2018).',
     'Solidification map: thermal gradient G at the liquid–solid front against its growth rate R. G/R sets the morphology (high: planar, cellular, columnar; low: dendritic, equiaxed); G·R is the cooling rate and sets the scale, λ ≈ A (dT/dt)^(−1/3), A ≈ 50 µm·(K/s)^(1/3) for Al alloys (to verify for other alloys). Process boxes are orders of magnitude (DebRoy 2018): casting G 10²–10⁴ K/m, R 10⁻⁵–10⁻³ m/s; DED and WAAM G 10⁴–10⁶, R 10⁻³–10⁻²; laser PBF G 10⁶–10⁷, R 0.1–1. Epitaxial growth on the layer below gives columnar grains along z, hence anisotropy. The melt pool also makes the pores: too little energy density E = P/(v h t) leaves lack-of-fusion pores, too much gives keyhole pores; dense parts come from a window of roughly 50–100 J/mm³ (alloy- and machine-dependent). Link to Andrei’s materials slides (microstructures, scales). FR : solidification, gradient thermique, vitesse de croissance, dendrites, grains colonnaires. DE: Erstarrung, Temperaturgradient, Wachstumsgeschwindigkeit, Dendriten, Stängelkristalle.')

mlaw('mlaw-stress', 2, 'RESIDUAL STRESS', 'The hot track shrinks on a cold part: residual stress reaches the yield strength', 'm02',
     'σᵢ = Eᵢ (εᵢ − αᵢ Δθᵢ),  ε₁ = ε₂,  σ₁A₁ + σ₂A₂ = 0   →   σ ≈ E α Δθ ≥ σ_y',
     'Thermal stress is 1.4 to 9 times the as-built yield strength, so parts carry stress near yield, held by the build plate.',
     'Cutting the part from the plate before stress relief (it springs back); thin walls and large flat areas (distortion, cracks); crack-prone alloys.',
     'What holds the part during the build, when is it stress-relieved, and how much does it move when cut off?',
     'Mercelis & Kruth, Rapid Prototyping J. 12 (2006); DebRoy et al. (2018). Values: estimates for a fully constrained track.',
     'Two-bar model, as in the materials slides: a hot layer (1) bonded to a cold part (2), each thermoelastic, σᵢ = Eᵢ(εᵢ − αᵢΔθᵢ); same strain (bonded) and zero resultant force give σ₁ = −E₁E₂A₂(α₁Δθ₁ − α₂Δθ₂)/(E₁A₁ + E₂A₂), tension in the new layer and compression below; for a thin layer on a large part σ₁ → E α Δθ. Temperature-gradient mechanism (Mercelis & Kruth 2006): the hot layer expands, is compressed by the cold material below and yields; on cooling it shrinks and is left in tension. Upper bound σ ≈ E α ΔT with ΔT ≈ solidus − build-plate temperature. Chart values (estimates, to verify): Ti-6Al-4V E 114 GPa, α 8.6×10⁻⁶ /K, ΔT 1450 K, as-built σy ≈ 1 GPa; 316L 193 GPa, 16×10⁻⁶, 1250 K, ≈ 0.45 GPa; IN718 200 GPa, 13×10⁻⁶, 1150 K, ≈ 0.7 GPa; AlSi10Mg 70 GPa, 21×10⁻⁶, 350 K (200 °C plate), ≈ 0.25 GPa. Because the bound exceeds yield, the residual stress saturates near yield. Remedies: plate preheat, scan strategy (islands), supports as anchors, stress relief 600–900 °C before removal. Binder jetting has no melt pool (shrinkage instead); cold spray leaves compressive peening stress. FR : contraintes résiduelles, distorsion, détensionnement. DE: Eigenspannungen, Verzug, Spannungsarmglühen.')

mlaw('mlaw-fatigue', 3, 'CYCLES, DEFECTS AND FATIGUE', 'Under cycles, the largest defect, not the average density, sets the life', 'm03',
     'σ_w = 1.43 (HV + 120) / (√area)^(1/6)',
     'An as-built part loses its endurance limit to pores and surface notches; HIP and machining bring it back near wrought. A 100 µm defect cuts the Ti-6Al-4V fatigue limit by a third compared with 10 µm.',
     'Judging a fatigue part by “99.9 % dense”; fatigue-critical parts left as built; tensile residual stress at the surface.',
     'How many cycles must the part see, what is the largest defect inspection can miss, and is the surface machined?',
     'Murakami, Metal Fatigue: Effects of Small Defects (2002); Beretta & Romano, Int. J. Fatigue 94 (2017); Ashby, Materials Selection (S–N curve).',
     'Left: S–N curves, schematic (no data): wrought machined, AM HIP plus machined, AM as built. As built, fatigue cracks start at surface valleys and near-surface pores, often with tensile residual stress, and the knee of the curve disappears. Right: Murakami’s √area model: fatigue limit σw (MPa) from Vickers hardness HV and the square root of the defect area projected normal to the stress (µm); 1.43 for surface defects, 1.56 for internal ones. Derived for steels with HV < 400; used for AM Ti and steels as a trend (Beretta & Romano 2017), values to verify. Worked example, Ti-6Al-4V HV 350: √area 10 µm gives ≈ 460 MPa, 100 µm gives ≈ 310 MPa. Defect sizes (indicative): gas pores 5–50 µm, lack-of-fusion pores 50–500 µm, as-built surface valleys 20–150 µm. Link to the risk deck: what inspection cannot see, the part must tolerate (QF32, Sioux City). FR : fatigue, courbe de Wöhler, limite d’endurance, défauts. DE: Ermüdung, Wöhlerlinie, Dauerfestigkeit, Fehler.')

write('mlaw-post', sec_open('mlaw-post', '48px 128px 100px') + head('METAL PHYSICS · 4 OF 5', 'POST-PROCESSING', 'HIP closes internal pores, machining removes the surface: neither is free')
      + f'<div style="display:flex;gap:40px;align-items:flex-start">{figbox("c10", 620, 560)}<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + tbl([['Problem from the print', 'Remedy', 'Typical'],
             ['residual stress', 'stress relief, before cutting from the plate', '600–900 °C, 1–2 h'],
             ['internal pores', 'hot isostatic pressing (HIP)', '100–200 MPa, 900–1250 °C, 2–4 h'],
             ['surface pores, roughness', 'machining, polishing, peening', 'Ra 5–20 µm as built'],
             ['fine, anisotropic grains', 'heat treatment to the alloy spec', 'alloy-dependent'],
             ['supports, trapped powder', 'removal, cleaning, CT inspection', 'by hand, hours']], [300, 420, 284], size=24)
      + card('Ask of any metal part', 'which steps, in which shops, how many days, and who qualifies the whole chain?', TOPS[2]) + '</div></div>'
      + src('ASTM F3301 (thermal post-processing of PBF metal parts); Atkinson & Rickinson, Hot Isostatic Processing (1991).') + foot()
      + notes('HIP closes pores that are not connected to the surface: argon pressure acts on every face, creep and diffusion bond the pore walls. Surface-connected pores and roughness stay and must be machined, which is why fatigue-critical PBF parts are HIPed and machined on functional faces. Each step adds days and transport between specialised shops; the space deck’s cost model makes the print about a fifth of the part cost (course estimate). Temperatures and times in the table are typical ranges (ASTM F3301), to check per alloy. FR : post-traitements, CIC, usinage, rugosité. DE: Nachbearbeitung, HIP, Zerspanung, Rauheit.') + '</section>')

mlaw('mlaw-rate', 5, 'BUILD RATE', 'Fine processes are slow, fast processes are coarse: machining closes the gap', 'm04',
     'laser PBF:  Q = v · h · t ≈ 1000 mm/s × 0.1 mm × 0.03 mm ≈ 11 cm³/h per laser',
     'A 500 cm³ titanium bracket takes about 45 h on one laser, 12 h on four; a wire-arc cell lays a 20 kg steel blank in a working day.',
     'Large parts with fine detail in one step: choose net shape (PBF, binder jetting) or near-net shape plus machining (DED, WAAM, cold spray).',
     'How many machine hours per part, at what hourly rate, and how many hours of post-processing?',
     'Rates and features from the metal process slide (makers’ data sheets, DebRoy 2018, Williams 2016, Yin 2018); binder jetting: printing step only.',
     'Rates (cm³/h, indicative): laser PBF 5–20 per laser, up to ~1000 with 12 lasers; binder jetting 1000–12000 for printing alone, then debinding and sintering over a day with 15–20 % shrinkage; DED powder 0.1–2 kg/h (13–250 cm³/h steel); cold spray up to ~6 kg/h Cu; WAAM 1–10 kg/h (125–1250 cm³/h steel). Smallest features: PBF 0.1–0.3 mm, BJ 0.1–0.4 mm, LMD 0.5–4 mm, cold spray 2–8 mm, WAAM 3–10 mm. Worked example: 500 cm³ / 11 cm³/h ≈ 46 h. Machine hour: a 0.5–1 M$ LPBF machine over 5 years at 4000 h/year is 25–50 $/h of depreciation alone, before gas, powder, staff and floor space (chapter 05). FR : taux de construction, quasi-forme, usinage de finition. DE: Aufbaurate, endkonturnah, Endbearbeitung.')

write('mlaw-questions', sec_open('mlaw-questions') + head('METAL PHYSICS · SYNTHESIS', 'CHECKLIST', 'Six questions to ask of any metal AM part, before the business case')
      + table([['Question', 'The law that answers it', 'Typical trap'],
               ['1. Is there a qualified window for this alloy and machine?', 'energy density, cooling rate', 'a datasheet value from another machine'],
               ['2. What holds the part, and when is stress relieved?', 'σ ≈ E α ΔT ≥ σ_y', 'distortion found after cutting from the plate'],
               ['3. What is the largest defect inspection can miss?', 'Murakami √area', '“99.9 % dense” as a fatigue argument'],
               ['4. Which faces are machined, which stay as built?', 'surface notches, HIP limits', 'HIP expected to fix the surface'],
               ['5. How many machine and post-processing hours per part?', 'Q = v h t; process chain', 'print time quoted, chain ignored'],
               ['6. What does qualification cost per part family?', 'class of part (risk deck)', 'qualifying one part at a time']],
              [560, 500, 604], size=24)
      + strip('The same questions open the metal exercise: print, cast from a printed mould, repair, or keep in stock?') + foot()
      + notes('Use the checklist on any metal AM claim. Questions 1–5 are physics; question 6 links to the risk deck (part class ↔ consequence of failure ↔ speed of adoption) and to chapter 05 (qualification as an investment). FR : liste de questions. DE: Prüfliste.') + '</section>')

exec(compile(open(__import__('pathlib').Path(HERE_DECK) / 'slides_metal_supply.py').read(), 'slides_metal_supply.py', 'exec'))

part('part-mrefs', 8, 'References', 'Metal AM processes, physics of the laws, supply chain, standards.', ['Processes', 'Physics', 'Machines, powders and markets', 'Standards'], '')
write('references-mphysics', sec_open('references-mphysics') + head('REFERENCES', 'METAL PHYSICS', 'Melting, residual stress, fatigue and post-processing')
      + ul(['T. DebRoy et al., Additive manufacturing of metallic components – Process, structure and properties, Prog. Mater. Sci. 92, 112 (2018).',
            'W. Kurz, D. J. Fisher, Fundamentals of Solidification, 4th ed., Trans Tech, 1998.',
            'P. Mercelis, J.-P. Kruth, Residual stresses in selective laser sintering and selective laser melting, Rapid Prototyping J. 12, 254 (2006).',
            'Y. Murakami, Metal Fatigue: Effects of Small Defects and Nonmetallic Inclusions, Elsevier, 2002.',
            'S. Beretta, S. Romano, A comparison of fatigue strength sensitivity to defects for materials manufactured by AM or traditional processes, Int. J. Fatigue 94, 178 (2017).',
            'ASTM F3301, Standard for additive manufacturing – post processing methods – thermal post-processing metal parts made via powder bed fusion.',
            'H. V. Atkinson, B. A. Rickinson, Hot Isostatic Processing, Adam Hilger, 1991.'], 26)
      + foot() + notes('Bibliographic details to check against the originals before publication.') + '</section>')
