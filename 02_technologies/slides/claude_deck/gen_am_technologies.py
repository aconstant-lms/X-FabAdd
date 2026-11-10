import json, html
from pathlib import Path
R=Path('/home/claude/deck02/project')
A={'carbon': '1a36628206234ecf69db55524ea00f26', 'j01': '2f48877385f11095635012aa60b42669', 'j02': 'a35f5d9472ea44a8a1f2a62134dc8ad1', 'j03': '7f534239f5c6d7005169468f2bf1d576', 'j04w': '900a90f63498e3f2acab1696afe2f31a', 'j04e': 'de811de1573bf63cc6ce70d2b9517af1', 'e05': 'f3a546cfe58d2306ca0c5f5392130406', 'a01n': '136a3e71f166f8cd9d68aed20795c2d1', 'c07n': 'd48fdbd2261c1b719d42e817c1bc8d60', 'd01n': '3daeb4b633f0c860b8cee80e27c10d58', 'g07': 'adf5ddd808c57f60e3501c97ca8ff1fe', 'c10': '977016cafecdf68c415b6ce3bdf097de', 'e04': 'bb08a8b1752281519e06f519540d2502', 'i01': 'ee321b7cd203c7fb2b9256e02dbfb001', 'i03': '4c06cfa6f8af2d3b47ff2919e24a30bc', 'i04w': 'bb68bccf4bb8e55c71bda29a19df5467', 'i04e': '599f065b94670d33a1bcfacfe68ee979', 'h01': 'faefb8329c71b4b7cd19b98734b9f5e1', 'h02': 'aa955dcbbb7c28eb7314809a32a3b745', 'h03': 'b792c142f6f6ceb091bd3c5409e38871', 'a00': '7e425f5b5db5bb0f9a3dc40ecaf1dcea', 'a01': '136a3e71f166f8cd9d68aed20795c2d1', 'b01': 'ba1da8f11a62e4137bdc3eb73d1bce3c', 'b02': 'de82ff157a3c7de8be62495253482af0', 'b03': 'c88a93a9f547b0ae012aa7a7292aaa8b', 'b04': 'cd97c8b8037b7981cc0011edfeac824f', 'b05': '28f9c4ac717389c4b631a80c973914ed', 'b06': 'e234f8fa75e7dc90bca9ef9f135b4e03', 'g01': '3704241184cd46ab557135c3be63c305', 'g02': '2d37f9abb66296ec4d326793f49d6ed5', 'g03': 'e3fbfbdafa4908867f6e9419a23dc496', 'g04': 'd78fe28568992d587be9a8ee6f5d1d10', 'g05': 'adb9bc354ef216f360c784834879d507', 'g06': '881a6a759a4398fc60a688080578eb1b', 'c00': '16a70d23fb389483c91af14cc9af0f99', 'c02': '8610ebd61c4b8bed1dcea7d0d6a51087', 'c07': 'd48fdbd2261c1b719d42e817c1bc8d60', 'c08': 'c0decacb3b2fc508a156d254a7820779', 'c09': 'fee969e751aa143e06ce6134c2809c20', 'd01': '3daeb4b633f0c860b8cee80e27c10d58', 'd02': '26097b6b7a88bdcf57b6f23552937217', 'e01': '99030d8c4e433eef44b7c4afa89e1287', 'e02': '62a2d20ea3b3598120ebded136f210c5', 'e03': 'dabcabb9cf1dd7e3333dee7394a83f24', 'f02': '5b94cb1b433a38181e556b76eca3480b', 'f03': 'db45ef150f9777ef5fdb4cdc33e5dccf', 'f04': 'dbfbf5478ac02c8c785e48cd23f667e2', 'f05': '8323fc33bc6d7101ea8bb49bcfa7332e', 'f06': '31ed34e3d725804c299749ff38ac6bff', 'f07': '3876cee9f5fa6d6c520446044ab37055', 'f08': '88ce66fdd4732e48de6b87043ad3b21f', 'f09': 'd6eec09ef97250f1a590ebd17d3b6173', 'f10': 'aa5ef7c9e5b693c6ffd2d586463eabca', 'f11': '8b7c934a5c0391096a0d317a83a777d8', 'f12': '0e34e712cc6b595b6c78f31f8d55e301'}
P={'j01':'02_j01_polymer_pyramid','j02':'02_j02_polymer_ashby_E_strength','j03':'02_j03_polymer_prices','j04w':'02_j04_map_world_numbered','j04e':'02_j04_map_europe_labels','e05':'02_e05_material_paths_physics','a01n':'02_a01_process_groups','c07n':'02_c07_heat_treatment_scales','d01n':'02_d01_file_layer_voxel','g07':'02_g07_twin_sheet_rolling','c10':'02_c10_hip','e04':'02_e04_groups_paths_matrix','i01':'02_i01_price_vs_voxel','i03':'02_i03_price_vs_build_volume','i04w':'02_i04_map_world_numbered','i04e':'02_i04_map_europe_labels','a00':'02_a00_colour_convention','a01':'02_a01_process_groups','b01':'02_b01_kitchen_primary_shaping','b02':'02_b02_kitchen_forming','b03':'02_b03_kitchen_separating','b04':'02_b04_kitchen_joining','b05':'02_b05_kitchen_coating','b06':'02_b06_kitchen_properties','g01':'02_g01_twin_casting','g02':'02_g02_twin_forging','g03':'02_g03_twin_milling','g04':'02_g04_twin_welding','g05':'02_g05_twin_thermal_spraying','g06':'02_g06_twin_quench_hardening','c00':'02_c00_ashby_process_tree','c02':'02_c02_injection_moulding','c07':'02_c07_heat_treatment_scales','c08':'02_c08_press_and_sinter','c09':'02_c09_four_routes','d01':'02_d01_file_layer_voxel','d02':'02_d02_point_line_area_volume','e01':'02_e01_material_paths','e02':'02_e02_clocks','e03':'02_e03_layer_interfaces','f02':'02_f02_vat_photopolymerisation','f03':'02_f03_material_extrusion','f04':'02_f04_material_jetting','f05':'02_f05_binder_jetting_chain','f06':'02_f06_laser_powder_bed_fusion','f07':'02_f07_directed_energy_deposition','f08':'02_f08_sheet_lamination','f09':'02_f09_cold_spray','f10':'02_f10_laser_cvd','f11':'02_f11_electrochemical_am','f12':'02_f12_paste_extrusion'}
FONT="font-family:'Space Grotesk', Inter, sans-serif"
BODY='font-family:Inter, Arial, sans-serif'
DARK='#0f1b2d'; LIGHT='#f3f1ec'; INK='#1b2433'; ORANGE='#c4561a'; GREY='#566170'
FOOT='EXED Polytechnique - Additive Manufacturing - 02 Technologies by Andrei Constantinescu 2027'
TOPS=['#1b2433','#2f5f9e','#1f7a5c','#a8480f']
e=html.escape
order=[]; sections={}
def write(i,body): (R/'slides'/f'{i}.html').write_text(body); order.append(i)
def foot(dark=False): return f'<p style="position:absolute;left:128px;bottom:8px;width:1664px;font-size:24px;color:{"#9fb0c4" if dark else "#6b6b6b"}">{FOOT}</p>'
def src(t): return f'<p style="position:absolute;left:128px;bottom:40px;width:1664px;font-size:24px;color:{GREY}">{e(t)}</p>'
def notes(t): return f'<aside>{e(t)}</aside>'
def img(k,w,h,extra=''):
    return (f'<div style="width:{w}px;height:{h}px;flex-shrink:0;background:#ffffff;border:1px solid #ddd6c6;border-radius:12px;padding:16px;display:flex;align-items:center;justify-content:center{extra}">'
            f'<img src="/_blob/{A[k]}" alt="02_technologies/figures/{P[k]}.png" style="width:{w-34}px;height:{h-34}px;object-fit:contain"></div>')
def head(kick,sub,title):
    s=f'<p style="font-size:24px;font-weight:600;letter-spacing:2px"><span style="color:{ORANGE};font-weight:700">{e(kick)}</span>'
    if sub: s+=f' <span style="color:{GREY}">· {e(sub)}</span>'
    return s+f'</p><h2 style="{FONT};font-size:54px;font-weight:600;line-height:1.08;color:{INK}">{e(title)}</h2>'
def sec_open(i,pad='56px 128px 100px'): return f'<section id="{i}" data-transition="fade" style="background:{LIGHT};color:{INK};{BODY};padding:{pad};display:flex;flex-direction:column;gap:20px">'
def card(t,body,c):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;background:#fbfaf7;border:1px solid #ddd6c6;border-top:5px solid {c};border-radius:12px;padding:16px 20px">'
            f'<p style="font-size:24px;font-weight:700;color:{c}">{e(t)}</p><p style="font-size:24px;line-height:1.25">{e(body)}</p></div>')
def ul(items,size=26): return f'<ul style="font-size:{size}px;line-height:1.32;padding-left:30px;display:flex;flex-direction:column;gap:10px">'+''.join(f'<li>{e(x)}</li>' for x in items)+'</ul>'
def table(rows,widths=None,size=24):
    h='<table style="width:1664px;border-collapse:collapse;background:#fbfaf7"><tr style="background:#0f1b2d">'
    for j,c in enumerate(rows[0]):
        w=f';width:{widths[j]}px' if widths else ''
        h+=f'<th style="font-size:24px;font-weight:700;text-align:left;padding:10px 14px;color:#f6f3ec{w}">{e(c)}</th>'
    h+='</tr>'
    for r in rows[1:]:
        h+='<tr>'+''.join(f'<td style="font-size:{size}px;line-height:1.2;padding:8px 14px;border-bottom:1px solid #cfc8b8;vertical-align:top{";font-weight:700" if j==0 else ""}">{e(c)}</td>' for j,c in enumerate(r))+'</tr>'
    return h+'</table>'
def part(i,n,title,lead,items,note):
    sections[f's{n}']={'description':f'Part {n}: {title}','start':i}
    write(i,f'<section id="{i}" data-transition="fade" style="background:{DARK};color:#f6f3ec;{BODY};padding:96px 128px;display:flex;flex-direction:column;justify-content:center">'
      f'<div style="display:flex;gap:80px;align-items:center;width:1664px"><div style="width:980px;display:flex;flex-direction:column;gap:28px"><p style="{FONT};font-size:40px;font-weight:700;letter-spacing:4px;color:#f0a46c">PART {n}</p>'
      f'<h1 style="{FONT};font-size:96px;font-weight:600;line-height:1.02;color:#f6f3ec">{e(title)}</h1><p style="font-size:34px;line-height:1.35;color:#c9d2de">{e(lead)}</p></div>'
      f'<div style="flex:1;border-left:4px solid #f0a46c;padding-left:40px"><ul style="font-size:30px;line-height:1.35;color:#f6f3ec;padding-left:30px;display:flex;flex-direction:column;gap:14px">'+''.join(f'<li>{e(x)}</li>' for x in items)+'</ul></div></div>'
      +foot(True)+notes(note)+'</section>')
def fig_full(i,kick,sub,title,k,h=700,source=None,note=''):
    write(i,sec_open(i)+head(kick,sub,title)+img(k,1664,h)+(src(source) if source else '')+foot()+notes(note)+'</section>')
def fig_side(i,kick,sub,title,k,bul,cards,source=None,note='',w=900,h=680):
    c=''.join(card(t,b,TOPS[j%4]) for j,(t,b) in enumerate(cards))
    write(i,sec_open(i)+head(kick,sub,title)+'<div style="display:flex;gap:44px;align-items:flex-start">'+img(k,w,h)
      +'<div style="flex:1;display:flex;flex-direction:column;gap:24px">'+ul(bul)+f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">{c}</div></div></div>'
      +(src(source) if source else '')+foot()+notes(note)+'</section>')
def twin(i,n,op,fr,de,title,kk,kt,kd,tk,tt,td,note):
    row=lambda lab,t,d,k: (f'<div style="display:flex;gap:32px;align-items:center"><div style="width:290px;display:flex;flex-direction:column;gap:8px">'
        f'<p style="font-size:24px;font-weight:700;letter-spacing:2px;color:{ORANGE if lab=="KITCHEN" else "#2f5f9e"}">{lab}</p>'
        f'<h3 style="{FONT};font-size:34px;font-weight:600;line-height:1.1">{e(t)}</h3><p style="font-size:24px;line-height:1.25;color:{GREY}">{e(d)}</p></div>'+img(k,1342,350)+'</div>')
    write(i,sec_open(i)+head(f'TRADITIONAL TECHNOLOGIES · CASE {n} OF 6',f'{op.upper()}',title)
      +row('KITCHEN',kt,kd,kk)+row('INDUSTRIAL TWIN',tt,td,tk)+foot()+notes(note+f' FR : {fr}. DE: {de}.')+'</section>')

# ---------------- cover
sections['s0']={'description':'Cover','start':'cover'}
write('cover',f'<section id="cover" data-transition="fade" style="background:{DARK};color:#f6f3ec;{BODY};padding:96px 128px;display:flex;flex-direction:column;justify-content:center">'
 f'<div style="display:flex;flex-direction:column;gap:32px;width:960px"><p style="font-size:24px;font-weight:600;letter-spacing:2px;color:#f0a46c">ADDITIVE MANUFACTURING · TECHNOLOGIES</p>'
 f'<h1 style="{FONT};font-size:112px;font-weight:600;line-height:1.02;color:#f6f3ec">AM technologies</h1>'
 '<p style="font-size:36px;line-height:1.35;color:#c9d2de">How things are made, from the kitchen to the factory, and how additive manufacturing makes them layer by layer: material paths, the morphological box, clocks, layer interfaces and the physics behind the design rules.</p>'
 '<p style="font-size:24px;color:#9fb0c4">Draft · November 2026</p></div>'
 f'<div style="position:absolute;right:128px;top:200px;width:600px;height:620px;background:#f6f3ec;border-radius:12px;padding:20px;display:flex;align-items:center;justify-content:center"><img src="/_blob/{A["f06"]}" alt="02_technologies/figures/{P["f06"]}.png" style="width:560px;height:580px;object-fit:contain"></div>'
 +notes('Chapter 02 of the EXED Polytechnique course. Structure after Gebhardt & Hötter, Additive Manufacturing (Hanser 2016), ch. 2; process taxonomy and drawing style after M. F. Ashby. FR : technologies de fabrication additive. DE: additive Fertigungsverfahren.')+'</section>')

# ---------------- part 1 traditional technologies
part('part-1',1,'Traditional technologies','What things are made of, the six ways of making them, in the kitchen and in the factory.',
 ['Materials through the ages','Shape created, changed, material changed','Six cases: kitchen and industrial twin','Temperature scales of treatments','Where the geometry is stored'],
 'Part 1 builds the vocabulary. DIN 8580 divides manufacturing into six main groups; each is shown first in the kitchen, then in its industrial twin, step by step.')
write('materials',sec_open('materials')+head('TRADITIONAL TECHNOLOGIES','MATERIALS','Every age has its materials, and its ways to shape them')
 +'<div style="display:flex;gap:44px;align-items:flex-start"><div style="width:1000px;height:680px;flex-shrink:0;border:2px dashed #9aa3ad;border-radius:12px;background:#e4e0d6;display:flex;flex-direction:column;gap:8px;align-items:center;justify-content:center;padding:14px">'
 '<p style="font-size:24px;color:#566170;text-align:center">[Picture: evolution of engineering materials with time]</p><p style="font-size:24px;color:#566170;text-align:center;font-style:italic">M. F. Ashby, Materials Selection in Mechanical Design</p><p style="font-size:24px;color:#566170;text-align:center">02_technologies/figures/02_ashby_materials_evolution.png</p></div>'
 '<div style="flex:1;display:flex;flex-direction:column;gap:16px">'+card('Metals','gold, copper, bronze, iron; then steels, light alloys, superalloys',TOPS[0])+card('Polymers and elastomers','wood, skins, fibres; then rubber, Bakelite, nylon, epoxies',TOPS[1])+card('Ceramics and glasses','stone, pottery, glass, cement; then technical ceramics',TOPS[2])+card('Composites','straw-brick, paper; then GFRP, CFRP, metal- and ceramic-matrix',TOPS[3])+'</div></div>'
 +src('Source: M. F. Ashby, Materials Selection in Mechanical Design, Butterworth-Heinemann (picture: licence to check).')+foot()
 +notes('Ashby\'s chart of the relative importance of the four material families from 10 000 BC to 2020. Picture not in the public repository until the licence is checked. FR : métaux, polymères et élastomères, céramiques et verres, composites. DE: Metalle, Polymere und Elastomere, Keramiken und Gläser, Verbundwerkstoffe.')+'</section>')
fig_full('groups','TRADITIONAL TECHNOLOGIES','DIN 8580','Six ways of making','a01n',h=640,
 source='After DIN 8580 and M. F. Ashby, Materials Selection in Mechanical Design, 5th ed., 2016, ch. 6.',
 note='DIN 8580 main groups and cohesion: primary shaping creates it, forming keeps it, separating reduces it, joining and coating increase it, changing properties rearranges atoms. FR : mise en forme primaire, formage, séparation, assemblage, revêtement, modification des propriétés. DE: Urformen, Umformen, Trennen, Fügen, Beschichten, Stoffeigenschaft ändern.')
fig_full('convention','TRADITIONAL TECHNOLOGIES','READING THE DRAWINGS','One colour code for every drawing in this chapter','a00',h=600,
 note='Kitchen materials pale yellow (initial) and blue (final); industrial materials orange (initial) and slate (final). Moulds hatched, other tools grey, carrier fluids pale cyan; force dark arrows, heat orange waves, radiation magenta, electricity blue, chemistry green.')
cases=[
 ('case-1','primary shaping','mise en forme primaire','Urformen','Primary shaping: a mould gives the shape, then the material sets','b01','A cake in a tin','batter (liquid) sets in the oven','g01','Sand casting','molten metal fills a sand mould and solidifies',
  'The tin and the sand mould carry the shape; heat sets the batter, cooling solidifies the metal. Risers feed the solidification shrinkage. Reference: Ashby, Shercliff & Cebon, Materials, 3rd ed., 2013, ch. 18.'),
 ('case-2','forming','formage','Umformen','Forming: the same material takes a new shape, still in one piece','b02','Rolling the dough','force spreads the ball into a sheet','g07','Sheet rolling','a hot slab passes between rolls and leaves as a thin strip',
  'Mass and cohesion are kept; the roll gap sets the thickness. Hot rolling of steel at about 1100–1250 °C, then cold rolling for thin sheet and finish. The rolling pin and the roll stand are the same operation. Closed-die forging is another forming twin.'),
 ('case-3','separating','séparation, usinage','Trennen, Spanen','Separating: material is removed until the part remains','b03','Slicing bread','the knife removes crumbs between slices','g03','Milling','a rotating tool removes chips from a clamped stock',
  'Cohesion is reduced. The geometry is stored in the tool path (a CNC program), as it will be in AM. Buy-to-fly ratios of aerospace parts can reach 10–20.'),
 ('case-4','joining','assemblage','Fügen','Joining: two parts become one assembly','b04','Gingerbread walls','icing glues the walls and dries','g04','Arc welding','an arc melts the wire and the groove edges into one weld',
  'Cohesion is increased between parts. The weld pool, the heat-affected zone and the residual stress are the physics of metal AM (DED, PBF).'),
 ('case-5','coating','revêtement','Beschichten','Coating: the part keeps its shape and gains a new surface','b05','Glazing a cake','a warm glaze spreads into a thin layer','g05','Thermal spraying','molten droplets flatten into splats on a grit-blasted part',
  'A layer is added on a part. Thermal spraying (plasma, flame, HVOF) builds coatings splat by splat; cold spray does it with solid particles and becomes an AM process.'),
 ('case-6','changing properties','modification des propriétés, traitement thermique','Stoffeigenschaft ändern, Wärmebehandlung','Changing properties: the shape stays, the material changes inside','b06','Boiling an egg','proteins unfold and bond at 100 °C','g06','Quench hardening of steel','austenitise, quench to martensite, temper',
  'The shape is kept, the microstructure changes. Steel: about 850 °C (austenite), water quench (martensite, hard and brittle), tempering at 200–600 °C (hard and tough). Later: the kitchen parallel will extend to a material twin of heterogeneous, fibrous and crystalline materials.'),
]
for n,(i,op,fr,de,t,kk,kt,kd,tk,tt,td,note) in enumerate(cases,1): twin(i,n,op,fr,de,t,kk,kt,kd,tk,tt,td,note)
fig_full('heat-scales','TRADITIONAL TECHNOLOGIES','CHANGING PROPERTIES','Material Processes temperature and time','c07n',h=680,
 source='Typical ranges after Ashby, Shercliff & Cebon, Materials, 3rd ed., 2013, ch. 19; ASTM F3301 (thermal post-processing of PBF metal parts).',
 note='Egg 60–100 °C: protein denaturation. Curing of thermosets 120–180 °C: cross-linking. Tempering 150–650 °C: carbide precipitation. Quench hardening ≈ 850 °C then quench: martensite. Stress relief of AM parts 600–900 °C: recovery. HIP 900–1250 °C at 100–200 MPa: creep and diffusion close pores. FR : trempe, revenu, détensionnement, CIC. DE: Härten, Anlassen, Spannungsarmglühen, HIP.')
fig_full('hip','TRADITIONAL TECHNOLOGIES','CHANGING PROPERTIES · HIP','Hot isostatic pressing: hot argon squeezes the part until its pores close','c10',h=680,
 source='After ASTM F3301 and H. V. Atkinson, B. A. Rickinson, Hot Isostatic Processing, Adam Hilger, 1991.',
 note='HIP: parts are loaded in a steel pressure vessel with a furnace inside; argon at 100–200 MPa and 900–1250 °C (Ti-6Al-4V ≈ 920 °C, Ni superalloys ≈ 1160–1200 °C) for 2–4 h. The gas pressure acts equally on every face, so the shape is kept while internal pores close by creep and diffusion bonding. Surface-connected pores do not close. Standard step for fatigue-critical PBF parts. FR : compression isostatique à chaud (CIC). DE: heißisostatisches Pressen (HIP).')
fig_side('ashby-tree','TRADITIONAL TECHNOLOGIES','ASHBY','Ashby sorts processes like living things: kingdom, family, class, member','c00',
 ['Three families: shaping, joining, surface treatment','Additive manufacturing is one class of shaping','Each member carries attributes for selection'],
 [('Kingdom','all processes'),('Family','shaping, joining, surface'),('Class','casting, moulding, deformation…'),('Attributes','material, size, tolerance, batch')],
 source='M. F. Ashby, Materials Selection in Mechanical Design, 5th ed., Butterworth-Heinemann, 2016, ch. 6–7.',
 note='Ashby\'s taxonomy is the basis of process selection charts (size, tolerance, roughness, economic batch). FR : mise en forme, assemblage, traitement de surface. DE: Formgebung, Fügen, Oberflächenbehandlung.')
fig_side('injection','TRADITIONAL TECHNOLOGIES','PRIMARY SHAPING FROM THE PLASTIC STATE','Injection moulding pushes a melt into a steel mould, seconds per part','c02',
 ['Pellets melt in a heated barrel','A screw injects, the mould cools the part','Moulds are costly: large batches only'],
 [('Starting state','plastic (polymer melt)'),('Tool','steel mould, reused'),('AM twin','material extrusion'),('Batch','thousands to millions')],
 note='Twin of material extrusion (FFF, pellet extrusion). FR : moulage par injection. DE: Spritzgießen.')
fig_side('pm','TRADITIONAL TECHNOLOGIES','PRIMARY SHAPING FROM POWDER','Powder metallurgy: press the powder into a die, then sinter it','c08',
 ['Die compaction gives a green part','Sintering bonds grains by diffusion below the melting point','The part shrinks; tolerances allow for it'],
 [('Starting state','granular or powder'),('Tool','die and punches'),('AM twin','binder jetting + sintering'),('Shrinkage','10–20 % linear')],
 note='FR : métallurgie des poudres, compactage, frittage. DE: Pulvermetallurgie, Pressen, Sintern.')
fig_full('geometry','TRADITIONAL TECHNOLOGIES','FROM THE TOOL TO THE FILE','The geometry lives in a mould, a die, a tool path or a layer file','c09',h=560,
 note='Casting and forging store the shape in tooling: expensive, so many identical parts. Machining and AM store it in a program: each part can differ. FR : outillage, programme, fichier. DE: Werkzeug, Programm, Datei.')

# ---------------- part 2 AM as layer-wise primary shaping
part('part-2',2,'AM process: polymers','Every AM process is an old primary-shaping process, made selective and layer by layer.',
 ['Shape, layer, path, voxel','Ways of making × material paths','Seven starting states, seven twins','Four material paths','Eleven processes and their twins'],
 'DIN 8580 sorts primary shaping by the state of the starting material; AM follows the same logic.')
def two_figs(i,kick,sub,title,k1,cap1,w1,h1,k2,cap2,w2,h2,source=None,note=''):
    def col(k,cap,w,h):
        return (f'<div style="display:flex;flex-direction:column;gap:12px;width:{w}px"><p style="font-size:30px;font-weight:700;color:{ORANGE}">{e(cap)}</p>'
                f'<div style="width:{w}px;height:{h}px;background:#ffffff;border:1px solid #ddd6c6;border-radius:12px;padding:12px;display:flex;align-items:center;justify-content:center">'
                f'<img src="/_blob/{A[k]}" alt="02_technologies/figures/{P[k]}.png" style="width:{w-26}px;height:{h-26}px;object-fit:contain"></div></div>')
    write(i,sec_open(i)+head(kick,sub,title)+'<div style="display:flex;gap:40px;align-items:flex-start">'+col(k1,cap1,w1,h1)+col(k2,cap2,w2,h2)+'</div>'
      +(src(source) if source else '')+foot()+notes(note)+'</section>')
def figbox(k,w,h):
    return (f'<div style="width:{w}px;height:{h}px;flex-shrink:0;background:#ffffff;border:1px solid #ddd6c6;border-radius:12px;padding:12px;display:flex;align-items:center;justify-content:center">'
            f'<img src="/_blob/{A[k]}" alt="02_technologies/figures/{P[k]}.png" style="width:{w-26}px;height:{h-26}px;object-fit:contain"></div>')
write('shape-process',sec_open('shape-process')+head('AM PROCESS','SHAPE AND PROCESS','AM is a shape and a process')
 +'<div style="display:flex;gap:40px;align-items:flex-start">'
 +f'<div style="width:1070px;display:flex;flex-direction:column;gap:14px"><p style="font-size:30px;font-weight:700;color:{ORANGE}">Shape · part: from voxel to path to layer to part</p>'+figbox('d01n',1070,400)
 +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+card('Shape: digital CAD file','NURBS surfaces carried by control points; exported as a mesh for the printer',TOPS[0])+card('Printing strategy','layers of thickness Δz, paths (contour + hatching), voxels (spot × track × Δz)',TOPS[1])+'</div></div>'
 +f'<div style="flex:1;display:flex;flex-direction:column;gap:14px"><p style="font-size:30px;font-weight:700;color:{ORANGE}">Process · the material path</p>'+figbox('e05',554,610)+'</div></div>'
 +src('Paths after Kruth (1991), Gebhardt & Hötter (2016) §2.3, Kruth et al. (2005), Tuncer & Bose (2020).')+foot()
 +notes('The part is no longer stored in a mould but in a file: the CAD shape is sliced into layers, the layers into paths, the paths into voxels. Process: four physical paths from the initial to the final material. Examples, not on the slide: liquid → solid: VPP, MJT, concrete, paste extrusion; solid → liquid → solid: PBF, DED, wire-arc, FFF (softening); solid → solid: binder jetting, LOM, cold spray, friction stir, ultrasonic AM; gas or ions → solid: laser CVD, electrochemical AM. FR : forme, couche, trajectoire, voxel, stratégie d’impression. DE: Form, Schicht, Bahn, Voxel, Druckstrategie.')+'</section>')
fig_full('groups-paths','AM PROCESS','WAYS OF MAKING × MATERIAL PATHS','Which material path serves which way of making','e04',h=660,
 source='Main groups: DIN 8580:2022, Fertigungsverfahren — Begriffe, Einteilung (Beuth). Paths: Kruth (1991); Gebhardt & Hötter (2016) §2.3.',
 note='Columns: the six DIN 8580 main groups of slide 4. Rows: the four material paths of the previous slide. First row: cohesion, as on slide 4 (created, increased, atoms rearranged in red). A dot marks where a path is used. Liquid → solid: shaping (casting, VPP, MJT), joining (gluing), properties (curing). Solid → liquid → solid: shaping (PBF, DED), joining (welding), coating (thermal spraying). Solid → solid: coating (cold spray); open circle: shaping by sintering or binder jetting, to confirm. Gas or ions → solid: left open (CVD, PVD, laser CVD, electroforming).')
am=[('vpp','f02','VAT PHOTOPOLYMERISATION (VPP)','Vat photopolymerisation is resin casting, one spot or one layer at a time',['Liquid monomers polymerise under UV light','Laser spot (SLA) or projected mask (DLP)','Layers 25–100 µm, fine detail'],[('Starting state','liquid'),('Twin','resin casting'),('Agent','light'),('Addressing','point or area')],'FR : photopolymérisation en cuve. DE: badbasierte Photopolymerisation.'),
 ('mjt','f04','MATERIAL JETTING (MJT)','Material jetting places droplets that cure where they land',['A print head jets resin droplets','A UV lamp cures each pass','Several materials, gel supports'],[('Starting state','liquid'),('Twin','inkjet printing, casting'),('Agent','light'),('Addressing','line')],'FR : projection de matière. DE: Freistrahl-Materialauftrag.'),
 ('mex','f03','MATERIAL EXTRUSION (MEX)','Material extrusion is injection moulding without a mould',['A filament melts in a hot end','The nozzle lays roads that weld to the layer below','Weak point: the bond between layers'],[('Starting state','plastic'),('Twin','injection moulding'),('Agent','heat'),('Addressing','point')],'FR : extrusion de matière. DE: Materialextrusion.'),
 ('paste','f12','PASTE EXTRUSION (MEX)','Paste extrusion builds slip and concrete bead by bead',['A paste flows in the nozzle and stands on the stack','Ceramics dry and are fired','Concrete sets by hydration'],[('Starting state','pasty'),('Twin','slip and concrete casting'),('Agent','drying, hydration'),('Addressing','point')],'FR : extrusion de pâte, impression béton. DE: Pastenextrusion, Betondruck.'),
 ('pbf','f06','POWDER BED FUSION (PBF)','Powder bed fusion is welding and casting, layer by layer',['A recoater spreads 20–100 µm of powder','A laser or electron beam melts the section','Melt pool, fast solidification, residual stress'],[('Starting state','powder'),('Twin','welding, casting'),('Agent','laser or electrons'),('Addressing','point')],'FR : fusion sur lit de poudre. DE: pulverbettbasiertes Schmelzen.'),
 ('ded','f07','DIRECTED ENERGY DEPOSITION (DED)','Directed energy deposition is a welding torch that builds',['Powder or wire fed into a melt pool','Laser, arc or electron beam','Large parts and repair, then machining'],[('Starting state','powder or wire'),('Twin','cladding, welding'),('Agent','laser, arc, electrons'),('Addressing','point')],'FR : dépôt sous énergie concentrée. DE: gerichtete Energieeinbringung.'),
 ('shl','f08','SHEET LAMINATION (SHL)','Sheet lamination cuts each sheet and glues it to the stack',['Paper, polymer or metal sheets','A laser or knife cuts the contour','Ultrasonic AM welds metal foils in the solid state'],[('Starting state','sheets (fibres)'),('Twin','lamination, gluing'),('Agent','glue, ultrasound'),('Addressing','point')],'FR : stratification de couches. DE: Schichtlaminierung.'),
 ('cold','f09','COLD SPRAY','Cold spray is thermal spraying without melting',['Particles reach 500–1200 m/s in a gas jet','They deform and bond in the solid state','Little oxidation; repair of Al and Mg parts'],[('Starting state','powder'),('Twin','thermal spraying'),('Agent','kinetic energy'),('Addressing','point')],'FR : projection à froid. DE: Kaltgasspritzen.'),
 ('lcvd','f10','LASER CVD','Laser CVD is chemical vapour deposition at one hot spot',['A precursor gas decomposes on a hot surface','The laser heats one spot only','Fibres and rods of C, SiC, W'],[('Starting state','gas'),('Twin','CVD'),('Agent','laser heat'),('Addressing','point')],'FR : dépôt chimique en phase vapeur assisté par laser. DE: laserunterstützte Gasphasenabscheidung.'),
 ('ecam','f11','ELECTROCHEMICAL AM','Electrochemical AM is electroforming under a moving nozzle',['Metal ions are reduced on a cathode','A micro-nozzle confines the reaction','Cu, Ni at room temperature, µm features'],[('Starting state','ionised'),('Twin','electroforming'),('Agent','electric current'),('Addressing','point')],'FR : fabrication additive électrochimique, électroformage. DE: elektrochemische additive Fertigung, Galvanoformung.')]
for i,k,kick,t,b,c,n in am[:1]: fig_side(i,'AM PROCESS',kick,t,k,b,c,note=n)
# ---------- photopolymerisation block
def gif(k,alt,cap,sub,sites,credit=None,w=528,h=300):
    return (f'<div style="display:flex;flex-direction:column;gap:6px;width:{w}px">'
            f'<div style="width:{w}px;height:{h}px;background:#ffffff;border:1px solid #ddd6c6;border-radius:12px;padding:8px;display:flex;align-items:center;justify-content:center">'
            f'<img src="/_blob/{A[k]}" alt="{alt}" style="width:{w-18}px;height:{h-18}px;object-fit:contain"></div>'
            +(f'<p style="font-size:24px;color:{GREY};font-style:italic">{e(credit)}</p>' if credit else '')
            +f'<p style="font-size:30px;font-weight:700;color:{INK}">{e(cap)}</p><p style="font-size:24px;line-height:1.2;color:{GREY}">{e(sub)}</p>'
            f'<p style="font-size:24px;line-height:1.2;color:#2f5f9e">{e(sites)}</p></div>')
def params(title,rows,c):
    body=''.join(f'<p style="font-size:24px;line-height:1.2"><b>{e(a)}</b> {e(b)}</p>' for a,b in rows)
    return (f'<div style="display:flex;flex-direction:column;gap:4px;background:#fbfaf7;border:1px solid #ddd6c6;border-top:5px solid {c};border-radius:12px;padding:12px 18px">'
            f'<p style="font-size:24px;font-weight:700;color:{c}">{e(title)}</p>{body}</div>')
write('photopoly',sec_open('photopoly','48px 128px 100px')+head('AM PROCESS','PHOTOPOLYMERISATION','Photopolymerisation: one physics, three technologies')
 +'<div style="display:flex;gap:40px;justify-content:space-between">'
 +gif('h01','02_technologies/figures/02_h01_sla_animation.gif','SLA','A UV laser spot traces each layer.','formlabs.com · 3dsystems.com · uniontech3d.com')
 +gif('h02','02_technologies/figures/02_h02_dlp_animation.gif','DLP / MSLA','The whole layer is lit at once.','asiga.com · carbon3d.com · stratasys.com · prusa3d.com · elegoo.com · bmf3d.com')
 +gif('h03','02_technologies/figures/02_h03_mpp_animation.gif','Multi-photon','A femtosecond focus cures inside the resin.','nanoscribe.com · upnano.com · microlight3d.com · femtika.lt',credit='Animation: Femtika (femtika.lt)')
 +'</div>'
 +'<div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:40px">'
 +params('Process parameters',[('Voxel','25–150 µm laser spot'),('Build volume','1–300 L'),('Writing','scan 1–10 m/s, 10–20 mm/h'),('Light','UV laser 355 or 405 nm, 0.25–2 W')],TOPS[0])
 +params('Process parameters',[('Voxel','20–75 µm pixel (micro-DLP 2–10 µm)'),('Build volume','0.2–50 L'),('Writing','20–100 mm/h, one flash per layer'),('Light','UV LED 385 or 405 nm, 5–20 mW/cm²')],TOPS[1])
 +params('Process parameters',[('Voxel','0.1–1 µm'),('Build volume','0.001–0.6 L'),('Writing','0.1–1.2 m/s, up to ≈ 450 mm³/h'),('Light','fs laser 780 or 515 nm, 0.1–1 W')],TOPS[2])
 +'</div>'+src('Typical ranges from the makers\' data sheets (to verify); see tables/02_printers_price_voxel.csv.')+foot()
 +notes('One physics: a photo-initiator absorbs light and starts the cross-linking of the monomer, the liquid becomes a solid. Three technologies: SLA (Hull 1986) scans a UV laser spot with galvanometer mirrors; DLP and MSLA project a whole layer through a micromirror chip or an LCD mask; Carbon CLIP/DLS adds an oxygen-permeable window for continuous pull. Multi-photon (2PP/MPP): absorption ∝ I², so only the focus of a femtosecond near-IR laser cures, voxel below 1 µm and no layer needed. Ranges indicative: Form 3L 2 × 250 mW lasers; SLA 750 beam 125–1000 µm; Form 4 up to 100 mm/h; UpNano 150–1200 mm/s and > 450 mm³/h; Nanoscribe Quantum X 50 × 50 × 20 mm. SLA and DLP animations: own drawings; multi-photon animation: Femtika. FR : photopolymérisation, stéréolithographie, polymérisation à deux photons. DE: Photopolymerisation, Stereolithografie, Zwei-Photonen-Polymerisation.')+'</section>')
# Carbon CLIP example (first example)
TL=[('2015','CLIP in Science; Carbon launched (TED talk)'),('2017','adidas Futurecraft 4D lattice midsole'),('2019–20','Riddell helmet liners; Specialized, fizik saddles'),('2022','M3 and M3 Max printers'),('2024–25','EPU Pro; FP3D dual-cure denture resin; $60M raise'),('2026','DB 4000 denture resin; DDK saddles; Arkema partnership; dual-cure patent upheld at the EPO')]
tl=''.join(f'<div style="display:flex;gap:14px;align-items:baseline"><p style="width:110px;flex-shrink:0;font-size:24px;font-weight:700;color:{ORANGE}">{e(y)}</p><p style="font-size:24px;line-height:1.2">{e(t)}</p></div>' for y,t in TL)
write('vpp-example-carbon',sec_open('vpp-example-carbon','48px 128px 100px')+head('EXAMPLE · PHOTOPOLYMERISATION','CLIP / DLS · CARBON','Carbon CLIP: the part is pulled continuously out of the resin')
 +'<div style="display:flex;gap:40px;align-items:flex-start">'
 +'<div style="width:700px;flex-shrink:0;display:flex;flex-direction:column;gap:10px">'
 +f'<div style="width:700px;height:394px;background:#0f1b2d;border-radius:12px;overflow:hidden"><img src="/_blob/{A["carbon"]}" alt="02_technologies/figures/02_h04_carbon_clip_animation.gif" style="width:700px;height:394px;object-fit:cover"></div>'
 +f'<p style="font-size:24px;color:{GREY};font-style:italic">Animation: Carbon, Inc. (carbon3d.com), 7× speed; CLIP after Tumbleston et al. 2015¹, Zastrow 2020²</p>'
 +f'<div style="display:flex;flex-direction:column;gap:6px">{tl}</div></div>'
 +'<div style="flex:1;display:flex;flex-direction:column;gap:20px">'
 +ul(['An oxygen-permeable window keeps a thin “dead zone” of liquid resin: no layer peeling, the platform rises continuously¹','Up to 100 times faster than earlier resin printers²','Dual-cure resins: UV light shapes, an oven bake gives engineering properties (EPU, RPU, EPX)'],26)
 +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+card('Company','Carbon, Redwood City (CA); co-founded by J. DeSimone, UNC',TOPS[0])+card('Printer / process','CLIP / DLS; M3, M3 Max, L1',TOPS[1])+card('Gains','speed, near-isotropic parts, lattices: 140 000 struts per Riddell liner',TOPS[2])+card('Problems / challenges','subscription model, mostly proprietary resins, oven step',TOPS[3])+'</div></div></div>'
 +src('¹ J. R. Tumbleston et al., Continuous liquid interface production of 3D objects, Science 347, 1349–1352 (2015). ² M. Zastrow, The new 3D printing, Nature 578, 20–23 (2020).')+foot()
 +notes('CLIP (continuous liquid interface production), sold as Carbon DLS (Digital Light Synthesis): a DLP projector cures through an oxygen-permeable window; oxygen inhibits the radical polymerisation in a dead zone a few tens of µm thick, so the part never sticks to the window and can be pulled continuously. Zastrow (Nature 2020): Carbon raised US$680 million and was valued at about US$2.4 billion; contracts with adidas (midsoles) and Riddell (helmet padding); follow-ups HARP (Azul 3D, Mirkin, Science 366, 2019) and dual-wavelength photo-inhibition (de Beer et al., Sci. Adv. 2019). Since then: $60M raise (Nov 2025; Sequoia, Silver Lake, adidas…); 6 of the top 10 of the 2025 Tour de France on Carbon-made saddles; fizik, Selle Italia and Trek saddles in hundreds of thousands; dental customers print millions of custom parts per week; FP3D flexible partial denture resin (2025), DB 4000 denture base resin (Aug 2026), DDK saddle partnership (May 2026), Arkema partnership (Nov 2026), dual-cure patent upheld by the EPO (Sep 2026). Sources: carbon3d.com press releases; voxelmatters.com (14 Nov 2025); Carbon lattice white paper. Animation: Carbon, Inc. (carbon3d.com), in the repository as 02_technologies/figures/02_h04_carbon_clip_animation.gif; process: Tumbleston et al., Science 347, 1349–1352 (2015), doi:10.1126/science.aaa2397, reference 3 of Zastrow, Nature 578, 20–23 (2020), doi:10.1038/d41586-020-00271-6. FR : production continue à interface liquide. DE: kontinuierliche Flüssigkeitsgrenzflächen-Produktion.')+'</section>')
# void example slide (aviation layout), to complete later
write('vpp-example-template',sec_open('vpp-example-template')+head('EXAMPLE · PHOTOPOLYMERISATION','TECHNOLOGY · MATERIAL','[Example to complete: part, company, what was gained]')
 +'<div style="display:flex;gap:44px;align-items:flex-start"><div style="width:680px;height:660px;flex-shrink:0;border:2px dashed #9aa3ad;border-radius:12px;background:#e4e0d6;display:flex;flex-direction:column;gap:8px;align-items:center;justify-content:center;padding:14px">'
 '<p style="font-size:24px;color:#566170;text-align:center;line-height:1.2">[Picture: example part]</p><p style="font-size:24px;color:#566170;text-align:center;line-height:1.2;font-style:italic">source › page › title</p></div>'
 '<div style="flex:1;display:flex;flex-direction:column;gap:24px">'+ul(['[What the part does]','[Why photopolymerisation: detail, surface, speed]','[Key figure: voxel, series size, time]'])
 +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">'+card('Company','[to complete]',TOPS[0])+card('Printer / process','[to complete]',TOPS[1])+card('Gains','[to complete]',TOPS[2])+card('Problems / challenges','[to complete]',TOPS[3])+'</div></div></div>'
 +src('Source: [to complete]')+foot()+notes('Template slide for application examples, same layout as the AM in aviation examples. Duplicate for each example.')+'</section>')
# the two price charts
def chart(k,cap,w=816,h=540):
    return (f'<div style="display:flex;flex-direction:column;gap:10px;width:{w}px"><div style="width:{w}px;height:{h}px;background:#ffffff;border:1px solid #ddd6c6;border-radius:12px;padding:10px;display:flex;align-items:center;justify-content:center">'
            f'<img src="/_blob/{A[k]}" alt="02_technologies/figures/{P[k]}.png" style="width:{w-22}px;height:{h-22}px;object-fit:contain"></div>'
            f'<p style="font-size:26px;line-height:1.25;color:{INK}">{e(cap)}</p></div>')
write('vpp-prices',sec_open('vpp-prices')+head('MACHINES AND PRICES','PHOTOPOLYMER PRINTERS','Finer voxels and larger volumes both cost: from 500 $ to 500 000 $')
 +'<div style="display:flex;gap:32px">'+chart('i01','Price vs voxel size: four orders of magnitude in voxel, three in price.')+chart('i03','Price vs build volume: price per litre from about 100 $ (desktop MSLA) to 10⁸ $ (two-photon).')+'</div>'
 +src('List and launch prices 2019–2025 from vendors, dealers, all3dp and aniwaa; Carbon: 3-year subscription totals. Data: 02_technologies/tables/02_printers_price_voxel.csv.')+foot()
 +notes('Ashby-style charts: one colour per technology (2PP/MPP, PµSL, DLP, MSLA, CLIP/DLS, laser SLA), bubbles are technology envelopes; dashed lines in the right chart are constant price per litre of build volume. Price on request: UpNano NanoOne, Nano Dimension Fabrica Tera. Femtika (≈ 415 k$) not in the volume chart, build volume depends on the stage. Carbon M3, M3 Max and L1 prices come from competitors\' comparison pages: least reliable points.')+'</section>')
# makers map, aviation layout
TC={'2PP / MPP':'#2a78d6','PµSL (micro-DLP)':'#eb6834','DLP':'#1baf7a','MSLA (LCD)':'#008300','CLIP / DLS':'#eda100','laser SLA':'#e87ba4'}
WORLD=[(1,'Carbon','Redwood City, US','CLIP / DLS',['CLIP / DLS']),(2,'Formlabs','Somerville, US','MSLA + laser SLA',['MSLA (LCD)','laser SLA']),(3,'3D Systems','Rock Hill, US','laser SLA',['laser SLA']),(4,'Stratasys','Eden Prairie, US / Rehovot, IL','DLP (P3)',['DLP']),(5,'BMF','Shenzhen, China','micro-DLP (PµSL)',['PµSL (micro-DLP)']),(6,'Elegoo','Shenzhen, China','MSLA',['MSLA (LCD)']),(7,'UnionTech','Shanghai, China','laser SLA',['laser SLA']),(8,'Asiga','Sydney, Australia','DLP',['DLP'])]
def ring(n,c,sz=34): return f'<div style="width:{sz}px;height:{sz}px;flex-shrink:0;border-radius:{sz//2}px;background:#fbfaf7;border:3px solid {c};display:flex;align-items:center;justify-content:center"><p style="font-size:22px;font-weight:700;color:{c};line-height:1">{n}</p></div>'
items=''.join(f'<div style="display:flex;gap:8px;align-items:flex-start;width:505px">'+''.join(ring(n,TC[t]) for t in ts)+f'<p style="font-size:24px;line-height:1.2"><b>{e(nm)}</b> · {e(city)} · {e(tech)}</p></div>' for n,nm,city,tech,ts in WORLD)
key=''.join(f'<div style="display:flex;gap:8px;align-items:center"><div style="width:22px;height:22px;border-radius:11px;background:#fbfaf7;border:3px solid {c}"></div><p style="font-size:24px">{e(t)}</p></div>' for t,c in TC.items())
write('vpp-makers','<section id="vpp-makers" data-transition="fade" style="background:#f3f1ec;color:#1b2433;font-family:Inter, Arial, sans-serif;padding:48px 128px 96px;display:flex;flex-direction:column;gap:14px">'
 +f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;color:#a8480f">WHERE PHOTOPOLYMER PRINTERS COME FROM</p><h2 style="{FONT};font-size:60px;font-weight:600;line-height:1.08;color:#1b2433">Photopolymer printer makers worldwide</h2>'
 +'<div style="display:flex;gap:24px;align-items:flex-start"><div style="width:1040px;display:flex;flex-direction:column;gap:16px">'
 +f'<img src="/_blob/{A["i04w"]}" alt="02_technologies/figures/{P["i04w"]}.png" style="width:1040px;height:326px;border-radius:12px;flex-shrink:0">'
 +f'<div style="display:flex;flex-wrap:wrap;gap:10px 30px">{items}</div><div style="display:flex;flex-wrap:wrap;gap:8px 24px">{key}</div></div>'
 +f'<div style="flex:1;display:flex;flex-direction:column;gap:10px"><img src="/_blob/{A["i04e"]}" alt="02_technologies/figures/{P["i04e"]}.png" style="width:600px;height:705px;border-radius:12px;flex-shrink:0"><p style="font-size:24px;color:#566170">Europe and Israel in detail</p></div></div>'
 +src('Ring colour = technology. Two-photon makers are all European: Nanoscribe (Karlsruhe), UpNano (Vienna), Microlight3D (Grenoble), Femtika (Vilnius).')+foot()
 +notes('Head offices from the vendors\' sites; coastlines Natural Earth (public domain). Co-located Shenzhen makers (BMF, Elegoo) drawn with leader lines. Stratasys is US–Israeli; Nano Dimension (ex Nanofabrica) is in Ness Ziona, Israel. Data: 02_technologies/tables/02_printers_price_voxel.csv.')+'</section>')
# ---------- polymers block
fig_full('poly-pyramid','POLYMERS','PRINTABLE THERMOPLASTICS','The higher the service temperature, the fewer the printable grades','j01',h=660,
 source='After BCG, exhibit "A wide variety of plastics can be used for AM". List not exhaustive.',
 note='Commodity (< 100 °C), engineering (100–150 °C) and high-temperature (> 150 °C) thermoplastics. Amorphous polymers soften gradually and print well as filament; semicrystalline polymers melt sharply and also suit powder bed fusion (PA 11, PA 12, PEEK, PEKK). The base is where conventional production volumes, and low prices, are. FR : thermoplastiques amorphes et semi-cristallins, température d’utilisation continue. DE: amorphe und teilkristalline Thermoplaste, Dauergebrauchstemperatur.')
fig_full('poly-ashby','POLYMERS','ASHBY CHART','Printable polymers: nine decades of stiffness','j02',h=770,
 note='Modulus vs tensile strength replaces the modulus–density chart: polymer densities only span 0.9–1.5 g/cm³. Ellipses span published ranges; colour = process (2PP/MPP, VPP, MEX, PBF). Dashed lines: constant strain σ/E, elastomers near 100 %, rigid polymers 1–5 %. 2PP resins (IP-S, IP-Dip, SU-8) sit with the stiffest unreinforced polymers; IP-PDMS and PEGDA hydrogels extend the chart to soft tissue. Sources: combined Ashby table (PDF), EOS PA 2200, Prusament PLA/PETG, Formlabs Standard, BASF Ultrafuse, Kayaku SU-8, Nanoscribe IP-PDMS, PMC6070906, Adv. Eng. Mater. 2025, Ashby 2016. Data: tables/02_polymers_ashby.csv.')
fig_full('poly-prices','POLYMERS','FEEDSTOCK PRICES','From 10 $/kg for PLA filament to 700 $/kg for PEEK filament','j03',h=640,
 source='Retail and bulk prices 2025–2026 (Prusa, Formlabs, Sinterit, Fiberlogy, SABIC resellers, all3dp, Fabbaloo, CNC Kitchen); data: tables/02_polymer_prices_makers.csv.',
 note='Feedstock costs 5 to 30 times the bulk pellet price (PA 12 pellets ≈ 18–22 $/kg): drying, filament extrusion, powder milling and qualification, small batches. Resins converted at 1.1 kg/L. 2PP photoresins (IP-S, OrmoComp, SU-8) come in small bottles on quote.')
RC={'base polymer':'#566170','filament':'#eb6834','powder':'#eda100','resin':'#1baf7a','2PP resin':'#2a78d6'}
PW=[(1,'NatureWorks','Minnesota, US','PLA (Ingeo)','base polymer'),(2,'Lubrizol','Ohio, US','TPU (Estane)','base polymer'),(3,'Formlabs','Somerville, US','resins 30–170 $/L, PA powder ≥ 45 $/kg','resin'),(4,'Kayaku AM','Massachusetts, US','SU-8 photoresist','2PP resin'),(5,'SABIC','Riyadh, Saudi Arabia','PEI (ULTEM), filament 230–340 €/kg','base polymer'),(6,'Polymaker','Jiangsu, China','filaments (PolyLite, PolyMax)','filament'),(7,'eSUN','Shenzhen, China','filaments, incl. PEEK','filament')]
pitems=''.join(f'<div style="display:flex;gap:8px;align-items:flex-start;width:505px">'+ring(n,RC[r])+f'<p style="font-size:24px;line-height:1.2"><b>{e(nm)}</b> · {e(city)} · {e(what)}</p></div>' for n,nm,city,what,r in PW)
pkey=''.join(f'<div style="display:flex;gap:8px;align-items:center"><div style="width:22px;height:22px;border-radius:11px;background:#fbfaf7;border:3px solid {c}"></div><p style="font-size:24px">{e(t)}</p></div>' for t,c in RC.items())
write('poly-makers','<section id="poly-makers" data-transition="fade" style="background:#f3f1ec;color:#1b2433;font-family:Inter, Arial, sans-serif;padding:48px 128px 96px;display:flex;flex-direction:column;gap:14px">'
 +f'<p style="font-size:24px;font-weight:600;letter-spacing:2px;color:#a8480f">WHERE PRINTABLE POLYMERS COME FROM</p><h2 style="{FONT};font-size:60px;font-weight:600;line-height:1.08;color:#1b2433">Polymer and feedstock makers worldwide</h2>'
 +'<div style="display:flex;gap:24px;align-items:flex-start"><div style="width:1040px;display:flex;flex-direction:column;gap:16px">'
 +f'<img src="/_blob/{A["j04w"]}" alt="02_technologies/figures/{P["j04w"]}.png" style="width:1040px;height:326px;border-radius:12px;flex-shrink:0">'
 +f'<div style="display:flex;flex-wrap:wrap;gap:10px 30px">{pitems}</div><div style="display:flex;flex-wrap:wrap;gap:8px 24px">{pkey}</div></div>'
 +f'<div style="flex:1;display:flex;flex-direction:column;gap:10px"><img src="/_blob/{A["j04e"]}" alt="02_technologies/figures/{P["j04e"]}.png" style="width:600px;height:705px;border-radius:12px;flex-shrink:0"><p style="font-size:24px;color:#566170">Europe in detail</p></div></div>'
 +src('Europe: Arkema (PA 11, PEKK), Evonik (PA 12, PEEK), Victrex (PEEK), Syensqo (PEEK, PPSU), TotalEnergies Corbion (PLA), Henkel Loctite, Forward AM, EOS, Prusa, Nanoscribe, micro resist.')+foot()
 +notes('Ring colour = role: base-polymer producer (grey), filament (orange), powder (yellow), resin (green), 2PP photoresin (blue). Europe: Arkema, Colombes (Rilsan PA 11, Kepstan PEKK, Sartomer resins); Evonik, Essen (Vestosint PA 12 powders, Vestakeep PEEK); Victrex, Thornton-Cleveleys (PEEK, PAEK); Syensqo ex-Solvay, Brussels (KetaSpire PEEK, Radel PPSU); TotalEnergies Corbion, Gorinchem (Luminy PLA); Henkel, Düsseldorf (Loctite resins); Forward AM (ex BASF 3D Printing Solutions), Heidelberg (Ultrafuse filaments, powders, resins); EOS, Krailling (PA 2200 powders); Prusa Polymers, Prague (Prusament, PLA 25 €/kg, PETG 30 €/kg); Nanoscribe, Karlsruhe (IP resins); micro resist technology, Berlin (OrmoComp). Prices: tables/02_polymer_prices_makers.csv. Head-office locations to verify before publication.')+'</section>')
for i,k,kick,t,b,c,n in am[1:4]: fig_side(i,'AM PROCESS',kick,t,k,b,c,note=n)
write('bjt',sec_open('bjt')+head('AM PROCESS','BINDER JETTING (BJT)','Binder jetting: one AM step, then four powder-metallurgy steps')+img('f05',1664,420)
 +'<div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:16px">'+card('Starting state','powder + liquid binder',TOPS[0])+card('Twin','pressing and sintering',TOPS[1])+card('Internal steps','print, cure, depowder, debind, sinter',TOPS[2])+card('Watch','15–20 % shrinkage built into the file',TOPS[3])+'</div>'
 +foot()+notes('The printer replaces the die; curing, depowdering, debinding and sintering come from powder metallurgy. No melt pool, so no residual stress from printing. FR : projection de liant, déliantage, frittage. DE: Binder Jetting, Entbindern, Sintern.')+'</section>')
for i,k,kick,t,b,c,n in am[4:]: fig_side(i,'AM PROCESS',kick,t,k,b,c,note=n)

# ---------------- part 3 morphological box
part('part-3',3,'A morphological box','Material state × feedstock form × agent × addressing: every process is one path through the box.',
 ['Point, line, area, volume','Nine processes in the box','Empty cells: new processes'],'Zwicky\'s morphological box applied to AM, after Gebhardt §2.4.')
fig_full('addressing','A MORPHOLOGICAL BOX','ADDRESSING','A spot, a line, a mask or a whole volume writes the layer','d02',h=560,
 source='Point, line and area after Gebhardt & Hötter (2016) §2.4: vector, raster and mask exposure.',
 note='Vector: contour traced continuously, most accurate, slowest. Raster: line by line. Mask: whole layer at once, time independent of layer complexity. Volume: tomographic and volumetric printing. FR : adressage. DE: Belichtungsstrategie.')
write('box',sec_open('box')+head('A MORPHOLOGICAL BOX','ZWICKY','Every process is one path through the box')
 +table([['Process','Material state','Feedstock form','Agent','Addressing'],['SLA','liquid','vat','light','point'],['DLP','liquid','vat','light','area'],['Multi-jet fusion','powder','bed','agent + heat','line'],['Binder jetting','powder','bed','binder','line'],['Laser PBF','powder','bed','laser','point'],['Laser DED','powder or wire','jet','laser','point'],['FFF','plastic','filament','heat','point'],['Cold spray','powder','jet','kinetic energy','point'],['Volumetric printing','liquid','vat','light','volume']],[420,330,330,330,254],size=24)
 +'<div style="display:flex;flex-direction:column;gap:6px;background:#fbfaf7;border:1px solid #ddd6c6;border-top:5px solid #a8480f;border-radius:12px;padding:14px 20px"><p style="font-size:24px;font-weight:700;color:#a8480f">Exercise</p><p style="font-size:24px">Find the empty cells: area-wise metal PBF and volumetric printing appeared there.</p></div>'
 +foot()+notes('FR : boîte morphologique. DE: morphologischer Kasten.')+'</section>')

# ---------------- part 4 clocks, part 5 interface, part 6 potentials
part('part-4',4,'Clocks','A race between how fast the material sets and how fast the next layer comes.',['Microseconds to days','Supports and open time'],'Characteristic times on a log scale.')
fig_full('clocks','CLOCKS','LOG TIME','How fast the material sets decides how a layer meets the next','e02',h=640,
 note='Melt pool µs–ms, photopolymer ms–s, filament road ≈ 1–10 s, cake ≈ 30 min, concrete minutes to hours, binder jetting hours in the furnace. Explains build speed, supports and the open-time problem of concrete. FR : temps caractéristiques. DE: charakteristische Zeiten.')
part('part-5',5,'The layer interface','What joins layer n to layer n − 1, and is it the mechanism that made the layer?',['Six interfaces','Anisotropy, weak z'],'The interface explains anisotropy and design rules.')
fig_full('interfaces','THE LAYER INTERFACE','SIX MECHANISMS','Six ways to join a layer to the one below','e03',h=660,
 note='Photopolymer: over-cure. PBF and DED: remelting. FFF: polymer chains interdiffuse, often incompletely. Cold spray: plastic deformation. Binder jetting: binder bridges, then sinter necks. Sheet lamination: glue. FR : interface entre couches, anisotropie. DE: Schichtgrenzfläche, Anisotropie.')
part('part-6',6,'From physics to potentials','Gebhardt\'s theoretical potentials, derived from the material path.',['Detail, accuracy, surface','Residual stress, anisotropy','Machines and prices'],'After Gebhardt & Hötter §2.6.')
write('potentials',sec_open('potentials')+head('FROM PHYSICS TO POTENTIALS','GEBHARDT §2.6','Each design rule follows from the physics of the path')
 +table([['Criterion','Set by','Orders of magnitude','Design rule'],['Smallest detail','spot, droplet or particle size','0.1 µm (2PP) – 0.1 mm (PBF) – 1 mm (DED)','no feature below ≈ 2–3 voxels'],['Accuracy','shrinkage of the transformation','polymerisation, solidification; 15–20 % linear on sintering','scale the file, test parts'],['Surface','layer thickness + partly bonded particles','Ra ≈ 5–20 µm for metal PBF','machine functional faces'],['Residual stress','a liquid-to-solid step over a large temperature range','PBF, DED high; binder jetting, cold spray low','supports, stress relief, HIP'],['Anisotropy','the layer interface','z weakest in FFF','load along the layers']],[300,480,520,364])
 +src('After Gebhardt & Hötter (2016) §2.6; orders of magnitude indicative.')+foot()+notes('FR : potentiels théoriques, règles de conception. DE: theoretische Potenziale, Konstruktionsregeln.')+'</section>')
write('lpbf-prices',sec_open('lpbf-prices')+head('MACHINES AND PRICES','METAL LASER PBF','A metal laser PBF machine costs 0.2–1 M$')
 +table([['Manufacturer','Model','Price (USD)','Build volume (mm)'],['SLM Solutions','SLM 125','400 000 – 500 000','125 × 125 × 125'],['SLM Solutions','SLM 280','500 000 – 800 000','280 × 280 × 300'],['SLM Solutions','SLM 500','800 000 +','500 × 500 × 500'],['EOS','M 290','600 000 – 1 000 000','290 × 290 × 400'],['EOS','M 400','1 000 000 +','400 × 400 × 400'],['Renishaw','AM 400','600 000 – 1 000 000','to check'],['TRUMPF','TruPrint 1000','170 000','100 × 100 × 100']])
 +src('Source: 03_Technologies deck (2025), after AMPOWER Insights. Table: 02_technologies/tables/02_machines_lpbf_metal.csv.')+foot()+notes('Prices as listed in the 2025 deck; Renishaw AM 400 build volume to check against the data sheet.')+'</section>')
write('bj-machines',sec_open('bj-machines')+head('MACHINES AND PRICES','METAL BINDER JETTING','Metal binder jetting machines aim at production rates')
 +table([['System','Maker','Build volume','Build speed','Resolution'],['X160PRO','ExOne (Desktop Metal)','800 × 500 × 400 mm','≤ 3 120 cm³/h','layers 30–200 µm'],['Production System P-50','Desktop Metal','490 × 380 × 260 mm','≤ 12 000 cm³/h','1 200 dpi'],['Metal Jet S100','HP','430 × 309 × 200 mm','1 990 cm³/h','1 200 dpi'],['Series 3','GE Additive','500 × 500 × 500 mm','≤ 100 × metal PBF','walls ≥ 400 µm'],['PX100','Markforged','250 × 217 × ? mm','1 000 cm³/h','1 600 dpi']])
 +src('Source: voxelmatters.com, complete guide to binder-based metal 3D printing. Table: 02_technologies/tables/02_machines_binder_jetting_metal.csv.')+foot()+notes('PX100 build height cut off on the source slide: to check.')+'</section>')
write('micro',sec_open('micro')+head('MACHINES AND PRICES','MICROPRINTING','Microprinting reaches the micrometre from liquid, paste, powder and ions')
 +table([['Printer','Technology','State','Min. layer','Resolution','Price (USD)'],['BMF microArch','projection micro-SLA','liquid','5 µm','2 µm','145 000 – 230 000'],['Nanoscribe Quantum X','two-photon polymerisation','liquid','0.1 µm','0.2 µm','500 000'],['UpNano NanoOne','two-photon polymerisation','liquid','0.17 µm','0.01 µm','on request'],['Incus Hammer Lab35','lithography-based metal','pasty','10 µm','35 µm','250 000'],['Exaddon Ceres','electrochemical deposition','ionised','—','< 1 µm','272 000'],['3D MicroPrint DMP','micro laser sintering','powder','15 µm','1 µm','on request'],['Microlight3D µFAB-3D','two-photon polymerisation','liquid','0.6 µm','0.2 µm','120 000 – 180 000']],size=24)
 +src('Source: all3dp.com, micro 3D printing guide. Table: 02_technologies/tables/02_machines_microprinting.csv.')+foot()+notes('')+'</section>')
# ---------------- references
part('part-7',7,'References','Standards, books and papers used in this chapter.',['Classification','Additive manufacturing'],'')
refs1=['DIN 8580, Fertigungsverfahren — Begriffe, Einteilung. Beuth.','ISO/ASTM 52900:2021, Additive manufacturing — General principles — Fundamentals and vocabulary.','M. F. Ashby, Materials Selection in Mechanical Design, 5th ed., Butterworth-Heinemann, 2016.','M. F. Ashby, H. Shercliff, D. Cebon, Materials: Engineering, Science, Processing and Design, 3rd ed., 2013.','M. F. Ashby, K. Johnson, Materials and Design, 3rd ed., 2014.','ASTM F3301, Thermal post-processing of metal parts made via powder bed fusion.','H. V. Atkinson, B. A. Rickinson, Hot Isostatic Processing, Adam Hilger, 1991.']
refs2=['A. Gebhardt, J.-S. Hötter, Additive Manufacturing: 3D Printing for Prototyping and Manufacturing, Hanser, 2016.','I. Gibson, D. Rosen, B. Stucker, M. Khorasani, Additive Manufacturing Technologies, 3rd ed., Springer, 2021.','J.-P. Kruth, Material incress manufacturing by rapid prototyping techniques, CIRP Annals 40 (1991).','J.-P. Kruth, M. C. Leu, T. Nakagawa, Progress in additive manufacturing and rapid prototyping, CIRP Annals 47 (1998).','J.-P. Kruth et al., Binding mechanisms in SLS and SLM, Rapid Prototyping Journal 11 (2005).','N. Tuncer, A. Bose, Solid-state metal additive manufacturing: a review, JOM 72 (2020).','J. R. Tumbleston et al., Continuous liquid interface production of 3D objects, Science 347 (2015) 1349.','M. Zastrow, The new 3D printing, Nature 578 (2020) 20–23.']
write('references',sec_open('references')+head('REFERENCES','','Sources of this chapter')
 +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px">'
 +f'<div style="display:flex;flex-direction:column;gap:10px"><h3 style="{FONT};font-size:30px;font-weight:700">Classification and processes</h3>'+ul(refs1,24)+'</div>'
 +f'<div style="display:flex;flex-direction:column;gap:10px"><h3 style="{FONT};font-size:30px;font-weight:700">Additive manufacturing</h3>'+ul(refs2,24)+'</div></div>'+foot()+notes('')+'</section>')

refs3=['all3dp.com — Micro 3D printing guide (2023): micro-printer table, prices.','Nanoscribe — nanoscribe.com: Quantum X; Photonic Professional GT2 (discontinued Nov. 2025).','Femtika — femtika.lt: Laser Nanofactory workstation; price via aniwaa.com micro-AM buyer\'s guide.','UpNano — NanoOne 1000 data sheet (2024), am.nus.edu.sg; aggiefab.tamu.edu 2PP selection guide (2025).','Microlight3D — aniwaa.com µFAB-3D and Altraspin pages; 3dprintingindustry.com, Altraspin launch (2019).','BMF — bmf3d.com, microArch S240. Nano Dimension — nano-di.com, Fabrica Tera 250.']
refs4=['Formlabs — formlabs.com, Form 4L; dental.formlabs.com, Form 4BL vs Carbon L1; matterhackers.com, Form 4 / 4L / 3L.','Carbon — carbon3d.com, M1–L1, press releases 2024–2026, lattice white paper; techcrunch.com (2022); voxelmatters.com, $60M raise (2025); dynamism.com.','Stratasys — aniwaa.com, Origin One; javelin-tech.com, Stratasys price list.','Asiga — techselect.aaoinfo.org, MAX 2; tools.tavast.eu and dream3d.co.uk, MAX X. Prusa — tomshardware.com, SL1S Speed.','Elegoo — all3dp.com, Saturn 4 Ultra 16K (2025). 3D Systems — all3dp.com, SLA 750. UnionTech — fabbaloo.com, RSPro.','Polymers — EOS PA 2200 data sheet; Prusament and BASF Ultrafuse TDS; Kayaku SU-8 TDS; Nanoscribe IP-PDMS; Sinterit SLS powder price guide; Fiberlogy PEI 9085; jlc3dp.com PEEK price; BCG exhibit on AM plastics.','Maps — Natural Earth 1:110m (public domain), via GeoPandas.']
write('references-web',sec_open('references-web')+head('REFERENCES','WEBSITES AND DATA SHEETS','Printers, prices and makers (accessed November 2026)')
 +'<div style="display:grid;grid-template-columns:1fr 1fr;gap:32px">'
 +f'<div style="display:flex;flex-direction:column;gap:10px"><h3 style="{FONT};font-size:30px;font-weight:700">Micro-printing and multi-photon</h3>'+ul(refs3,24)+'</div>'
 +f'<div style="display:flex;flex-direction:column;gap:10px"><h3 style="{FONT};font-size:30px;font-weight:700">DLP, MSLA, CLIP and laser SLA</h3>'+ul(refs4,24)+'</div></div>'+foot()
 +notes('Full URLs in 02_technologies/tables/02_printers_price_voxel.csv (column source).')+'</section>')

part('part-8',8,'Parked slides','Slides kept for later, to be placed in the story.',['Ashby process tree','Injection moulding, powder metallurgy','Where the geometry lives','DIN states and twins','Vat photopolymerisation (overview)'],'Moved here on 9 Nov 2026.')
PARK=['ashby-tree','injection','pm','geometry','twins','vpp']
order[:]=[x for x in order if x not in PARK]+PARK
deck={"v":4,"createdOnFiles":{"v":1,"at":"2026-11-09T00:05:00Z"},"lists":"css","title":"AM technologies","order":order,"sections":sections,"cover":"cover",
 "faces":{"space-grotesk":{"family":"Space Grotesk","href":"https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400..700&display=swap"},"inter":{"family":"Inter","href":"https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap"}},"designSystems":[]}
(R/'deck.json').write_text(json.dumps(deck,indent=1,ensure_ascii=False))
print(len(order),'slides'); 
import re
for f in sorted((R/'slides').glob('*.html')):
    t=f.read_text(); n=len(re.findall(r'<(?!/)[a-zA-Z]',t))
    if n>190 or ('EXED' not in t and f.stem!='cover'): print('CHECK',f.stem,n)
