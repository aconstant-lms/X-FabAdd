# New slides for the technology_polymer and technology_unused decks (Nov 2026).
# Executed by gen_technology_decks.py inside the namespace of gen_am_technologies.py,
# so write(), sec_open(), head(), card(), table(), part(), figbox() ... and A, P, R are available.
import re as _re

for _k, _p in {"l01": "02_l01_beer_lambert", "l02": "02_l02_two_photon", "l03": "02_l03_viscosity_ruler",
               "l04": "02_l04_jetting_window", "l05": "02_l05_frenkel_sintering", "l06": "02_l06_yield_stress",
               "k03": "02_k03_maturity_2022", "i01i": "02_i01_price_vs_voxel_intro",
               "i03i": "02_i03_price_vs_build_volume_intro"}.items():
    A[_k] = f"NEW-{_k}"; P[_k] = _p

GREEN, BLUE = "#1f7a5c", "#2f5f9e"
P24 = "font-size:24px;line-height:1.25"


def tbl(rows, widths, size=24):
    """table() at a width other than the full 1664 px column."""
    return table(rows, widths, size).replace('width:1664px', f'width:{sum(widths)}px', 1)


def para(t, extra=""):
    return f'<p style="{P24};{extra}">{e(t)}</p>'


def strip(t, c=ORANGE):
    return (f'<div style="background:#fbfaf7;border:1px solid #ddd6c6;border-left:8px solid {c};border-radius:12px;padding:14px 22px">'
            f'<p style="font-size:28px;line-height:1.3;color:{INK}">{t}</p></div>')


def formula(t):
    return (f'<div style="background:{DARK};border-radius:12px;padding:16px 22px">'
            f'<p style="font-family:Inter, Arial, sans-serif;font-size:34px;line-height:1.3;color:#f6f3ec">{e(t)}</p></div>')


def cover(i, kicker, title, lead, k):
    write(i, f'<section id="{i}" data-transition="fade" style="background:{DARK};color:#f6f3ec;{BODY};padding:96px 128px;display:flex;flex-direction:column;justify-content:center">'
          f'<div style="display:flex;flex-direction:column;gap:32px;width:960px"><p style="font-size:24px;font-weight:600;letter-spacing:2px;color:#f0a46c">{e(kicker)}</p>'
          f'<h1 style="{FONT};font-size:104px;font-weight:600;line-height:1.02;color:#f6f3ec">{e(title)}</h1>'
          f'<p style="font-size:34px;line-height:1.35;color:#c9d2de">{e(lead)}</p>'
          '<p style="font-size:24px;color:#9fb0c4">Draft · November 2026</p></div>'
          f'<div style="position:absolute;right:128px;top:200px;width:600px;height:620px;background:#f6f3ec;border-radius:12px;padding:20px;display:flex;align-items:center;justify-content:center"><img src="/_blob/{A[k]}" alt="02_technologies/figures/{P[k]}.png" style="width:560px;height:580px;object-fit:contain"></div>'
          + notes('Chapter 02 of the EXED Polytechnique course, polymer session. Structure after Gebhardt & Hötter, Additive Manufacturing (Hanser 2016), ch. 2; drawing style after M. F. Ashby. Slides set aside for later (traditional technologies, metals, other processes) are in the deck "AM technologies: slides set aside". FR : technologies de fabrication additive des polymères. DE: additive Fertigungsverfahren für Kunststoffe.') + '</section>')


cover('cover-polymer', 'ADDITIVE MANUFACTURING · TECHNOLOGIES', 'AM technologies: polymers',
      'How polymer parts are printed, the six physical laws that limit every process, how ready a technology is, and an exercise: ten new technologies of 2022, where are they today?', 'f02')
cover('cover-unused', 'ADDITIVE MANUFACTURING · TECHNOLOGIES', 'AM technologies: slides set aside',
      'Traditional technologies, other processes and parked slides, kept for later sessions. Polymers and metals have their own decks.', 'f06')

# ---------------------------------------------------------------- pre-exercise price slide
_s = (R / 'slides' / 'vpp-prices.html').read_text()
_s = _s.replace('id="vpp-prices"', 'id="vpp-prices-intro"')
_s = _s.replace(f'/_blob/{A["i01"]}"', f'/_blob/{A["i01i"]}"').replace(f'/_blob/{A["i03"]}"', f'/_blob/{A["i03i"]}"')
_s = _s.replace('02_i01_price_vs_voxel.png', '02_i01_price_vs_voxel_intro.png').replace('02_i03_price_vs_build_volume.png', '02_i03_price_vs_build_volume_intro.png')
_s = _re.sub(r'Price on request: .*?high-viscosity film\)\. ', 'Price on request: UpNano NanoOne, Nano Dimension Fabrica Tera. Version shown before the exercise: the volumetric and high-viscosity-film printers are left out (they appear on the full slide in the debrief). ', _s)
write('vpp-prices-intro', _s)

# ---------------------------------------------------------------- part 6: six physical laws
part('part-laws', 6, 'Six physical laws', 'Every new process is a bet against a few laws of physics. Know them, and you can judge a founder\'s claim in five minutes.',
     ['Light in a resin', 'Thresholds and two photons', 'Viscosity and recoating', 'The jetting window', 'Sintering by viscous flow', 'Yield stress', 'Build rate against the mould'],
     'Each slide: one relation, one order of magnitude, what it decides, what it forbids, and the question to ask of any process. The same questions are on the exercise canvas. FR : lois physiques. DE: physikalische Gesetze.')


def law(i, n, sub, title, k, eq, decides, forbids, ask, source, note, w=1000, h=600):
    right = (f'<div style="flex:1;display:flex;flex-direction:column;gap:16px">{formula(eq)}'
             + card('Decides', decides, TOPS[1]) + card('Forbids', forbids, TOPS[3]) + card('Ask of any process', ask, TOPS[2]) + '</div>')
    write(i, sec_open(i, '48px 128px 100px') + head(f'SIX PHYSICAL LAWS · {n} OF 6' if n else 'SIX PHYSICAL LAWS · SYNTHESIS', sub, title)
          + f'<div style="display:flex;gap:40px;align-items:flex-start">{figbox(k, w, h)}{right}</div>'
          + src(source) + foot() + notes(note) + '</section>')


law('law-light', 1, 'LIGHT IN A RESIN · BEER–LAMBERT', 'Light dies exponentially in a resin: the penetration depth Dₚ sets layer and part size', 'l01',
    'I(z) = I₀ e^(−z/Dₚ)   ·   C_d = Dₚ ln(E/E_c)',
    'The cured depth grows only with the log of the dose: a layer is about one to two Dₚ thick.',
    'A part many Dₚ deep, lit from one side. Volumetric printing needs Dₚ of centimetres: clear resins, small parts.',
    'What is Dₚ of the resin, how deep is the part, and how is light brought to every voxel?',
    'Jacobs (1992) working curve; Kelly et al., Science 363 (2019); Regehly et al., Nature 588 (2020).',
    'Beer–Lambert: intensity decays as exp(−z/Dp); Dp = 1/(absorption coefficient), set by photoinitiator and UV absorber. Jacobs working curve: Cd = Dp ln(E/Ec), Ec the critical (gel) exposure. Typical SLA/DLP resins: Dp ≈ 0.1–0.2 mm, Ec ≈ 5–15 mJ/cm² (values to verify per resin data sheet); layers 25–100 µm. Volumetric printing (tomographic, xolography) needs light to reach the whole vial: low absorbance, Dp of several mm to cm, so transparent resins and part size of cm; the larger the vat the harder it is to deliver enough dose to every voxel. Values on the left chart are illustrative. FR : loi de Beer-Lambert, profondeur de pénétration, courbe de travail de Jacobs. DE: Lambert-Beer-Gesetz, Eindringtiefe, Arbeitskurve.')

law('law-threshold', 2, 'THRESHOLDS · ONE AND TWO PHOTONS', 'Curing only where you want: a dose threshold and a trick that concentrates the dose', 'l02',
    'gel if dose > E_c   ·   two photons: rate ~ I²',
    'Where the voxel forms. One photon: every plane gets the same energy, so cure by layers or by masks. Two photons: only the focus cures.',
    'Fine detail and speed together: two-photon voxels are below 1 µm, but writing rates are tiny.',
    'Which trick decides where the process cures (mask, oxygen, two photons, two colours, many angles), and what does it cost?',
    'Tumbleston et al., Science 347 (2015) (CLIP); Kelly et al. (2019) (tomography); Regehly et al. (2020) (xolography).',
    'One-photon absorption: rate proportional to I, the power crossing each plane is the same, so a focused beam cures a column; layers or masks confine the cure. Two-photon absorption: rate proportional to I², energy per plane ∝ 1/w(z)², so only the focal volume passes the threshold (2PP, Nanoscribe, UpNano). Oxygen inhibition: a thin dead zone (tens of µm) at an oxygen-permeable window lets CLIP pull the part continuously. Xolography: one colour excites a light sheet, a second colour (the image) cures only where both meet. Tomographic volumetric printing: projections from many angles add up; only the part volume passes the threshold. FR : seuil de gel, absorption à deux photons, inhibition par l’oxygène. DE: Gelschwelle, Zwei-Photonen-Absorption, Sauerstoffinhibierung.')

law('law-viscosity', 3, 'VISCOSITY · RECOATING', 'Viscosity decides how a fresh layer arrives, and so which materials a process can use', 'l03',
    'F = 3π η R⁴ (dh/dt) / (2 h³)',
    'A vat refills a thin gap only if η is low (about 0.1–3 Pa·s). Tough, filled or long-chain resins are 10 to 1000 times more viscous.',
    'Large layers of viscous resin in a vat: the force grows with R⁴ and 1/h³. Ways out: heat the resin, or carry it on a film.',
    'How does the process bring a fresh layer, and what viscosity does it accept?',
    'Stefan (1874) and Reynolds (1886) squeeze-film flow; resin viscosities from data sheets, orders of magnitude to verify.',
    'Squeeze film between two discs of radius R at gap h (Stefan–Reynolds): F = 3πηR⁴ (dh/dt) / (2h³). Separating a 100 mm part from the window at 50 µm gap, or pulling fresh resin in, scales with η R⁴ / h³: it is the reason vat printers stay small or slow with viscous resins. Better mechanical properties need higher molecular weight oligomers and fillers, hence higher viscosity: the trade-off between printability and toughness. Viscosity falls roughly exponentially with temperature (Arrhenius), so heating is one way out; carrying a thin layer of resin on a moving film is the other. Ruler values are indicative ranges (to verify): water 0.001 Pa·s, standard resins 0.1–3 Pa·s, honey ≈ 10 Pa·s, polymer melts 10²–10⁴ Pa·s at zero shear. FR : viscosité, film écrasé, recouchage. DE: Viskosität, Quetschfilm, Beschichtung.')

law('law-jetting', 4, 'JETTING · OHNESORGE NUMBER', 'A jetted ink must sit in a narrow window: 1 < Z < 10, a viscosity of a few mPa·s', 'l04',
    'Z = 1/Oh = √(ρ γ d) / η   ·   1 < Z < 10',
    'With ρ = 1000 kg/m³, γ = 0.03 N/m and a 30 µm nozzle, the ink must be 3–30 mPa·s at jetting temperature.',
    'Long chains and heavy fillers: inks are short molecules that cure into a network, and the material is tied to the print head.',
    'Can a third party make a material for the process, or is the user locked in?',
    'Derby, Annu. Rev. Mater. Res. 40, 395 (2010); Reis & Derby (2000).',
    'Drop-on-demand printing window after Derby (2010): Reynolds Re = ρvd/η, Weber We = ρv²d/γ, Ohnesorge Oh = √We/Re, Z = 1/Oh. Z < 1: viscous dissipation stops ejection; Z > 10: satellite drops. Minimum We ≈ 4 to eject; splashing above We^0.5 Re^0.25 ≈ 50. Worked example: √(1000 × 0.03 × 3×10⁻⁵) = 0.03, so Z between 1 and 10 means η between 3 and 30 mPa·s; industrial heads quote about 10–20 mPa·s. Consequence: jettable photopolymers are low-viscosity monomer blends; properties and supply depend on the machine maker. FR : jet de matière, nombre d’Ohnesorge, fenêtre d’impression. DE: Freistrahl, Ohnesorge-Zahl, Druckfenster.')

law('law-sintering', 5, 'SINTERING · FRENKEL', 'Particles and sheets bond by viscous flow: time, temperature and pressure trade off', 'l05',
    '(x/a)² = 3 γ t / (2 η a)',
    'The neck between particles grows faster with a low melt viscosity (hot), small particles and pressure.',
    'Viscous, filled or high-molecular melts in a few seconds per layer: porosity and a weak z direction. Pressure helps, but the press sets the part height.',
    'What joins the layers, at what temperature, and how many seconds does it get?',
    'Frenkel, J. Phys. USSR 9, 385 (1945); particle radius 12 µm, γ = 0.03 N/m.',
    'Frenkel’s viscous sintering of two spheres of radius a: (x/a)² = 3γt/(2ηa). It is a scaling law: real polymer melts are viscoelastic, shear-thinning and not at uniform temperature, so measured coalescence in powder bed fusion takes longer than the curves suggest. Use it to compare: ten times the viscosity needs ten times the time. Electrophotographic or sheet lamination adds heat and pressure to close the gaps within a short layer time; consolidation under a press limits the stack height. FR : frittage visqueux, loi de Frenkel, formation des ponts. DE: viskoses Sintern, Frenkel-Gesetz, Halsbildung.')

law('law-yield', 6, 'YIELD STRESS · SUPPORT', 'A liquid that must stand needs a yield stress, a supporting bath, or to cure as it is laid', 'l06',
    'h ≈ τ_y / (ρ g)',
    'A bath of 10–100 Pa holds a soft part a few centimetres high; a gel cured on the fly builds walls of a metre.',
    'Printing a runny silicone or resin into air. A bath has to be removed afterwards and can contaminate the part.',
    'What holds the part up while it is still liquid, and how is it taken out?',
    'Coussot, J. Non-Newtonian Fluid Mech. 211 (2014); Hinton et al., Science Advances 1 (2015).',
    'Hydrostatic estimate: a column stands if its weight stress ρgh stays below the yield stress τy, so h ≈ τy/ρg (ρ = 1100 kg/m³ on the chart). Support baths of granular or microgel media (FRESH printing, Hinton 2015) have yield stresses of order 10–100 Pa (to verify) and hold soft liquids in place until they cure. Gels that cure under UV as they leave the nozzle skip the bath and build large parts with few supports. Silicone cures by platinum-catalysed addition, thermally (minutes to hours) or UV-triggered. FR : seuil d’écoulement, bain support, réticulation. DE: Fließgrenze, Stützbad, Vernetzung.')

write('law-rate', sec_open('law-rate', '48px 128px 100px') + head('SIX PHYSICAL LAWS · SYNTHESIS', 'BUILD RATE', 'Speed is volume per hour of the whole chain, against a mould that fills in seconds')
      + '<div style="display:flex;gap:40px;align-items:flex-start"><div style="width:1000px;display:flex;flex-direction:column;gap:18px">'
      + formula('Q = A × Δz / t_layer      ·      Q = V_envelope / t_build')
      + tbl([['Process', 'Assumptions', 'Envelope rate'],
               ['Injection moulding, 1 cavity', '20 cm³ part, 20 s cycle', '3 600 cm³/h'],
               ['Injection moulding, 8 cavities', 'same part and cycle', '28 800 cm³/h'],
               ['DLP vat printer', '192 × 120 mm, Δz = 50 µm, 3 s per layer', '≈ 1 400 cm³/h'],
               ['Your process', 'from the report', '?']], [330, 450, 220], size=24)
      + para('Illustrative numbers. A printer fills only 10–30 % of its envelope with parts.', f'color:{GREY}') + '</div>'
      + '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + card('Then add', 'washing, post-cure, support or powder removal, inspection: per part, by hand or by machine', TOPS[1])
      + card('Cost', 'adding material takes time: printing cost grows about linearly with part volume, moulding cost does not', TOPS[3])
      + card('Ask of any process', 'how many parts per hour, all steps included, and at what volume does the mould win?', TOPS[2]) + '</div></div>'
      + src('Envelope rate = build area × layer thickness / layer time. Worked examples, not vendor data.') + foot()
      + notes('Productivity is the bridge from physics to economics (chapter 05). Layer-wise processes: Q = A Δz / t_layer, where t_layer is set by the slowest of the clocks (cure, recoat, sinter). Volumetric processes: the whole envelope in one exposure, but envelopes are cm-scale. Injection moulding: a 20 cm³ part every 20 s is 1 cm³/s per cavity; tools carry 1 to 64 cavities. DLP example: 19.2 × 12 × 0.005 cm³ = 1.15 cm³ every 3 s = 1 380 cm³/h of envelope. Printed parts fill a fraction of the envelope and each needs post-processing; the mould needs weeks and tens of k€ before the first part. FR : productivité, taux de construction. DE: Aufbaurate, Produktivität.') + '</section>')

write('law-questions', sec_open('law-questions') + head('SIX PHYSICAL LAWS · SYNTHESIS', 'CHECKLIST', 'Six questions to ask of any new process, before reading the founder’s claims')
      + table([['Question', 'The law that answers it', 'Typical trap'],
               ['1. What sets the smallest detail?', 'voxel: spot, Dₚ, droplet, particle', 'a resolution valid only for a tiny part'],
               ['2. What sets the largest part?', 'Beer–Lambert; press or oven size; τ_y > ρgh', '“scalable” without saying how light, heat or support scale'],
               ['3. What sets the speed?', 'Q = A Δz / t_layer; dose, power, sintering time', 'one layer’s speed, not the whole chain'],
               ['4. Which materials, and why only those?', 'viscosity and jetting windows; transparency', 'proprietary feedstock: lock-in'],
               ['5. What joins one layer to the next?', 'over-cure, viscous flow, pressure, or no layers', 'a weak z direction'],
               ['6. What happens after the printer?', 'post-cure, cleaning, support removal, inspection', 'the print is a fraction of the part cost']],
              [460, 620, 584], size=24)
      + strip('These six questions are box A and B of your exercise canvas.') + foot()
      + notes('The checklist links the laws to the canvas. Use it on any announcement: a resolution claim needs the voxel; a size claim needs the scaling of light, heat or support; a speed claim needs the whole chain; a material claim needs the window of the process. FR : liste de questions. DE: Prüfliste.') + '</section>')

# ---------------------------------------------------------------- part 7: maturity
part('part-maturity', 7, 'Maturity', 'How ready is a technology? Two indices, ten criteria, and a thumb rule you can use in ten minutes.',
     ['The 2022 landscape', 'Two axes, ten criteria', 'Levels 1 to 5 and the TRL', 'A rubric for thumb estimates', 'Where the new technologies stood in 2022'],
     'AMPOWER Maturity Index as published in AMPOWER Insights Vol. 11 (Nov. 2022), pp. 10–11; the rubric anchors at level 3 and the TRL mapping are ours. FR : maturité technologique. DE: Technologiereife.')

write('mi-def', sec_open('mi-def') + head('MATURITY', 'AMPOWER MATURITY INDEX', 'Two questions: does the process work, and is there a market around it?')
      + '<div style="display:flex;gap:40px">'
      + f'<div style="flex:1;display:flex;flex-direction:column;gap:14px"><h3 style="{FONT};font-size:40px;color:{BLUE}">Technology maturity index (x)</h3>'
      + para('Can the process and the machine make good parts, again and again?') + ul(['Series production capability', 'Machine concept', 'Process capability', 'In-process quality control'], 28) + '</div>'
      + f'<div style="flex:1;display:flex;flex-direction:column;gap:14px"><h3 style="{FONT};font-size:40px;color:{ORANGE}">Industrialisation maturity index (y)</h3>'
      + para('Can a company buy it, feed it and staff it with confidence?') + ul(['Technology source', 'Material availability', 'Installed base', 'Experience and applications', 'Knowledge base', 'Standards and best practice'], 28) + '</div></div>'
      + strip('Each criterion from 1 to 5. In 2022 the established polymer processes stood at about 4.5 on both axes.')
      + src('AMPOWER Insights Vol. 11, Additive Manufacturing: new polymer technologies, Nov. 2022, pp. 10–11.') + foot()
      + notes('The technology index looks at the process: can it make series parts, is the machine a product, is the process repeatable, is it monitored. The industrialisation index looks at the market around it: one or many sources, proprietary or open materials, how many machines installed, series applications, public knowledge, standards. A technology can be technically mature and still unbought (one source, proprietary feedstock), or bought early by one user who owns the application. AMPOWER weights the criteria and does not publish the weights. FR : indice de maturité technologique, indice d’industrialisation. DE: Technologiereifeindex, Industrialisierungsindex.') + '</section>')

write('mi-levels', sec_open('mi-levels') + head('MATURITY', 'LEVELS', 'From proof of concept to widespread use: five levels, and a thumb rule')
      + '<div style="display:flex;gap:40px;align-items:flex-start"><div style="width:1040px">'
      + tbl([['Level', 'AMPOWER label', 'Roughly'],
               ['1', 'Proof of concept', 'TRL 3–4: lab demonstration'],
               ['2', 'Prototype system', 'TRL 5–6: beta machines at test users'],
               ['3', 'First applications', 'TRL 7: series parts at pilot customers'],
               ['4', 'Industrial use', 'TRL 8: production in one or more industries'],
               ['5', 'Widespread industrial use', 'TRL 9: off-the-shelf, many industries']], [120, 420, 500], size=26) + '</div>'
      + '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + card('Thumb rule', 'x = mean of the 4 technology scores; y = mean of the 6 industrialisation scores', TOPS[1])
      + card('Honesty', 'AMPOWER’s weights are not public: your mean can differ by ± 0.5. Say so.', TOPS[3])
      + card('Time to industrial use', 'under 2 years, 2 to 5 years, over 5 years: give one, with a reason', TOPS[2]) + '</div></div>'
      + src('Levels: AMPOWER (2022). TRL: NASA / EU Horizon 2020 technology readiness levels; the mapping is our approximation.') + foot()
      + notes('The TRL scale (NASA, Mankins 1995; EU Horizon 2020) has nine levels for technology readiness; manufacturing readiness levels (MRL, US DoD) add the production side. AMPOWER’s two axes resemble TRL (x) and a market readiness (y). The mapping in the right column is an approximation for orientation, not an AMPOWER statement. FR : niveaux de maturité (TRL, MRL). DE: Technologie-Reifegrad, Fertigungsreifegrad.') + '</section>')

_rub = lambda rows: table([['Criterion', '1', '3', '5']] + rows, [400, 400, 420, 444], size=24)
write('mi-rubric-tech', sec_open('mi-rubric-tech') + head('MATURITY', 'RUBRIC · TECHNOLOGY', 'Technology index: four criteria, one piece of evidence each')
      + _rub([['Series production capability', 'basic R&D on manufacturing use', 'series of specific parts at pilot customers', 'full-scale series with integrated periphery'],
              ['Machine concept', 'proof-of-concept rig', 'first serial machines delivered', 'off-the-shelf, customisable series machines'],
              ['Process capability', 'basic process R&D', 'capable for specific parts', 'defect-free, repeatable, reproducible for any part'],
              ['In-process quality control', 'none', 'sensors and cameras log the process', 'closed-loop control and simulation']])
      + strip('Evidence, not adjectives: a named customer, a delivered machine, a measured scrap rate.')
      + src('Ends of each scale: AMPOWER Insights Vol. 11 (2022), p. 11. Level-3 anchors: course rubric.') + foot()
      + notes('Score 2 or 4 when the evidence sits between two anchors. A founder interview is a claim; a customer, a delivery or a published measurement is evidence. FR : grille d’évaluation. DE: Bewertungsraster.') + '</section>')
write('mi-rubric-ind', sec_open('mi-rubric-ind', '48px 128px 100px') + head('MATURITY', 'RUBRIC · INDUSTRIALISATION', 'Industrialisation index: six criteria about the market around the process')
      + _rub([['Technology source', 'one proprietary source, high IP barrier', 'a few licensees or competitors', 'many sources'],
              ['Material availability', 'proprietary feedstock only', 'a few qualified third-party materials', 'many suppliers, large choice'],
              ['Installed base', 'research labs only', 'tens of machines at industrial users', 'installed base across industries'],
              ['Experience and applications', 'application development', 'series application in one industry', 'series production in several industries'],
              ['Knowledge base', 'no general knowledge', 'papers, a user community', 'broad knowledge, research programmes'],
              ['Standards and best practice', 'none', 'company guidelines, first standards', 'established standards across industries']])
      + src('Ends of each scale: AMPOWER Insights Vol. 11 (2022), p. 10. Level-3 anchors: course rubric.') + foot()
      + notes('Industrialisation is what a buyer needs: a second source, materials, people who know the process, standards to qualify parts. A start-up with one machine model and one proprietary resin scores low here whatever its technology. FR : indice d’industrialisation. DE: Industrialisierungsindex.') + '</section>')

fig_full('mi-2022', 'MATURITY', '2022', 'In 2022 the ten new technologies sat between prototype and first applications', 'k03', h=700,
         source='AMPOWER Insights Vol. 11 (Nov. 2022), pp. 11 and 70. Numbers = exercise groups.',
         note='Grey dots: the 17 technology classes rated by AMPOWER in 2022; labelled: the established ones. Numbered circles: the ten companies of the exercise (1 xolo, 2 Readily3D, 3 Cubicure, 4 BCN3D, 5 Evolve, 6 Impossible Objects, 7 3Deus Dynamics, 8 Spectroplast, 9 Massivit, 10 Inkbit), 2022 rating only. 2 and 8, 1 and 7 share almost the same point and are nudged apart. The same grid, printed A1, is the wall for the exercise. FR : indice de maturité 2022. DE: Reifeindex 2022.')

# ---------------------------------------------------------------- part 8: exercise
part('part-exercise', 8, 'Exercise: polymer AM 2022 → 2026', 'November 2022: ten new technologies. Find the product, or prove there is none. Where are they today?',
     ['Mission and groups', 'First guess, then research', 'Canvas, bets, research log', 'Wall and twin duels'],
     'Run sheet, answer key and debrief in the instructor guide (claude.ai doc “Polymer AM 2022 → 2026 — instructor guide”). Student handout: “Polymer AM 2022 → 2026 — student handout”. FR : exercice. DE: Übung.')


def tile3(num, t, b, c):
    return (f'<div style="flex:1;display:flex;flex-direction:column;gap:8px;background:#fbfaf7;border:1px solid #ddd6c6;border-top:6px solid {c};border-radius:12px;padding:18px 22px">'
            f'<p style="{FONT};font-size:64px;font-weight:700;line-height:1;color:{c}">{e(num)}</p><h3 style="{FONT};font-size:36px;color:{INK}">{e(t)}</h3>{para(b)}</div>')


write('ex-mission', sec_open('ex-mission') + head('EXERCISE', 'THE MISSION', 'November 2022: your group owns one new technology. Three questions')
      + '<div style="display:flex;gap:24px">'
      + tile3('1', 'Physics', 'What can this process do that no other can, and which law limits it?', TOPS[1])
      + tile3('2', 'Option', 'Which product, for which customer, replacing which process? Or why none?', TOPS[3])
      + tile3('3', '2026', 'Where does the technology stand today on the maturity index?', TOPS[2]) + '</div>'
      + strip('A well-argued <b>“no option found”</b> scores as well as an option. The gap between your first guess and your research is part of the result.')
      + foot() + notes('Read the mission aloud. Insist on the second point: “not found” is a valid answer if it is argued from physics, market and money. FR : mission. DE: Auftrag.') + '</section>')

write('ex-groups', sec_open('ex-groups', '48px 128px 100px') + head('EXERCISE', 'GROUPS AND TWINS', 'Ten groups, ten companies, five pairs of twins')
      + table([['Group', 'Company', 'Technology (AMPOWER name)', 'Pages', 'Twin'],
               ['1', 'XOLO', 'volumetric vat polymerisation, xolography', '14–17', '2'],
               ['2', 'READILY3D', 'volumetric vat polymerisation, tomographic', '18–21', '1'],
               ['3', 'CUBICURE', 'area-wise film polymerisation, hot lithography', '24–27', '4'],
               ['4', 'BCN3D', 'area-wise film polymerisation, viscous lithography', '28–31', '3'],
               ['5', 'EVOLVE', 'electrophotography lamination', '34–37', '6'],
               ['6', 'IMPOSSIBLE OBJECTS', 'continuous fibre sheet lamination', '38–41', '5'],
               ['7', '3DEUS DYNAMICS', 'elastomer deposition in a granular bed', '44–47', '8'],
               ['8', 'SPECTROPLAST', 'vat vulcanisation of silicone', '48–51', '7'],
               ['9', 'MASSIVIT', 'thermoset (gel) deposition', '54–57', '10'],
               ['10', 'INKBIT', 'vision-controlled material jetting', '58–61', '9']], [140, 360, 840, 170, 154], size=24)
      + src('Packet: report pp. 10–11 + your 4 pages + your twin’s first 2 pages. AMPOWER Insights Vol. 11, Nov. 2022.') + foot()
      + notes('Page numbers are the printed numbers of the report. Twins share a physics family; their fates may differ, which is the point of the duel. FR : groupes, jumeaux. DE: Gruppen, Zwillinge.') + '</section>')

_tl = [('5 min', '1 · Briefing', 'packet, twin, roles if you want them'), ('15 min', '2 · First guess', 'canvas A–E and bets, packet and slides only; then locked'),
       ('25 min', '3 · Research', 'any source, AI included; canvas F and research log'), ('5 min', '4 · Post', 'two dots on the wall, your row in the shared table'),
       ('25 min', '5 · Twin duels', '90 s per group, 1 min questions, room vote'), ('20 min', '6 · Reveal', 'what happened, scores, lessons')]
write('ex-timeline', sec_open('ex-timeline') + head('EXERCISE', 'TIMELINE · 95 MINUTES', 'Six steps; the first guess is locked before you research')
      + '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">'
      + ''.join(f'<div style="display:flex;flex-direction:column;gap:6px;background:#fbfaf7;border:1px solid #ddd6c6;border-top:6px solid {TOPS[j % 4]};border-radius:12px;padding:16px 20px">'
                f'<p style="{FONT};font-size:48px;font-weight:700;line-height:1;color:{TOPS[j % 4]}">{e(m)}</p><h3 style="{FONT};font-size:32px;color:{INK}">{e(t)}</h3>{para(b)}</div>'
                for j, (m, t, b) in enumerate(_tl)) + '</div>'
      + foot() + notes('Project a countdown during steps 2, 3 and the duels. Collect or photograph the bet sheets at the end of step 2: that is what “locked” means. FR : déroulé. DE: Ablauf.') + '</section>')

_cv = [('A · Physics', 'path in the morphological box; what only this process can do'), ('B · Killer limit', 'the law that limits size, speed or material, with one number'),
       ('C · Option', 'product, customer, parts per year, process replaced, why it wins, or why none'), ('D · 2026 dot', 'technology and industrialisation index, time to industrial use'),
       ('E · Bets', 'three probabilities from the bet sheet'), ('F · After research', 'new dot, new bets, found / not found, confidence, what changed your mind')]
write('ex-canvas', sec_open('ex-canvas') + head('EXERCISE', 'THE CANVAS · A3', 'One canvas per group: A–E before research, F after')
      + '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">' + ''.join(card(t, b, TOPS[j % 4]) for j, (t, b) in enumerate(_cv)) + '</div>'
      + strip('Boxes A and B: answer the six physics questions before reading the founder’s interview.')
      + foot() + notes('The canvas is in the student handout (printable A3). Box A uses the morphological box; box B one of the six laws; box D the rubric of part 7. FR : canevas. DE: Arbeitsblatt.') + '</section>')

write('ex-bets', sec_open('ex-bets') + head('EXERCISE', 'BETS', 'Three bets, the same for every group: true in November 2026?')
      + table([['Statement', 'First guess (%)', 'After research (%)'],
               ['1. The company still operates independently under its own name', '', ''],
               ['2. It sells its printers to customers (not only parts or services)', '', ''],
               ['3. Its process makes end-use parts in series for at least one named customer', '', '']], [1024, 320, 320], size=26)
      + '<div style="display:flex;gap:24px">' + formula('score = (p − outcome)²')
      + card('Reading the score', '0 is perfect; “50 %” always scores 0.25; 90 % and wrong costs 0.81, 60 % and wrong costs 0.36', TOPS[1]) + '</div>'
      + foot() + notes('Brier score per bet: p as a fraction, outcome 1 if true and 0 if false; lower is better. It rewards honest uncertainty, not bold claims. The class sees every group’s score, first guess and after research. FR : paris, score de Brier. DE: Wetten, Brier-Score.') + '</section>')

write('ex-research', sec_open('ex-research') + head('EXERCISE', 'RESEARCH · 25 MINUTES', 'Research freely, but every number needs a page you have opened')
      + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px">'
      + card('Any source', 'web, AI, trade press, a phone call, a colleague in the room', TOPS[0])
      + card('AI is a lead', 'an AI answer is not a source: find the page behind it, with its date', TOPS[3])
      + card('Log it', 'three claims with their source, and one AI claim you found wrong or unsupported', TOPS[1])
      + card('Organise yourselves', 'cover technology, market, operations and money; no fixed roles', TOPS[2]) + '</div>'
      + strip('Then: your two dots on the wall and your row in the shared table.') + foot()
      + notes('Walk the room. Ask each group: what is your source for that, and what date is it? Push groups that found a 2026 fact to explain it with the physics of part 6. FR : recherche documentaire. DE: Recherche.') + '</section>')

write('ex-wall', sec_open('ex-wall', '48px 128px 100px') + head('EXERCISE', 'THE WALL', 'Place two dots: your first guess and your answer after research')
      + f'<div style="display:flex;gap:40px;align-items:flex-start">{figbox("k03", 1100, 640)}'
      + '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + card('Colour 1', 'first guess, step 2', TOPS[1]) + card('Colour 2', 'after research, step 3', TOPS[3])
      + card('On each dot', 'your group number', TOPS[0]) + card('Shared table', 'one row per group: dots, bets, verdict', TOPS[2]) + '</div></div>'
      + foot() + notes('Print 02_k03_maturity_2022_wall.pdf on A1. The circles are AMPOWER’s 2022 ratings; groups add two sticky dots each. At the reveal, add the 2026 positions in a third colour. FR : mur des estimations. DE: Schätzwand.') + '</section>')

write('ex-duel', sec_open('ex-duel') + head('EXERCISE', 'TWIN DUELS · 5 MINUTES PER PAIR', 'Same physics, possibly different fates: the duel is where you find out why')
      + '<div style="display:flex;gap:40px"><div style="width:800px;display:flex;flex-direction:column;gap:14px">'
      + ul(['Group A: 90 s · physics, option or none, 2026 dot', 'Group B: 90 s', 'Cross-questions: one each, 1 min', 'Room vote, 30 s: which option would you fund with your company’s money? A, B or neither'], 28) + '</div>'
      + '<div style="flex:1">' + tbl([['Pair', 'Twins'], ['1–2', 'XOLO · READILY3D'], ['3–4', 'CUBICURE · BCN3D'], ['5–6', 'EVOLVE · IMPOSSIBLE OBJECTS'],
                                        ['7–8', '3DEUS DYNAMICS · SPECTROPLAST'], ['9–10', 'MASSIVIT · INKBIT']], [140, 684], size=26) + '</div></div>'
      + foot() + notes('Cut speakers at 90 s. Note the vote per pair on the board; it is compared with what happened in the debrief. FR : duel. DE: Duell.') + '</section>')

# ---------------------------------------------------------------- part 9: debrief
part('part-debrief', 9, 'Debrief: 2022 → 2026', 'What happened to the ten technologies, what the physics predicted, and what it says about developing a product.',
     ['Readiness 2022 → 2026', 'What became of the companies', 'Five patterns', 'Takeuchi & Nonaka: the rugby team', 'Back to your company'],
     'Show only after the duels. FR : débriefing. DE: Nachbesprechung.')

write('db-patterns', sec_open('db-patterns', '48px 128px 100px') + head('DEBRIEF', 'FIVE PATTERNS', 'Own an application, not a printer: five patterns from ten companies')
      + '<div style="display:grid;grid-template-columns:1fr 1fr;gap:18px">'
      + card('1 · Bought by its application', 'Cubicure: acquired by Align Technology (2023), already its investor, for direct-printed orthodontic devices', TOPS[0])
      + card('2 · From printer to parts', 'Spectroplast and Inkbit sell parts and services; Massivit sells tooling through RapidWings (2026)', TOPS[1])
      + card('3 · Science push stays in the lab', 'xolo and Readily3D sell research instruments: the light-penetration limit (law 1) holds', TOPS[2])
      + card('4 · Same physics, opposite fates', 'Cubicure vs BCN3D (bankrupt 2025); Evolve wound down (2026) while Impossible Objects raised $40 M', TOPS[3])
      + card('5 · “2 to 5 years” was optimistic', 'of the four companies AMPOWER placed 2–5 years from industrial use, one closed and one was bought', TOPS[0])
      + card('Question for the room', 'which of these was visible in the 2022 report? (Align was listed as Cubicure’s investor.)', TOPS[1]) + '</div>'
      + foot() + notes('Sources in tables/02_ampower_maturity_2022_2026.csv and the instructor guide. Align–Cubicure: definitive agreement Sept. 2023, about €79 M, completed afterwards. BCN3D: voluntary bankruptcy May 2025, assets bought by Quantum; VLM continues in Supernova. Evolve: winding down, assets auctioned Sept.–Oct. 2026. Impossible Objects: $40 M series B (Sept. 2026), drone bodies at Rock Island Arsenal. Massivit: RapidWings platform (June 2026), service centre Barcelona (July 2026). The 2–5-year group in 2022: Cubicure, Inkbit, Impossible Objects, Evolve. FR : enseignements. DE: Erkenntnisse.') + '</section>')

write('db-takeuchi', sec_open('db-takeuchi', '48px 128px 100px') + head('DEBRIEF', 'TAKEUCHI & NONAKA (1986)', 'The new new product development game: a rugby team, not a relay race')
      + table([['Characteristic', 'In their cases', 'In today’s exercise'],
               ['Built-in instability', 'Fuji-Xerox: a copier at half the cost, in two years', 'one broad goal: find the market or prove there is none'],
               ['Self-organising teams', 'Honda City: a young team sets its own concept', 'no fixed roles; the group covers tech, market, money'],
               ['Overlapping phases', 'Canon, Honda: design starts before tests end', 'first guess, research, revision'],
               ['Multilearning', 'Honda team sent to Europe; NEC engineers with hobbyists', 'research as a field trip; one AI error logged'],
               ['Subtle control', 'checkpoints, peer pressure, group rewards', 'time boxes, shared table, group scores'],
               ['Transfer of learning', 'Canon’s review format reused; Epson: next model 40 % better', 'which of the ten would you test at home?']], [400, 640, 624], size=24)
      + strip('Their own limit: the method may not fit breakthrough science or a lone genius. Volumetric printing is such a case.')
      + src('H. Takeuchi, I. Nonaka, “The New New Product Development Game”, Harvard Business Review, Jan.–Feb. 1986.') + foot()
      + notes('Six characteristics: built-in instability, self-organising project teams (autonomy, self-transcendence, cross-fertilisation), overlapping development phases, multilearning (multilevel, multifunctional), subtle control, organisational transfer of learning (and unlearning). Limits named by the authors: extraordinary effort, may not suit breakthrough projects in biotechnology or chemistry, mammoth projects such as aerospace, or genius-led development. Discussion: Cubicure grew with a lead customer in a joint development programme (overlap, multilearning); science-push volumetric start-ups match the authors’ limit. The rugby image later gave Scrum its name. FR : développement de produits, équipe auto-organisée. DE: Produktentwicklung, selbstorganisierendes Team.') + '</section>')

write('db-transfer', sec_open('db-transfer') + head('DEBRIEF', 'BACK TO YOUR COMPANY', 'One technology, one part, one test: what would you do next year?')
      + '<div style="display:flex;gap:24px">'
      + tile3('1', 'Which part?', 'one part of your own products where a law of part 6 is on your side', TOPS[1])
      + tile3('2', 'Which technology?', 'of the ten, or an established one, and its maturity dot', TOPS[3])
      + tile3('3', 'Which test?', 'the cheapest test that would kill the idea early, and who runs it', TOPS[2]) + '</div>'
      + strip('Write it on the back of your canvas; we come back to it in chapter 05, economics.')
      + foot() + notes('Transfer of learning (Takeuchi & Nonaka): the lesson leaves the room only if it is attached to a part, a technology and a test with an owner. Chapter 05 prices the part. FR : transfert. DE: Transfer.') + '</section>')

# ---------------------------------------------------------------- part 10 references, other sections
part('part-refs', 10, 'References', 'Standards, books, papers and reports used in this chapter.', ['Classification', 'Additive manufacturing', 'Physics of the laws', 'Reports and press'], '')
write('references-physics', sec_open('references-physics') + head('REFERENCES', 'PHYSICS AND EXERCISE', 'Physical laws, maturity and product development')
      + ul(['P. F. Jacobs, Rapid Prototyping & Manufacturing: Fundamentals of Stereolithography, SME, 1992.',
            'J. R. Tumbleston et al., Continuous liquid interface production of 3D objects, Science 347, 1349 (2015).',
            'B. E. Kelly et al., Volumetric additive manufacturing via tomographic reconstruction, Science 363, 1075 (2019).',
            'M. Regehly et al., Xolography for linear volumetric 3D printing, Nature 588, 620 (2020).',
            'B. Derby, Inkjet printing of functional and structural materials, Annu. Rev. Mater. Res. 40, 395 (2010).',
            'J. Frenkel, Viscous flow of crystalline bodies under surface tension, J. Phys. USSR 9, 385 (1945).',
            'T. J. Hinton et al., 3D printing of soft materials by freeform reversible embedding (FRESH), Sci. Adv. 1, e1500758 (2015).',
            'P. Coussot, Yield stress fluid flows: a review, J. Non-Newtonian Fluid Mech. 211, 31 (2014).',
            'AMPOWER Insights Vol. 11, Additive Manufacturing: new polymer technologies, Nov. 2022.',
            'H. Takeuchi, I. Nonaka, The New New Product Development Game, Harvard Business Review, Jan.–Feb. 1986.'], 24)
      + foot() + notes('Bibliographic details to check against the originals before publication (page numbers, article numbers).') + '</section>')

part('part-other', 'X', 'Other AM processes', 'Paste extrusion, microprinting, laser CVD and electrochemical AM: kept for later sessions.',
     ['Paste extrusion', 'Microprinting', 'Laser CVD', 'Electrochemical AM'], 'Set aside from the polymer and metal sessions, Nov 2026.')
