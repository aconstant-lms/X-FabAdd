# Part 7 of the technology_metal deck: machines, powders and makers (Nov 2026).
# Executed from slides_metal_new.py in the namespace of gen_am_technologies.py.
# Data: 02_technologies/tables/02_machines_metal_makers.csv, 02_metal_powder_prices.csv, 02_powder_makers.csv,
# 02_powder_co2.csv, 02_metal_market_ampower.csv. Figures: 02_technologies/figures/02_n00_metal_supply.py.

part('part-msupply', 7, 'Machines, powders and makers',
     'Who makes the powder and the machines, where, at what price, and what the metal AM market is worth.',
     ['From melt to powder: four routes', 'Who makes the powder, and at what price', 'Powder footprint: virgin vs recycled',
      'Machines: price against build volume', 'Makers worldwide; China’s large formats', 'The market, 2016–2028'],
     'This part gathers the supply-chain data of Andrei’s 04_Metal and 05_Market slides and of AMPOWER, checked and completed with web sources (Nov 2026). '
     'Several items also belong in the aviation, repair and space decks (see the project note “am-metal-supply-redistribution”). '
     'FR : chaîne d’approvisionnement, poudres, fabricants de machines. DE: Lieferkette, Pulver, Maschinenhersteller.')

# ---------- powder routes
write('msup-routes', sec_open('msup-routes', '48px 128px 100px') + head('MACHINES, POWDERS AND MAKERS', 'POWDER ROUTES', 'Four ways to turn molten metal into spherical powder')
      + figbox('n07', 1664, 500)
      + '<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">'
      + card('Gas atomisation dominates', 'about two thirds of AM powder volume; flexible on alloy, cheapest spherical route; satellites and gas pores to control', TOPS[1])
      + card('Only 15–45 or 20–63 µm is used', 'laser PBF takes the fine cut, DED and EBM the coarse one: yield, not melting, sets the price', TOPS[3])
      + card('Scrap can be the feedstock', 'Outokumpu (330 t/year from steel scrap), Continuum and 6K (plasma, from turnings), Amazemet (ultrasonic, lab scale)', TOPS[2])
      + '</div>'
      + src('metal-am.com, “An introduction to metal powders for AM” and “The evolving metal powder marketplace”; 04_Metal pp. 5–8; market share: CB Insights (gas atomisation 68 % of volume, 2025).') + foot()
      + notes('Schematic, not to scale. VIGA: vacuum induction melting, then argon or nitrogen jets break the melt stream; most alloys; particles 15–150 µm; satellites (small particles stuck to large ones) and argon-filled pores. '
              'EIGA (electrode induction gas atomisation, ALD trademark): a rotating pre-alloyed bar melts in an induction coil and drips into the gas nozzle; no crucible, so no ceramic inclusions: titanium and reactive alloys; needs bar stock. '
              'Plasma atomisation (AP&C, now Colibrium Additive): plasma torches melt a wire tip; very spherical, low oxygen titanium; cost of the wire. '
              'PREP (plasma rotating electrode): a bar spun at high speed, its end melted by a plasma arc; centrifugal droplets, almost no internal pores, coarse powder. '
              'Water atomisation, the highest-volume route, makes irregular powder for press-and-sinter PM and some binder jetting. '
              'Yield: the share of the batch in the 15–45 µm cut can be well below half (EIGA patents quote about 70 % below 106 µm), so the rest is sold to other processes or remelted. '
              'Ultrasonic atomisation (Amazemet rePowder, Add. Manuf. 2024) turns small scrap batches into powder for alloy development. '
              'FR : atomisation au gaz, à plasma, électrode tournante, granulométrie, satellites. DE: Gasverdüsung, Plasmaverdüsung, rotierende Elektrode, Korngrößenverteilung.') + '</section>')

# ---------- powder makers map
RT = {'gas atomisation': '#2a78d6', 'plasma': '#7b52c7', 'water, multi-route': '#566170',
      'from scrap': '#1baf7a', 'ultrasonic': '#eda100'}
PWM = [(1, 'Carpenter Additive', 'Reading PA, US · VIGA · Ni, Co, steel, Ti', '#2a78d6'),
       (2, '6K Additive', 'Burgettstown PA, US · microwave plasma from scrap · 200 → 800 t/yr by end 2026', '#1baf7a'),
       (3, 'Continuum Powders', 'Houston, US · plasma melt-to-powder · IN718 qualified on Velo3D', '#1baf7a'),
       (4, 'Colibrium Additive (AP&C)', 'Boisbriand, Canada · plasma atomised Ti', '#7b52c7'),
       (5, 'Tekna', 'Sherbrooke, Canada · induction-plasma spheroidisation', '#7b52c7'),
       (6, 'Equispheres', 'Ottawa, Canada · aluminium', '#2a78d6'),
       (7, 'BLT', 'Xi’an, China · machine maker with own powder', '#2a78d6'),
       (8, 'AVIMETAL', 'Beijing, China (AVIC) · Ti, Ni', '#2a78d6'),
       (9, 'Sanyo Special Steel', 'Himeji, Japan', '#2a78d6'), (10, 'Daido Steel', 'Nagoya, Japan', '#2a78d6')]


def maps_slide(i, sub, title, kw, ke, items, key, source, note):
    its = ''.join(f'<div style="display:flex;gap:8px;align-items:flex-start;width:505px">' + ring(n, c) + f'<p style="font-size:21px;line-height:1.18"><b>{e(nm)}</b> · {e(what)}</p></div>' for n, nm, what, c in items)
    kk = ''.join(f'<div style="display:flex;gap:8px;align-items:center"><div style="width:22px;height:22px;border-radius:11px;background:#fbfaf7;border:3px solid {c}"></div><p style="font-size:21px">{e(t)}</p></div>' for t, c in key.items())
    write(i, f'<section id="{i}" data-transition="fade" style="background:#f3f1ec;color:#1b2433;font-family:Inter, Arial, sans-serif;padding:48px 128px 96px;display:flex;flex-direction:column;gap:14px">'
          + f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;color:#a8480f">MACHINES, POWDERS AND MAKERS · {e(sub)}</p><h2 style="{FONT};font-size:54px;font-weight:600;line-height:1.08;color:#1b2433">{e(title)}</h2>'
          + '<div style="display:flex;gap:24px;align-items:flex-start"><div style="width:1040px;display:flex;flex-direction:column;gap:12px">'
          + f'<img src="/_blob/{A[kw]}" alt="02_technologies/figures/{P[kw]}.png" style="width:1040px;height:390px;border-radius:12px;flex-shrink:0">'
          + f'<div style="display:flex;flex-wrap:wrap;gap:6px 30px">{its}</div><div style="display:flex;flex-wrap:wrap;gap:6px 22px">{kk}</div></div>'
          + f'<div style="flex:1;display:flex;flex-direction:column;gap:8px"><img src="/_blob/{A[ke]}" alt="02_technologies/figures/{P[ke]}.png" style="width:600px;height:705px;border-radius:12px;flex-shrink:0"><p style="font-size:22px;color:#566170">Europe in detail</p></div></div>'
          + src(source) + foot() + notes(note) + '</section>')


maps_slide('msup-powder-makers', 'POWDER MAKERS', 'Powder makers: steel and nickel groups in Europe, titanium and recycling in North America',
           'n04w', 'n04e', PWM, RT,
           'Makers’ sites; metal-am.com; MarketPublishers producer lists (2024–2026); 04_Metal pp. 6–8. Data: tables/02_powder_makers.csv.',
           'Ring colour = main powder route. Europe: Sandvik Osprey, Neath (VIGA; nickel, cobalt, steel); Höganäs, Höganäs (water, gas and plasma; the largest press-and-sinter supplier); Carpenter Additive’s LPW site, Widnes; Oerlikon AM, Barleben; Heraeus AMLOY, Hanau; Linde AMT, Pullach (also the argon); m4p, Feistritz; Aubert & Duval, Les Ancizes (aerospace grades; owned since 2022 by Airbus, Safran and Tikehau); Erasteel (Eramet), plants in Sweden and France; Outokumpu, Krefeld powder plant, 330 t/year from scrap (plant location to check); Amazemet, Warsaw (ultrasonic, lab scale). '
           'Consolidation: Carpenter bought LPW (2018) and Puris (2017); 6K bought Global Metal Powders (2023) and an atomiser from the defunct Uniformity Labs. Chinese machine makers (BLT) integrate their own powder; one Chinese report puts China’s import dependence for AM powder at about a third, highest for nickel superalloys (to verify). Several head-office locations marked “to check” in the table. '
           'Redistribute: titanium and nickel supply → aviation and space decks; scrap-to-powder → repair deck (revert from machining). '
           'FR : producteurs de poudre, recyclage, rachats. DE: Pulverhersteller, Recycling, Übernahmen.')

# ---------- powder prices
write('msup-powder-prices', sec_open('msup-powder-prices', '48px 128px 100px') + head('MACHINES, POWDERS AND MAKERS', 'POWDER PRICES', 'AM powder costs 6 to 30 times the metal it is made of')
      + '<div style="display:flex;gap:32px;align-items:flex-start">' + figbox('n03', 1150, 640)
      + '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + card('Ti-6Al-4V', 'ingot ≈ 7.5 $/kg, AM powder ≈ 140–420 $/kg: the market average fell to ≈ 140–210 $/kg in 2024–25 as Chinese capacity grew', TOPS[3])
      + card('Lot size counts', 'IN718 at 60–70 $/kg for an aerospace contract, 300–500 $/kg in 10 kg bottles: a factor 5', TOPS[1])
      + card('Ask', 'how many kg per year, which particle cut, how many reuse cycles are allowed?', TOPS[2])
      + '</div></div>'
      + src('makerverse.com (2025); met3dp.com; LPW case study (IN718); LP Information and MarketPublishers (Ti powder averages 2024–25); carboncredits.com (Ti ingot); 04_Metal p. 9. Data: tables/02_metal_powder_prices.csv.') + foot()
      + notes('Bars: published ranges, mixing small-lot retail (msesupplies, 04_Metal p. 9) and bulk contract prices; dot: typical value used in the course; diamond: bulk metal price, an order of magnitude only (to check per alloy, LME and producer price lists). '
              'Two numbers on Andrei’s p. 9 cited Gemini/ChatGPT; they are replaced here by web sources, still to confirm with a supplier quote. Powder cost per part also depends on reuse: unmolten powder is sieved and blended back (04_Metal p. 10), within the limits on oxygen pick-up set by the specification. '
              'Market sizes (to verify): atomised titanium AM powder ≈ 11 kt in 2025 at ≈ 210 $/kg (MarketPublishers), titanium alloy AM powders ≈ 2.5 kt in 2024 at ≈ 140 $/kg (LP Information): the two reports disagree on volume, so quote ranges, not a figure. '
              'Link to chapter 05 (cost per part) and to the exercise: the powder is rarely the largest cost item for a PBF part; machine hours are. FR : prix des poudres, lot, réutilisation. DE: Pulverpreise, Losgröße, Wiederverwendung.') + '</section>')

# ---------- CO2
write('msup-co2', sec_open('msup-co2', '48px 128px 100px') + head('MACHINES, POWDERS AND MAKERS', 'POWDER FOOTPRINT', 'Recycled feedstock cuts the CO₂ of a nickel powder by a factor of ten')
      + '<div style="display:flex;gap:32px;align-items:flex-start">' + figbox('n05', 1050, 640)
      + '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + card('The raw material dominates', 'mining and refining nickel, cobalt and molybdenum, not the atomiser, set the footprint of a superalloy powder', TOPS[1])
      + card('316L: 5.1 → 0.6 t CO₂/t', 'IN718: 9.6 → 0.9 t CO₂/t when the melt is made from scrap (Sandvik’s estimate)', TOPS[2])
      + card('Ask', 'is the powder’s feedstock certified scrap, and does the part qualification allow it?', TOPS[3])
      + '</div></div>'
      + src('P. A. Davies (Sandvik Additive Manufacturing), “Sustainability of inert gas atomised powders”, PowderMet 2023, via 04_Metal p. 12. Data: tables/02_powder_co2.csv.') + foot()
      + notes('Cradle-to-gate t CO₂ per t of metal and kWh per kg (energy column in the table): virgin vs recycled raw material for each element, and for two powders. Values are Sandvik’s, for its own melt shop and energy mix: an order of magnitude, not a general LCA. '
              'Consequences: AM’s buy-to-fly advantage (less material machined away) matters most for alloys with a high virgin footprint (Ni, Co, Ti); scrap-based powders (6K, Continuum, Outokumpu) sell on CO₂ as well as price. '
              'Redistribute: aviation deck (buy-to-fly ratio and CO₂), repair deck (machining revert as feedstock). FR : empreinte carbone, matière recyclée. DE: CO₂-Fußabdruck, Rezyklat.') + '</section>')

# ---------- machines price vs volume
write('msup-machines', sec_open('msup-machines', '48px 128px 100px') + head('MACHINES, POWDERS AND MAKERS', 'MACHINE PRICES', 'A litre of laser PBF build volume costs 2 to 200 k$, and China sits at the low end')
      + '<div style="display:flex;gap:32px;align-items:flex-start">' + figbox('n01', 1100, 700)
      + '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'
      + card('Western flagships', 'EOS M 400-4 ≈ 1–1.5 M$, Nikon SLM NXG XII 600 ≈ 1.5–3.5 M$, Velo3D Sapphire XC 1MZ ≈ 2–3.5 M$', TOPS[1])
      + card('Chinese machines', 'similar volume for half the price or less: Tianhong TH-M800 ≈ 0.8 M$ for 441 L, ZRapid iSLM420D ≈ 0.3 M$ (listings)', TOPS[2])
      + card('Lasers, not litres, set the rate', '12 to 64 lasers on the large beds: rate scales with the number of lasers (law 5)', TOPS[3])
      + '</div></div>'
      + src('laser-spec-hub (estimated ranges, 2026); 3dtechvalley; 3dnatives; All3DP; directindustry (Tianhong); 05_Market pp. 24–25, 28; metal-am.com. Data: tables/02_machines_metal_makers.csv.') + foot()
      + notes('Makers rarely publish prices: the ranges come from aggregators, resellers and marketplace listings and are indicative. The 2025 deck’s table (moved to the slides set aside) gave higher figures for SLM 125 and M 290; the SLM 500 envelope is 500 × 280 × 365 mm, not 500³. '
              'Price per litre falls with size, as for polymer printers (polymer deck, i03): a bigger chamber shares the optics, gas and control; but the laser count, not the litres, sets productivity. '
              'Binder jetting and bound-metal extrusion (squares) are cheaper machines but need a sintering furnace; Desktop Metal’s Studio System 2 is shown as history: the company was liquidated in 2025. '
              'Redistribute: space deck (large-format machines for engines: Nikon SLM and ArianeGroup, AMCM M 8K), aviation deck (qualified machine fleets). FR : prix machines, volume de fabrication. DE: Maschinenpreise, Bauraum.') + '</section>')

# ---------- makers map
PK = {'laser PBF': '#2a78d6', 'e-beam PBF': '#7b52c7', 'DED, laser': '#eda100', 'DED, wire': '#eb6834',
      'binder jet, extrusion': '#1baf7a', 'cold spray': '#a0522d'}
MWM = [(1, 'Velo3D', 'Fremont CA · LPBF', '#2a78d6'), (2, 'HP', 'Palo Alto CA · Metal Jet', '#1baf7a'),
       (3, 'Optomec', 'Albuquerque · LENS DED, repair', '#eda100'), (4, 'Sciaky', 'Chicago · EBAM 300 (5.8 m)', '#eb6834'),
       (5, 'ExOne (Arc Impact)', 'Pennsylvania · binder jetting', '#1baf7a'), (6, 'Markforged', 'Waltham MA · PX100, Metal X', '#1baf7a'),
       (7, '3D Systems', 'Rock Hill SC / Leuven · DMP', '#2a78d6'), (8, 'BLT', 'Xi’an · up to 1.5 m, 26 lasers', '#2a78d6'),
       (9, 'Farsoon', 'Changsha · FS1521M', '#2a78d6'), (10, 'Eplus3D', 'Hangzhou · EP-M2050, 64 lasers', '#2a78d6'),
       (11, 'HBD', 'Shanghai', '#2a78d6'), (12, 'ZRapid, Tianhong', 'Suzhou', '#2a78d6'),
       (13, 'JEOL', 'Tokyo · electron-beam PBF', '#7b52c7'), (14, 'SPEE3D, Titomic', 'Melbourne · cold spray', '#a0522d')]
maps_slide('msup-makers', 'MACHINE MAKERS', 'Metal machine makers: Germany for laser PBF, China for size, wire in the rest of Europe',
           'n02w', 'n02e', MWM, PK,
           'Makers’ sites; metal-am.com; Context (2025–26); 05_Market p. 28. Data: tables/02_machines_metal_makers.csv.',
           'Ring colour = main process. Europe: EOS and AMCM (Krailling, Starnberg), Nikon SLM Solutions (Lübeck), TRUMPF (Ditzingen), Colibrium Additive ex Concept Laser (Lichtenfels), ExOne GmbH (Gersthofen, now Anzu Partners), DMG MORI (Bielefeld, hybrid DED + milling), Gefertec (Berlin, WAAM), MX3D (Amsterdam), WAAM3D (Milton Keynes), Renishaw (Wotton-under-Edge), AddUp (Cébazat, Fives-Michelin), Prima Additive (Turin), Meltio (Linares, wire-laser), Norsk Titanium (Hønefoss), Arcam (Colibrium) and Freemelt (Mölndal, electron beam). '
           'Moves 2024–26: GE Additive renamed Colibrium Additive (2024); Nikon bought SLM Solutions (2023); Desktop Metal Chapter 11 (July 2025), US assets to Arc Impact for 7 M$; Velo3D rescued and relisted (2025). Build volumes of EBM, DED and cold-spray machines in the table are from memory: to check. '
           'Redistribute: repair deck (Optomec, DMG MORI hybrid, Meltio, cold spray), space deck (Sciaky, Norsk Titanium, large LPBF), aviation deck (Norsk Titanium Boeing 787 parts). FR : fabricants de machines. DE: Maschinenhersteller.')

# ---------- China
write('msup-china', sec_open('msup-china', '48px 128px 100px') + head('MACHINES, POWDERS AND MAKERS', 'CHINA', 'Chinese makers lead in units and bed size; EOS and Nikon SLM still lead in revenue')
      + '<div style="display:flex;gap:20px">'
      + tile('+24 %', 'metal PBF units shipped worldwide, Q4 2025 vs Q4 2024 (Context)', TOPS[2])
      + tile('4', 'Chinese vendors lead metal PBF unit share: BLT, Eplus3D, ZRapid, Farsoon', TOPS[1])
      + tile('2 050 mm', 'square bed of the Eplus3D EP-M2050, 64 lasers', TOPS[3])
      + tile('−4 %', 'metal machine shipments 2025, all technologies (binder jetting and extrusion fell)', TOPS[0]) + '</div>'
      + tbl([['Maker (country)', 'Large-format laser PBF', 'Build volume (mm)', 'Lasers'],
             ['BLT (China)', 'BLT-S1500', '1500 × 1500 × 1200', '26 × 500 W'],
             ['Farsoon (China)', 'FS1521M', 'Ø 1530 × 1650', '16 × 500 W'],
             ['Eplus3D (China)', 'EP-M2050', '2050 × 2050 × 1100', '64 × 500 W'],
             ['HBD (China)', 'HBD 1000Pro', '660 × 660 × 1250', '8 × 500 W'],
             ['Nikon SLM (Germany)', 'NXG XII 600', '600 × 600 × 600', '12 × 1000 W'],
             ['AMCM / EOS (Germany)', 'M 8K', '800 × 800 × 1200', '8 lasers'],
             ['Velo3D (USA)', 'Sapphire XC 1MZ', 'Ø 600 × 1000', '8 × 1000 W']], [420, 420, 500, 324], size=23)
      + src('Context Q2–Q4 2025 and Q1 2026 via metal-am.com, TCT, 3D Printing Industry; metal-am.com “China’s thriving metal AM industry” (05_Market p. 28); All3DP.') + foot()
      + notes('Context: China is the largest market for industrial printers by units, supplied mostly by domestic vendors; in Q1 2026 Farsoon and BLT credited titanium hinges and frames for foldable phones (the “3C” sector), and EOS more than doubled its metal shipments after a large contract with a defence drone maker. '
              'Western makers keep the revenue lead (higher prices, service, qualified fleets), Chinese makers the unit lead and the largest beds, driven by domestic aerospace and private space. '
              'AMPOWER 2026: the ten largest metal PBF makers held 78.3 % of revenue in 2025, down from 80 %: fragmentation alongside consolidation. '
              'Redistribute: space deck (Chinese private launchers and large beds), aviation deck (qualification as the barrier for Chinese machines in the West). FR : Chine, grands formats, parts de marché. DE: China, Großformat, Marktanteile.') + '</section>')

# ---------- market
write('msup-market', sec_open('msup-market', '48px 128px 100px') + head('MACHINES, POWDERS AND MAKERS', 'MARKET', 'Metal AM: 3.4 billion euros, flat in 2024, forecast to more than double by 2028')
      + figbox('n06', 1664, 470)
      + '<div style="display:flex;gap:20px">'
      + tile('−2.9 %', 'metal AM market 2024 (AMPOWER 2025)', TOPS[3])
      + tile('11.3 B€', 'all industrial AM 2025, +5.6 % (AMPOWER 2026)', TOPS[1])
      + tile('39 %', 'of AM machine sales are metal PBF (2024)', TOPS[2])
      + tile('20 %/yr', 'growth forecast in 2024 for 2023–28', TOPS[0]) + '</div>'
      + src('AMPOWER Report 2024 (via 04_Metal pp. 49–51); AMPOWER 2025 and 2026 press releases (metal-am.com, 3D Printing Industry, TCT). Data: tables/02_metal_market_ampower.csv.') + foot()
      + notes('Left: market by segment, equipment, material and part manufacturing (service bureaus and in-house production); 2024 derived from the −2.9 % reported in AMPOWER 2025 (no split available here); 2028 = AMPOWER 2024 forecast. Right: metal PBF machines sold per year, flat around 1500–1700 since 2018, with the suppliers’ and buyers’ 2028 forecasts. '
              'The gap between the 2024 forecast (+20 %/yr) and the 2024–25 actuals is itself a lesson for the exercise: forecasts by suppliers run ahead of buyers. Material and parts now grow faster than machines: the market grows by making parts, as in polymers. '
              'Wohlers 2026 counts all AM at 24.2 B$ in 2025 (+10.9 %), with a different scope: compare like with like. The AMPOWER 2025/2026 metal split is not in hand: to update if Andrei has the reports. FR : marché, prévisions. DE: Markt, Prognose.') + '</section>')

write('references-msupply', sec_open('references-msupply') + head('REFERENCES', 'MACHINES, POWDERS AND MAKERS', 'Powders, machines and markets')
      + ul(['AMPOWER Report 2024; AMPOWER Report 2025 and 2026 press releases, additive-manufacturing-report.com; AMPOWER Insights vol. 6, New metal AM technologies (2020).',
            'Context, quarterly 3D printer shipment reports Q2 2025 – Q1 2026 (contextworld.com).',
            'P. A. Davies, Sustainability of inert gas atomised powders, PowderMet 2023 (Sandvik Additive Manufacturing).',
            'Metal AM magazine: An introduction to metal powders for AM; The evolving metal powder marketplace; China’s thriving metal AM industry; Arc Impact to acquire Desktop Metal and ExOne assets (Sept 2025).',
            'Wohlers Report 2026, Wohlers Associates / ASTM International.',
            'Price aggregators (indicative): laser-spec-hub, makerverse, met3dp, 3dnatives, All3DP, directindustry, Alibaba listings.'], 26)
      + foot() + notes('Web sources consulted 17 Nov 2026; prices and head-office locations to check before publication.') + '</section>')
