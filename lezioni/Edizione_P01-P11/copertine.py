"""Copertine delle spedizioni P01-P11: scene Blender costruite da codice e rese con Cycles.

Uso (Blender 4.3 o successivo, oppure il modulo bpy di PyPI):
    python copertine.py P01 [P02 ...]    oppure    blender -b -P copertine.py -- P01

Ogni scena riprende l'impianto delle copertine delle lezioni (camera ortografica, fondale stellare, tre luci ad
area) e aggiunge il pianeta della spedizione con un oggetto ricavato dai dati del caso. Nessuna texture esterna e
nessuna immagine generata: materiali procedurali e geometrie calcolate. Scrive Scena/copertina.blend,
Scena/copertina.jpg e Scena/render.json nella cartella della lezione.

Codice: PolyForm Noncommercial 1.0.0. Required Notice: Copyright 2026 Marzio De Corato.
"""
import csv
import json
import math
import random
import sys
from pathlib import Path

import bpy

LEZIONI = Path(__file__).resolve().parent.parent
CARTELLE = {'P01': 'P01_Pori', 'P02': 'P02_Foraminiferi', 'P03': 'P03_Nilo', 'P04': 'P04_Geyser', 'P05': 'P05_CO2',
            'P06': 'P06_Validazione', 'P07': 'P07_Terreno', 'P08': 'P08_Proxy', 'P09': 'P09_Livelli',
            'P10': 'P10_Ricostruibile', 'P11': 'P11_Stazioni'}
# Colori del pianeta d'origine (src/planets.js): terre, fondali, rilievi, atmosfera.
PIANETI = {'P01': ('#628f79', '#063b65', '#e5ddae', '#62d2e5'), 'P02': ('#5f8c86', '#0b3a5c', '#dcd8b6', '#6ccbe0'),
           'P03': ('#b2d6e1', '#163b57', '#e6edef', '#79d8df'), 'P04': ('#a78e70', '#4b575c', '#dad4b5', '#d4c5a5'),
           'P05': ('#a7cfdc', '#1b3f5c', '#eef2f2', '#86d9e2'), 'P06': ('#bc814f', '#4a2c27', '#e7c18c', '#e2aa76'),
           'P07': ('#9f503c', '#382b33', '#d79d72', '#d68d7c'), 'P08': ('#aa7760', '#442f35', '#e4c59c', '#ddb292'),
           'P09': ('#35313b', '#141820', '#e46e20', '#e77145'), 'P10': ('#9dacae', '#333b4e', '#d8d3ba', '#b3d4e5'),
           'P11': ('#5c8685', '#39394d', '#b4a27a', '#91c5b9')}
SEMI = {p: 4101 + 17 * i for i, p in enumerate(CARTELLE)}


def lineare(hexa, a=1.0):
    """Colore sRGB esadecimale nello spazio lineare di Blender."""
    v = [int(hexa[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    return tuple(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in v) + (a,)


def leggi(pid, nome):
    with open(LEZIONI / CARTELLE[pid] / nome, encoding='utf-8') as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- materiali
def materiale(nome, colore, rugosita=0.55, metallo=0.0, emissione=0.0, coat=0.0):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = lineare(colore) if isinstance(colore, str) else colore
    p.inputs['Roughness'].default_value = rugosita
    p.inputs['Metallic'].default_value = metallo
    p.inputs['Coat Weight'].default_value = coat
    if emissione:
        p.inputs['Emission Color'].default_value = p.inputs['Base Color'].default_value
        p.inputs['Emission Strength'].default_value = emissione
    return m


def rampa(nt, colori, posizioni=None):
    r = nt.nodes.new('ShaderNodeValToRGB')
    el = r.color_ramp.elements
    posizioni = posizioni or [i / (len(colori) - 1) for i in range(len(colori))]
    el[0].position, el[0].color = posizioni[0], lineare(colori[0])
    el[1].position, el[1].color = posizioni[-1], lineare(colori[-1])
    for pos, col in zip(posizioni[1:-1], colori[1:-1]):
        e = el.new(pos)
        e.color = lineare(col)
    return r


def materiale_rumore(nome, colori, scala=4.0, dettaglio=8.0, rilievo=0.25, scala_rilievo=40.0, posizioni=None,
                     rugosita=0.6, coordinate='Object'):
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = rugosita
    tc = nt.nodes.new('ShaderNodeTexCoord')
    n = nt.nodes.new('ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = scala
    n.inputs['Detail'].default_value = dettaglio
    nt.links.new(tc.outputs[coordinate], n.inputs['Vector'])
    r = rampa(nt, colori, posizioni)
    nt.links.new(n.outputs['Fac'], r.inputs['Fac'])
    nt.links.new(r.outputs['Color'], p.inputs['Base Color'])
    if rilievo:
        n2 = nt.nodes.new('ShaderNodeTexNoise')
        n2.inputs['Scale'].default_value = scala_rilievo
        n2.inputs['Detail'].default_value = 3.0
        nt.links.new(tc.outputs[coordinate], n2.inputs['Vector'])
        b = nt.nodes.new('ShaderNodeBump')
        b.inputs['Strength'].default_value = rilievo
        nt.links.new(n2.outputs['Fac'], b.inputs['Height'])
        nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m


def materiale_pori(nome, roccia, poro, scala=9.0, soglia=0.22):
    """Arenaria con pori: celle di Voronoi scure sotto la soglia di distanza, con rilievo."""
    m = bpy.data.materials.new(nome)
    m.use_nodes = True
    nt = m.node_tree
    p = nt.nodes['Principled BSDF']
    p.inputs['Roughness'].default_value = 0.8
    tc = nt.nodes.new('ShaderNodeTexCoord')
    v = nt.nodes.new('ShaderNodeTexVoronoi')
    v.inputs['Scale'].default_value = scala
    nt.links.new(tc.outputs['Object'], v.inputs['Vector'])
    r = nt.nodes.new('ShaderNodeValToRGB')
    r.color_ramp.interpolation = 'CONSTANT'
    r.color_ramp.elements[0].color = lineare(poro)
    r.color_ramp.elements[1].position = soglia
    r.color_ramp.elements[1].color = lineare(roccia)
    nt.links.new(v.outputs['Distance'], r.inputs['Fac'])
    n = nt.nodes.new('ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = 60
    mix = nt.nodes.new('ShaderNodeMix')
    mix.data_type = 'RGBA'
    mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 0.25
    nt.links.new(r.outputs['Color'], mix.inputs['A'])
    nt.links.new(n.outputs['Color'], mix.inputs['B'])
    nt.links.new(mix.outputs['Result'], p.inputs['Base Color'])
    b = nt.nodes.new('ShaderNodeBump')
    b.inputs['Strength'].default_value = 0.6
    nt.links.new(v.outputs['Distance'], b.inputs['Height'])
    nt.links.new(b.outputs['Normal'], p.inputs['Normal'])
    return m


def assegna(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    return obj


def liscio(obj):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    return obj


# ---------------------------------------------------------------- scena comune
def scena(pid):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.name = 'Copertina ' + pid
    sc.render.engine = 'CYCLES'
    sc.cycles.device = 'CPU'
    sc.cycles.samples = 16
    sc.cycles.seed = SEMI[pid]
    sc.cycles.use_denoising = False
    sc.cycles.max_bounces = 12
    sc.render.resolution_x, sc.render.resolution_y, sc.render.resolution_percentage = 2400, 1500, 100
    sc.view_settings.view_transform = 'AgX'
    w = bpy.data.worlds.new('Spazio')
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.045, 0.045, 0.055, 1)
    sc.world = w
    cam = bpy.data.cameras.new('Camera 16x10')
    cam.type = 'ORTHO'
    cam.ortho_scale = 11.6
    co = bpy.data.objects.new('Camera', cam)
    co.location, co.rotation_euler = (0, -15, 6), (1.19, 0, 0)
    sc.collection.objects.link(co)
    sc.camera = co
    for nome, loc, rot, energia, colore, size in (
            ('Contorno', (4, 4, 6), (0.621, 0, 2.772), 1200, (0.66, 0.8, 1.0), 3.0),
            ('Luce diffusa', (7, -4, 3), (1.111, 0, 0.85), 520, (0.5, 0.72, 1.0), 5.0),
            ('Luce stellare', (-2, -6, 8), (0.751, 0, -0.638), 980, (1.0, 0.84, 0.67), 5.0)):
        ld = bpy.data.lights.new(nome, 'AREA')
        ld.shape, ld.size, ld.energy, ld.color = 'DISK', size, energia, colore
        lo = bpy.data.objects.new(nome, ld)
        lo.location, lo.rotation_euler = loc, rot
        sc.collection.objects.link(lo)
    # Fondale: lastra emissiva con nebulosità violacea a bassa intensità.
    bpy.ops.mesh.primitive_cube_add(location=(0, 6, -2))
    fondo = bpy.context.object
    fondo.name = 'Fondale stellare'
    fondo.scale = (14, 0.01, 9)
    m = bpy.data.materials.new('Spazio profondo')
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    n = nt.nodes.new('ShaderNodeTexNoise')
    n.inputs['Scale'].default_value = 3.5
    n.inputs['Detail'].default_value = 6
    n.inputs['Distortion'].default_value = 1.1
    r = nt.nodes.new('ShaderNodeValToRGB')
    r.color_ramp.elements[0].position, r.color_ramp.elements[0].color = 0.22, (0.001, 0.002, 0.007, 1)
    r.color_ramp.elements[1].position, r.color_ramp.elements[1].color = 0.77, (0.056, 0.031, 0.098, 1)
    e = nt.nodes.new('ShaderNodeEmission')
    nt.links.new(n.outputs['Fac'], r.inputs['Fac'])
    nt.links.new(r.outputs['Color'], e.inputs['Color'])
    nt.links.new(e.outputs['Emission'], nt.nodes['Material Output'].inputs['Surface'])
    assegna(fondo, m)
    # Campo stellare: 1100 quadratini emissivi davanti al fondale.
    rng = random.Random(SEMI[pid])
    verts, faces = [], []
    for i in range(1100):
        x, z, s = rng.uniform(-8, 8), rng.uniform(-8, 5), rng.uniform(0.003, 0.0125)
        k = len(verts)
        verts += [(x - s / 2, 5.4, z - s / 2), (x + s / 2, 5.4, z - s / 2), (x + s / 2, 5.4, z + s / 2), (x - s / 2, 5.4, z + s / 2)]
        faces.append((k, k + 1, k + 2, k + 3))
    me = bpy.data.meshes.new('Campo stellare')
    me.from_pydata(verts, [], faces)
    stelle = bpy.data.objects.new('Campo stellare', me)
    sc.collection.objects.link(stelle)
    assegna(stelle, materiale('Punti stellari', (0.7, 0.83, 1.0, 1), emissione=2.0))
    return sc


def pianeta(pid, loc=(4.15, 2.0, 1.35), raggio=1.25):
    terre, fondali, rilievi, atmosfera = PIANETI[pid]
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, radius=raggio, location=loc)
    p = liscio(bpy.context.object)
    p.name = 'Pianeta della spedizione'
    p.rotation_euler = (0.35, 0.2, SEMI[pid] % 7 * 0.4)
    assegna(p, materiale_rumore('Superficie del pianeta', [fondali, fondali, terre, rilievi], scala=2.4 + SEMI[pid] % 5 * 0.3,
                                posizioni=[0.0, 0.46, 0.55, 0.78], rilievo=0.18))
    # Alone atmosferico: guscio trasparente che emette verso il bordo.
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=raggio * 1.035, location=loc)
    a = liscio(bpy.context.object)
    a.name = 'Atmosfera'
    m = bpy.data.materials.new('Atmosfera')
    m.use_nodes = True
    m.blend_method = 'BLEND'
    nt = m.node_tree
    nt.nodes.remove(nt.nodes['Principled BSDF'])
    lw = nt.nodes.new('ShaderNodeLayerWeight')
    lw.inputs['Blend'].default_value = 0.35
    tr = nt.nodes.new('ShaderNodeBsdfTransparent')
    em = nt.nodes.new('ShaderNodeEmission')
    em.inputs['Color'].default_value = lineare(atmosfera)
    em.inputs['Strength'].default_value = 1.6
    mix = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(lw.outputs['Facing'], mix.inputs['Fac'])
    nt.links.new(tr.outputs['BSDF'], mix.inputs[1])
    nt.links.new(em.outputs['Emission'], mix.inputs[2])
    nt.links.new(mix.outputs['Shader'], nt.nodes['Material Output'].inputs['Surface'])
    assegna(a, m)


def cilindro(nome, loc, raggio, altezza, mat, vertici=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertici, radius=raggio, depth=altezza,
                                        location=(loc[0], loc[1], loc[2] + altezza / 2))
    o = bpy.context.object
    o.name = nome
    return assegna(o, mat)


def barre(nome, posizioni, altezze, larghezza, materiali, scelta):
    """Una mesh unica di parallelepipedi: posizione della base, altezza, materiale scelto per indice."""
    verts, faces, idx = [], [], []
    for k, ((x, y, z), h) in enumerate(zip(posizioni, altezze)):
        s = larghezza / 2
        b = len(verts)
        verts += [(x - s, y - s, z), (x + s, y - s, z), (x + s, y + s, z), (x - s, y + s, z),
                  (x - s, y - s, z + h), (x + s, y - s, z + h), (x + s, y + s, z + h), (x - s, y + s, z + h)]
        for f in ((0, 1, 2, 3), (4, 7, 6, 5), (0, 4, 5, 1), (1, 5, 6, 2), (2, 6, 7, 3), (3, 7, 4, 0)):
            faces.append(tuple(b + i for i in f))
            idx.append(scelta(k))
    me = bpy.data.meshes.new(nome)
    me.from_pydata(verts, [], faces)
    o = bpy.data.objects.new(nome, me)
    bpy.context.scene.collection.objects.link(o)
    for m in materiali:
        o.data.materials.append(m)
    for poly, i in zip(o.data.polygons, idx):
        poly.material_index = i
    return o


def tubo(nome, punti, raggio, mat):
    cu = bpy.data.curves.new(nome, 'CURVE')
    cu.dimensions = '3D'
    cu.bevel_depth = raggio
    cu.bevel_resolution = 4
    sp = cu.splines.new('POLY')
    sp.points.add(len(punti) - 1)
    for pt, (x, y, z) in zip(sp.points, punti):
        pt.co = (x, y, z, 1)
    o = bpy.data.objects.new(nome, cu)
    bpy.context.scene.collection.objects.link(o)
    cu.materials.append(mat)
    return o


def lastra(nome, centro, dimensioni, mat):
    bpy.ops.mesh.primitive_cube_add(location=centro)
    o = bpy.context.object
    o.name = nome
    o.scale = tuple(d / 2 for d in dimensioni)
    return assegna(o, mat)


# ---------------------------------------------------------------- soggetti
def p01():
    """Tre carote di arenaria porosa su una lastra e una sezione sottile sollevata."""
    pietra = materiale_pori('Arenaria porosa', '#c9a77c', '#2e2119', scala=11, soglia=0.2)
    lastra('Basamento', (2.6, -0.6, -2.12), (4.4, 1.7, 0.16), materiale_rumore('Basamento', ['#2a3140', '#3b4456'], rilievo=0.1))
    for k, (x, h) in enumerate(((1.35, 1.75), (2.45, 1.35), (3.55, 1.05))):
        liscio(cilindro('Carota %d' % (k + 1), (x, -0.6, -2.04), 0.4, h, pietra))
    sezione = cilindro('Sezione sottile', (4.55, -0.9, -1.2), 0.42, 0.05, materiale_pori('Sezione', '#e3cfa8', '#1f2a3a', 14, 0.24))
    sezione.rotation_euler = (1.05, 0.2, 0.3)


def p02():
    """Carosello di coppe di una trappola sedimentaria e tre gusci di foraminiferi ingranditi."""
    bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=1.45, depth=0.14, location=(2.5, -0.4, -2.1))
    assegna(bpy.context.object, materiale('Carosello', '#59677a', 0.35, 0.7))
    coppa = materiale('Coppe', '#b7c4cf', 0.25, 0.85)
    for k in range(12):
        a = 2 * math.pi * k / 12
        cilindro('Coppa %d' % (k + 1), (2.5 + 1.15 * math.cos(a), -0.4 + 1.15 * math.sin(a), -2.03), 0.15, 0.36, coppa, 32)
    guscio = materiale_rumore('Guscio', ['#efe6d2', '#d8c7a6'], scala=20, rilievo=0.35, scala_rilievo=120, rugosita=0.5)
    for (cx, cy, cz, rot, s) in ((1.9, -0.9, -0.7, 0.4, 1.0), (3.15, -1.1, -0.35, 2.2, 0.85), (4.5, -0.8, -1.05, 4.0, 0.7)):
        for i in range(9):
            r = 0.07 * 1.24 ** i * s
            a = rot + i * 0.95
            d = 0.12 * 1.2 ** i * s
            bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=r,
                                                 location=(cx + d * math.cos(a), cy, cz + d * math.sin(a)))
            assegna(liscio(bpy.context.object), guscio)


def p03():
    """I cento volumi annuali del Nilo ad Aswan come colonne disposte ad arco; il colore cambia dal 1898."""
    d = leggi('P03', 'dati/progetti/nile.csv')
    pos, alt = [], []
    for k, r in enumerate(d):
        a = math.radians(205 + 130 * k / (len(d) - 1))
        pos.append((2.75 + 2.6 * math.cos(a), 0.9 + 2.0 * math.sin(a), -2.25))
        alt.append(float(r['volume_1e8_m3']) / 1000 * 1.55)
    prima, dopo = materiale('Prima del 1898', '#55b9c4', 0.4), materiale('Dal 1898', '#2f62a8', 0.4)
    barre('Volumi annuali', pos, alt, 0.075, [prima, dopo], lambda k: 0 if int(d[k]['year']) < 1898 else 1)


def p04():
    """Cono di sinter con cratere e pennacchio di vapore."""
    bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=1.9, radius2=0.35, depth=0.9, location=(1.9, -0.3, -1.95))
    cono = bpy.context.object
    cono.name = 'Cono di sinter'
    mod = cono.modifiers.new('Suddivisione', 'SUBSURF')
    mod.levels = mod.render_levels = 2
    assegna(liscio(cono), materiale_rumore('Sinter', ['#9a8f7c', '#d9cdb4', '#c9884f', '#e8dfcc'], scala=6, rilievo=0.5,
                                          posizioni=[0, 0.4, 0.55, 1]))
    vapore = materiale('Vapore', '#eef2f6', 0.9, emissione=0.35)
    rng = random.Random(7)
    for i in range(70):
        t = i / 69
        r = 0.12 + 0.42 * t
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=r,
                                             location=(1.9 + rng.uniform(-0.25, 0.25) * (0.4 + t) - 0.3 * t ** 2,
                                                       -0.3 + rng.uniform(-0.2, 0.2), -1.45 + 3.2 * t))
        assegna(liscio(bpy.context.object), vapore)


def p05():
    """Medie mensili della CO2 a Mauna Loa (1958-2001) come tubo luminoso con l'oscillazione stagionale."""
    d = leggi('P05', 'dati/progetti/co2_weekly.csv')
    mesi = {}
    for r in d:
        if r['co2_ppm'].strip():
            mesi.setdefault(r['date'][:7], []).append(float(r['co2_ppm']))
    chiavi = sorted(mesi)
    lo, hi = min(sum(v) / len(v) for v in mesi.values()), max(sum(v) / len(v) for v in mesi.values())
    pts = []
    for k, c in enumerate(chiavi):
        m = sum(mesi[c]) / len(mesi[c])
        t = k / (len(chiavi) - 1)
        pts.append((0.55 + 5.0 * t, -0.6 - 0.6 * math.sin(t * math.pi), -2.6 + 3.4 * (m - lo) / (hi - lo)))
    tubo('Medie mensili', pts, 0.028, materiale('Curva', '#72d8c8', 0.3, emissione=1.4))
    lastra('Base', (3.05, -0.4, -2.75), (5.4, 1.8, 0.08), materiale('Base', '#253046', 0.5, 0.3))


def p06():
    """Sessantaquattro concentrazioni come colonne sul reticolo; la fascia orientale è il settore di verifica."""
    d = leggi('P06', 'dati/spazio_v3.csv')
    c = [float(r['concentrazione']) for r in d]
    lo, hi = min(c), max(c)
    pos = [((float(r['x_m']) - 875) / 250 * 0.42, (float(r['y_m']) - 875) / 250 * 0.42, 0) for r in d]
    alt = [0.25 + 1.5 * (v - lo) / (hi - lo) for v in c]
    ovest, est = materiale('Settore di adattamento', '#4fb3a9', 0.45), materiale('Settore di verifica', '#e09a4f', 0.45)
    o = barre('Concentrazioni', pos, alt, 0.22, [ovest, est], lambda k: 0 if d[k]['area'] == 'Ovest' else 1)
    piano = lastra('Reticolo', (0, 0, -0.05), (3.6, 3.6, 0.1), materiale('Reticolo', '#273247', 0.6))
    for ob in (o, piano):
        ob.location = (ob.location[0] + 2.85, ob.location[1] - 0.2, ob.location[2] - 2.45)
        ob.rotation_euler = (0, 0, math.radians(-38))


def p07():
    """Il raster delle quote come blocco di terreno, con pareti stratificate."""
    d = leggi('P07', 'dati/raster_v3.csv')
    nr = max(int(r['riga']) for r in d) + 1
    nc = max(int(r['colonna']) for r in d) + 1
    q = {(int(r['riga']), int(r['colonna'])): float(r['quota_m']) for r in d}
    lo, hi = min(q.values()), max(q.values())
    s, base = 0.155, -2.6
    x0, y0 = 3.0 - (nc - 1) * s / 2, 0.2 - (nr - 1) * s / 2
    z = lambda i, j: -1.9 + 1.25 * (q[(i, j)] - lo) / (hi - lo)
    verts, faces = [], []
    for i in range(nr):
        for j in range(nc):
            verts.append((x0 + j * s, y0 + (nr - 1 - i) * s, z(i, j)))
    for i in range(nr - 1):
        for j in range(nc - 1):
            a = i * nc + j
            faces.append((a, a + nc, a + nc + 1, a + 1))
    bordo = [(0, j) for j in range(nc)] + [(i, nc - 1) for i in range(1, nr)] + \
        [(nr - 1, j) for j in range(nc - 2, -1, -1)] + [(i, 0) for i in range(nr - 2, 0, -1)]
    k0 = len(verts)
    for i, j in bordo:
        x, y, _ = verts[i * nc + j]
        verts.append((x, y, base))
    n = len(bordo)
    for t in range(n):
        i, j = bordo[t]
        i2, j2 = bordo[(t + 1) % n]
        faces.append((i * nc + j, i2 * nc + j2, k0 + (t + 1) % n, k0 + t))
    faces.append(tuple(range(k0 + n - 1, k0 - 1, -1)))
    me = bpy.data.meshes.new('Terreno')
    me.from_pydata(verts, [], faces)
    me.validate()
    o = bpy.data.objects.new('Terreno', me)
    bpy.context.scene.collection.objects.link(o)
    # Colore per quota: attributo di vertice letto dal materiale della superficie.
    attr = me.color_attributes.new('quota', 'FLOAT_COLOR', 'POINT')
    pal = ['#2f5a45', '#6f8f4e', '#b98f5e', '#efe3c6']
    def tinta(t):
        k = min(int(t * (len(pal) - 1)), len(pal) - 2)
        f = t * (len(pal) - 1) - k
        a, b = lineare(pal[k]), lineare(pal[k + 1])
        return tuple(a[i] * (1 - f) + b[i] * f for i in range(3)) + (1,)
    for v in me.vertices:
        attr.data[v.index].color = tinta(max(0.0, min(1.0, (v.co.z + 1.9) / 1.25)))
    sup = bpy.data.materials.new('Superficie')
    sup.use_nodes = True
    nt = sup.node_tree
    at = nt.nodes.new('ShaderNodeAttribute')
    at.attribute_name = 'quota'
    nt.links.new(at.outputs['Color'], nt.nodes['Principled BSDF'].inputs['Base Color'])
    nt.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.75
    o.data.materials.append(sup)
    o.data.materials.append(materiale_rumore('Pareti', ['#4a3a33', '#7b5b45', '#a7825d'], scala=2.0, rilievo=0.2))
    for poly in o.data.polygons:
        poly.material_index = 0 if poly.index < (nr - 1) * (nc - 1) else 1
        poly.use_smooth = poly.index < (nr - 1) * (nc - 1)
    # Rotazione attorno al centro del blocco: due pareti in vista.
    cx, cy = 3.0, 0.2
    for v in me.vertices:
        x, y = v.co.x - cx, v.co.y - cy
        a = math.radians(-24)
        v.co.x, v.co.y = cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)


def p08():
    """Carota sedimentaria a dischi colorati dal proxy, con lo scarto di uno hiatus e le sei ancore cronologiche."""
    d = leggi('P08', 'dati/proxy_v3.csv')
    anc = leggi('P08', 'dati/cronologia_v3.csv')
    v = [float(r['proxy']) for r in d]
    lo, hi = min(v), max(v)
    pal = ['#2c3e5c', '#3f6f8a', '#7aa595', '#d8c38e', '#d9894f']
    def colore(t):
        k = min(int(t * (len(pal) - 1)), len(pal) - 2)
        f = t * (len(pal) - 1) - k
        a, b = lineare(pal[k]), lineare(pal[k + 1])
        return tuple(a[i] * (1 - f) + b[i] * f for i in range(3)) + (1,)
    mats = [materiale('Proxy %d' % i, colore(i / 15), 0.6) for i in range(16)]
    top, h = 1.2, 3.3 / len(d)
    for k, r in enumerate(d):
        prof = float(r['profondita_cm'])
        gap = 0.18 if prof > 80 else 0.0
        t = (float(r['proxy']) - lo) / (hi - lo)
        cilindro('Livello %d' % k, (2.3, -0.5, top - (k + 1) * h - gap), 0.5, h * 0.98, mats[min(15, int(t * 15.99))], 40)
    oro = materiale('Ancora', '#e9c46a', 0.25, 0.9)
    for r in anc:
        prof = float(r['profondita_cm'])
        gap = 0.18 if prof > 80 else 0.0
        bpy.ops.mesh.primitive_torus_add(major_radius=0.56, minor_radius=0.025,
                                         location=(2.3, -0.5, top - prof / 2 * h - gap))
        assegna(bpy.context.object, oro)
    cilindro('Hiatus', (2.3, -0.5, top - 41 * h - 0.17), 0.53, 0.012, materiale('Hiatus', '#d1495b', 0.4, emissione=1.0), 40)


def p09():
    """Cento massimi annuali come colonne su un anello; il disco traslucido segna il livello centennale."""
    d = leggi('P09', 'dati/estremi_v3.csv')
    q = [float(r['portata_massima_m3s']) for r in d]
    scala = 2.1 / 900
    pos, alt = [], []
    for k, v in enumerate(q):
        a = 2 * math.pi * k / len(q)
        pos.append((2.75 + 1.55 * math.cos(a), -0.25 + 1.55 * math.sin(a), -2.3))
        alt.append(v * scala)
    soglia = 857.9
    sotto, sopra = materiale('Massimi', '#5d8fb8', 0.45), materiale('Oltre il livello', '#e46e20', 0.35, emissione=0.6)
    barre('Massimi annuali', pos, alt, 0.075, [sotto, sopra], lambda k: 1 if q[k] > soglia else 0)
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=1.66, depth=0.012, location=(2.75, -0.25, -2.3 + soglia * scala))
    disco = bpy.context.object
    m = materiale('Livello centennale', '#e77145', 0.2, emissione=0.25)
    m.node_tree.nodes['Principled BSDF'].inputs['Alpha'].default_value = 0.16
    m.blend_method = 'BLEND'
    assegna(disco, m)
    bpy.ops.mesh.primitive_cylinder_add(vertices=128, radius=1.75, depth=0.1, location=(2.75, -0.25, -2.36))
    assegna(bpy.context.object, materiale('Base', '#262f42', 0.55, 0.3))


def p10():
    """Catena di blocchi (dati, funzioni, controlli, risultati, archivio) con la storia delle versioni."""
    corpo = materiale('Blocco', '#2b3a52', 0.35, 0.4, coat=0.6)
    bordo = materiale('Spigoli', '#72d8c8', 0.3, emissione=2.2)
    centri = [(0.75 + 0.98 * k, -0.4 - 0.15 * k, -1.85 + 0.42 * k) for k in range(5)]
    for k, c in enumerate(centri):
        bpy.ops.mesh.primitive_cube_add(size=0.62, location=c, rotation=(0.2, 0.1, 0.35 + 0.1 * k))
        b = bpy.context.object
        b.name = 'Blocco %d' % (k + 1)
        assegna(b, corpo)
        bpy.ops.mesh.primitive_cube_add(size=0.64, location=c, rotation=(0.2, 0.1, 0.35 + 0.1 * k))
        w = bpy.context.object
        w.name = 'Spigoli %d' % (k + 1)
        mod = w.modifiers.new('Spigoli', 'WIREFRAME')
        mod.thickness = 0.022
        assegna(w, bordo)
    for a, b in zip(centri, centri[1:]):
        tubo('Collegamento', [a, b], 0.03, materiale('Flusso', '#abb5ff', 0.3, emissione=1.2))
    pts = [(0.75 + 0.38 * k, -1.4, -2.6 + 0.03 * k) for k in range(12)]
    tubo('Storia', pts, 0.015, materiale('Ramo', '#9aa4b5', 0.5))
    commit = materiale('Commit', '#e9c46a', 0.3, 0.6)
    for p in pts:
        bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=12, radius=0.07, location=p)
        assegna(liscio(bpy.context.object), commit)


def p11():
    """Provini sintetici nello spazio standardizzato di SiO2, CaO e FeO, con i centroidi delle tre litologie."""
    d = leggi('P11', 'dati/ml_v3.csv')
    cols = ['SiO2', 'CaO', 'FeO']
    stat = {}
    for c in cols:
        v = [float(r[c]) for r in d if r['split'] == 'train']
        m = sum(v) / len(v)
        s = (sum((x - m) ** 2 for x in v) / (len(v) - 1)) ** 0.5
        stat[c] = (m, s)
    colori = {'Arenaria': '#d9b26f', 'Basalto': '#4d5d78', 'Calcare': '#ece5d3'}
    mat = {k: materiale(k, v, 0.4) for k, v in colori.items()}
    cen = {k: materiale('Centroide ' + k, v, 0.2, 0.8, emissione=0.3) for k, v in colori.items()}
    sx, cx, cy, cz, rot = 0.78, 2.85, -0.4, -1.0, math.radians(32)
    gruppi = {}
    for r in d:
        z = [(float(r[c]) - stat[c][0]) / stat[c][1] for c in cols]
        u, w = sx * z[0], sx * z[2]
        p = (cx + u * math.cos(rot) - w * math.sin(rot), cy + u * math.sin(rot) + w * math.cos(rot), cz + sx * z[1])
        gruppi.setdefault(r['litologia'], []).append(p)
        bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=0.05 if r['split'] == 'train' else 0.075,
                                             location=p)
        assegna(liscio(bpy.context.object), mat[r['litologia']])
    for k, pts in gruppi.items():
        c = tuple(sum(p[i] for p in pts) / len(pts) for i in range(3))
        bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.16, location=c)
        assegna(liscio(bpy.context.object), cen[k])
    bpy.ops.mesh.primitive_cube_add(size=1, location=(cx, cy, cz), rotation=(0, 0, rot))
    box = bpy.context.object
    box.scale = (2.9, 2.6, 2.5)
    mod = box.modifiers.new('Spigoli', 'WIREFRAME')
    mod.thickness = 0.012
    assegna(box, materiale('Cornice', '#657180', 0.5, emissione=0.4))


SOGGETTI = {'P01': p01, 'P02': p02, 'P03': p03, 'P04': p04, 'P05': p05, 'P06': p06, 'P07': p07, 'P08': p08,
            'P09': p09, 'P10': p10, 'P11': p11}


def rendi(pid):
    sc = scena(pid)
    pianeta(pid)
    SOGGETTI[pid]()
    out = LEZIONI / CARTELLE[pid] / 'Scena'
    out.mkdir(parents=True, exist_ok=True)
    sc.render.image_settings.file_format = 'JPEG'
    sc.render.image_settings.quality = 88
    sc.render.filepath = str(out / 'copertina.jpg')
    bpy.ops.render.render(write_still=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out / 'copertina.blend'), compress=True)
    info = {'modulo': pid, 'motore': 'Blender Cycles', 'versione': bpy.app.version_string, 'pixel': [2400, 1500],
            'campioni': 16, 'seme': SEMI[pid], 'denoising': False, 'texture_esterne': [], 'immagini_IA': False}
    (out / 'render.json').write_text(json.dumps(info, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    args = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:]
    for pid in args or list(CARTELLE):
        rendi(pid)
