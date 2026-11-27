"""
WASHEEJ — The Invisible Order · CGI shots built procedurally in Blender (Cycles, CPU).
usage: python3 cgi/scene.py <shot> [--res 720] [--samples 24] [--frames a:b] [--still N]
shots: S04A (tunnel chase) · S04B (impact + frozen hold, slow creep) · S00 (same impact, crash zoom)
       S03D (capsule born from the phone screen) · S06 (one-take: the Washeej thread tests, snags, repairs, re-tests)
Art direction (from washeej.site + bible): graphite void, ivory glass, warm peach core #FED7B8, burgundy #59171B glow,
no neon, no code, no text. The thread is an ink-like fibre bundle, not a laser.
"""
import bpy, math, sys, os, random
from mathutils import Vector

ARGS = sys.argv[1:]
SHOT = ARGS[0]
def opt(k, d):
    return ARGS[ARGS.index(k) + 1] if k in ARGS else d
RES = int(opt('--res', 720)); SAMPLES = int(opt('--samples', 24))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS = 30

def hexc(h, a=1.0):
    h = h.lstrip('#'); c = [int(h[i:i+2], 16) / 255 for i in (0, 2, 4)]
    return tuple((x / 12.92) if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (a,)
PEACH, BURG, IVORY, GRAPH = hexc('FED7B8'), hexc('59171B'), hexc('F6EFE6'), hexc('0B0A0C')

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True; sc.cycles.use_adaptive_sampling = True; sc.cycles.adaptive_threshold = 0.04; sc.cycles.max_bounces = 6; sc.cycles.transmission_bounces = 6
sc.cycles.glossy_bounces = 3; sc.cycles.diffuse_bounces = 2; sc.cycles.caustics_reflective = False
sc.render.resolution_x = RES; sc.render.resolution_y = int(RES * 16 / 9); sc.render.fps = FPS
sc.render.use_motion_blur = True; sc.render.motion_blur_shutter = 0.22
sc.view_settings.view_transform = 'AgX'; sc.view_settings.look = 'AgX - Medium High Contrast'
sc.render.film_transparent = False
sc.render.use_overwrite = False
sc.view_settings.exposure = -0.3

# ---------- materials ----------
def mat_emit(name, col, strength):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission')
    e.inputs['Color'].default_value = col; e.inputs['Strength'].default_value = strength
    nt.links.new(e.outputs[0], o.inputs[0]); return m, e
def mat_glass(name, col, rough=0.02, ior=1.45):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); g = nt.nodes.new('ShaderNodeBsdfGlass')
    g.inputs['Color'].default_value = col; g.inputs['Roughness'].default_value = rough; g.inputs['IOR'].default_value = ior
    nt.links.new(g.outputs[0], o.inputs[0]); return m, g
def mat_mix_emit_transp(name, col, strength, alpha):
    m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); e = nt.nodes.new('ShaderNodeEmission'); t = nt.nodes.new('ShaderNodeBsdfTransparent')
    mx = nt.nodes.new('ShaderNodeMixShader'); e.inputs['Color'].default_value = col; e.inputs['Strength'].default_value = strength
    mx.inputs['Fac'].default_value = alpha
    nt.links.new(t.outputs[0], mx.inputs[1]); nt.links.new(e.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], o.inputs[0])
    return m, e, mx

def key(obj_or_socket, path, frame, value, interp='BEZIER'):
    setattr_path = path
    if hasattr(obj_or_socket, 'default_value') and path == 'default_value':
        obj_or_socket.default_value = value; obj_or_socket.keyframe_insert('default_value', frame=frame)
    else:
        target = obj_or_socket
        if isinstance(value, (tuple, list, Vector)):
            setattr(target, path, value)
        else:
            setattr(target, path, value)
        target.keyframe_insert(path, frame=frame)


def fcurves(idb):
    """Blender 5 slotted actions: collect fcurves of an ID's action."""
    ad = idb.animation_data
    if not ad or not ad.action: return []
    act = ad.action
    if hasattr(act, 'fcurves') and not hasattr(act, 'layers'): return list(act.fcurves)
    out = []
    for L in act.layers:
        for st in L.strips:
            cb = st.channelbag(ad.action_slot) if hasattr(st, 'channelbag') else None
            if cb: out += list(cb.fcurves)
    return out
def fcurve(idb, path, index):
    for fc in fcurves(idb):
        if fc.data_path == path and fc.array_index == index: return fc

# ---------- world ----------
w = bpy.data.worlds.new('W'); sc.world = w; w.use_nodes = True
bg = w.node_tree.nodes['Background']; bg.inputs['Color'].default_value = GRAPH; bg.inputs['Strength'].default_value = 1.0

# ---------- tunnel along -Y ----------
TUN_LEN = 120.0; TUN_R = 1.5
glass_tube, _ = mat_glass('tube', (0.92, 0.95, 1.0, 1), rough=0.06, ior=1.12)
bpy.ops.mesh.primitive_cylinder_add(vertices=96, radius=TUN_R, depth=TUN_LEN, location=(0, -TUN_LEN / 2 + 2, 0), rotation=(math.pi / 2, 0, 0))
tube = bpy.context.object; tube.name = 'tube'; tube.data.materials.append(glass_tube)
mod = tube.modifiers.new('solid', 'SOLIDIFY'); mod.thickness = 0.03
bpy.ops.object.shade_smooth()
for p in tube.data.polygons:
    if abs(p.normal.y) > 0.9: p.select = True
rib_mat, rib_emit = mat_emit('rib', hexc('E9DCCD'), 0.7)
RIBS = []
for i in range(0, int(TUN_LEN / 0.9)):
    y = 1.0 - i * 0.9
    bpy.ops.mesh.primitive_torus_add(major_radius=TUN_R + 0.02, minor_radius=0.005, major_segments=96, minor_segments=6,
                                     location=(0, y, 0), rotation=(math.pi / 2, 0, 0))
    r = bpy.context.object; r.data.materials.append(rib_mat); RIBS.append(r)
# faint long light lines along the tube (rails)
for a in (math.radians(30), math.radians(150), math.radians(270)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius=0.006, depth=TUN_LEN, location=(math.cos(a) * (TUN_R - 0.05), -TUN_LEN / 2 + 2, math.sin(a) * (TUN_R - 0.05)), rotation=(math.pi / 2, 0, 0))
    bpy.context.object.data.materials.append(rib_mat); RIBS.append(bpy.context.object)
END_Y = 2 - TUN_LEN   # where the tube ends
vol = bpy.data.materials.new('haze'); vol.use_nodes = True; vnt = vol.node_tree; vnt.nodes.remove(vnt.nodes['Principled BSDF'])
vs = vnt.nodes.new('ShaderNodeVolumeScatter'); vs.inputs['Density'].default_value = 0.012; vs.inputs['Color'].default_value = (0.8, 0.85, 1.0, 1)
vnt.links.new(vs.outputs[0], vnt.nodes['Material Output'].inputs['Volume'])
bpy.ops.mesh.primitive_cylinder_add(vertices=32, radius=TUN_R - 0.06, depth=TUN_LEN, location=(0, -TUN_LEN / 2 + 2, 0), rotation=(math.pi / 2, 0, 0))
bpy.context.object.data.materials.append(vol); bpy.context.object.name = 'haze'; bpy.context.object.hide_render = True
BARRIER_Y = END_Y - 6.0

# ---------- capsule ----------
def make_capsule(name='capsule'):
    shell_m = bpy.data.materials.new('shell'); shell_m.use_nodes = True; nt = shell_m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); gl = nt.nodes.new('ShaderNodeBsdfGlass'); gl.inputs['Roughness'].default_value = 0.02
    gl.inputs['IOR'].default_value = 1.33; gl.inputs['Color'].default_value = (1, 0.96, 0.92, 1)
    lw = nt.nodes.new('ShaderNodeLayerWeight'); lw.inputs['Blend'].default_value = 0.08
    em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Color'].default_value = PEACH; em.inputs['Strength'].default_value = 1.4
    ad = nt.nodes.new('ShaderNodeAddShader'); mx = nt.nodes.new('ShaderNodeMixShader')
    tr_ = nt.nodes.new('ShaderNodeBsdfTransparent')
    nt.links.new(lw.outputs['Facing'], mx.inputs[0]); nt.links.new(tr_.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2])
    nt.links.new(gl.outputs[0], ad.inputs[0]); nt.links.new(mx.outputs[0], ad.inputs[1]); nt.links.new(ad.outputs[0], o.inputs[0])
    core_m, core_e = mat_emit('core', hexc('FFB98A'), 5.0)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=0.22)
    shell = bpy.context.object; shell.name = name; shell.scale = (1, 1.75, 1); shell.data.materials.append(shell_m); bpy.ops.object.shade_smooth()
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32, ring_count=16, radius=0.075)
    core = bpy.context.object; core.scale = (1, 1.6, 1); core.data.materials.append(core_m); core.parent = shell
    rec_m, _ = mat_emit('receipt', IVORY, 2.0)
    bpy.ops.mesh.primitive_plane_add(size=0.12); rec = bpy.context.object; rec.scale = (0.6, 1.3, 1); rec.rotation_euler = (0.3, 0.2, 0.5)
    rec.data.materials.append(rec_m); rec.parent = shell
    li = bpy.data.lights.new('caplight', 'POINT'); li.energy = 0.0; li.color = PEACH[:3]; li.shadow_soft_size = 0.1
    lo = bpy.data.objects.new('caplight', li); sc.collection.objects.link(lo); lo.parent = shell
    # short light trail
    trail_m, _, _ = mat_mix_emit_transp('trail', PEACH, 6.0, 0.35)
    bpy.ops.mesh.primitive_cone_add(vertices=32, radius1=0.12, radius2=0.0, depth=1.6, location=(0, 0, 0), rotation=(-math.pi / 2, 0, 0))
    tr = bpy.context.object; tr.data.materials.append(trail_m); tr.parent = shell; tr.location = (0, 1.0, 0); tr.hide_render = True
    return shell, core_e, li, tr

def cam(name, lens=24):
    c = bpy.data.cameras.new(name); c.lens = lens; c.clip_start = 0.02; c.clip_end = 400
    c.dof.use_dof = True; c.dof.aperture_fstop = 2.0
    o = bpy.data.objects.new(name, c); sc.collection.objects.link(o); return o

def track_to(cam_obj, target):
    t = cam_obj.constraints.new('TRACK_TO'); t.target = target; t.track_axis = 'TRACK_NEGATIVE_Z'; t.up_axis = 'UP_Y'

# ---------- barrier ripple (invisible wall, only visible by refraction) ----------
def make_dust(y, n=420, seed=9):
    random.seed(seed); dm, _ = mat_emit('dust', hexc('DCD3CC'), 1.2)
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=0.006); proto = bpy.context.object; proto.data.materials.append(dm)
    for i in range(n):
        o = proto.copy(); sc.collection.objects.link(o)
        o.location = (random.uniform(-3, 3), y - random.uniform(0.5, 9), random.uniform(-4, 4)); s = random.uniform(0.5, 2.2); o.scale = (s, s, s)
def make_barrier(y):
    make_dust(y)
    m = bpy.data.materials.new('barrier'); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    o = nt.nodes.new('ShaderNodeOutputMaterial'); g = nt.nodes.new('ShaderNodeBsdfGlass'); g.inputs['IOR'].default_value = 1.0
    g.inputs['Roughness'].default_value = 0.0; g.inputs['Color'].default_value = (1, 1, 1, 1)
    nt.links.new(g.outputs[0], o.inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=8, location=(0, y, 0), rotation=(math.pi / 2, 0, 0))
    p = bpy.context.object; p.name = 'barrier'; p.data.materials.append(m)
    sub = p.modifiers.new('sub', 'SUBSURF'); sub.subdivision_type = 'SIMPLE'; sub.levels = 6; sub.render_levels = 6
    tex = bpy.data.textures.new('ripple', 'WOOD'); tex.wood_type = 'RINGNOISE'; tex.noise_basis_2 = 'SIN'; tex.turbulence = 0.0
    tex.noise_scale = 0.35
    d = p.modifiers.new('disp', 'DISPLACE'); d.texture = tex; d.strength = 0.0; d.texture_coords = 'LOCAL'
    return p, g, d, tex

# ---------- shards ----------
def make_shards(center, n=26, seed=3):
    random.seed(seed); sm, _ = mat_emit('shard', PEACH, 5.0); objs = []
    for i in range(n):
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=random.uniform(0.003, 0.012))
        s = bpy.context.object; s.data.materials.append(sm)
        v = Vector((random.uniform(-1, 1), random.uniform(0.0, 0.6), random.uniform(-1, 1))).normalized() * random.uniform(0.15, 0.9)
        s['dir'] = v[:]; s.location = center; s.scale = (1, random.uniform(1, 3), 1); objs.append(s)
    return objs

def out_path(shot):
    d = os.path.join(ROOT, 'cgi', 'frames', shot); os.makedirs(d, exist_ok=True); return os.path.join(d, 'f_')

# =====================================================================================
if SHOT in ('S04A', 'S04B', 'S00'):
    cap, core_e, caplight, trail = make_capsule()
    barrier, bglass, bdisp, btex = make_barrier(BARRIER_Y)
    hit = Vector((0, BARRIER_Y + 0.42, 0))
    shards = make_shards(hit)
    if SHOT == 'S04A':
        # 2.4s chase: capsule flies at speed, tunnel ends ahead in darkness
        N = 72; sc.frame_start, sc.frame_end = 1, N
        y0, y1 = -60.0, END_Y + 3.0
        for f, y in ((1, y0), (N, y1)):
            cap.location = (0, y, 0); cap.keyframe_insert('location', frame=f)
        c = cam('cam', 20); sc.camera = c
        for f, y in ((1, y0 + 2.2), (N, y1 + 1.6)):
            c.location = (0.55, y, 0.3); c.keyframe_insert('location', frame=f)
        track_to(c, cap); c.data.dof.focus_object = cap
        for fc in fcurves(cap) + fcurves(c):
            for k in fc.keyframe_points: k.interpolation = 'LINEAR'
        # camera shake (subtle)
        n = fcurve(c, 'location', 0).modifiers.new('NOISE'); n.scale = 6; n.strength = 0.03
    else:
        # Impact timeline (frames @30): approach 1..30, impact at 30, freeze & dim, slow creep to end
        N = 150 if SHOT == 'S04B' else 45; sc.frame_start, sc.frame_end = 1, N
        IMP = 30
        cap.location = (0, END_Y + 8.0, 0); cap.keyframe_insert('location', frame=1)
        cap.location = hit; cap.keyframe_insert('location', frame=IMP)
        cap.location = hit + Vector((0, 0.04, 0)); cap.keyframe_insert('location', frame=IMP + 4)   # tiny recoil, then suspended
        cap.location = hit + Vector((0, 0.05, 0)); cap.keyframe_insert('location', frame=N)
        for k in fcurve(cap, 'location', 1).keyframe_points: k.interpolation = 'LINEAR'
        cap.rotation_euler = (0, 0, 0); cap.keyframe_insert('rotation_euler', frame=IMP)
        cap.rotation_euler = (0.0, 0.25, 0.06); cap.keyframe_insert('rotation_euler', frame=N)
        # core dims after the hit
        core_e.inputs['Strength'].default_value = 5; core_e.inputs['Strength'].keyframe_insert('default_value', frame=IMP)
        core_e.inputs['Strength'].default_value = 14; core_e.inputs['Strength'].keyframe_insert('default_value', frame=IMP + 1)
        core_e.inputs['Strength'].default_value = 1.8; core_e.inputs['Strength'].keyframe_insert('default_value', frame=N)
        caplight.energy = 0; caplight.keyframe_insert('energy', frame=IMP); caplight.energy = 0; caplight.keyframe_insert('energy', frame=N)
        # trail vanishes on impact
        trail.scale = (1, 1, 1); trail.keyframe_insert('scale', frame=IMP - 1); trail.scale = (0.01, 0.01, 0.01); trail.keyframe_insert('scale', frame=IMP + 2)
        # ripple: ring displacement expands then freezes
        bdisp.strength = 0.0; bdisp.keyframe_insert('strength', frame=IMP)
        bdisp.strength = 0.09; bdisp.keyframe_insert('strength', frame=IMP + 3)
        bdisp.strength = 0.06; bdisp.keyframe_insert('strength', frame=N)
        btex.noise_scale = 0.08; btex.keyframe_insert('noise_scale', frame=IMP)
        btex.noise_scale = 0.32; btex.keyframe_insert('noise_scale', frame=IMP + 8)
        btex.noise_scale = 0.34; btex.keyframe_insert('noise_scale', frame=N)
        bglass.inputs['IOR'].default_value = 1.0; bglass.inputs['IOR'].keyframe_insert('default_value', frame=IMP)
        bglass.inputs['IOR'].default_value = 1.08; bglass.inputs['IOR'].keyframe_insert('default_value', frame=IMP + 2)
        # shards burst then hang (near-frozen drift)
        for s in shards:
            d = Vector(s['dir'])
            s.scale = (0.001,) * 3; s.keyframe_insert('scale', frame=IMP - 1)
            s.scale = (1, 2, 1); s.keyframe_insert('scale', frame=IMP)
            s.location = hit; s.keyframe_insert('location', frame=IMP)
            s.location = hit + d * 0.85; s.keyframe_insert('location', frame=IMP + 5)
            s.location = hit + d * 1.0; s.keyframe_insert('location', frame=N)
        c = cam('cam', 24 if SHOT == 'S04B' else 22); sc.camera = c
        if SHOT == 'S04B':
            # chase in, then the camera keeps creeping very slowly toward the frozen capsule
            c.location = (1.0, END_Y + 9.2, 0.22); c.keyframe_insert('location', frame=1)
            c.location = (0.95, hit.y + 1.3, 0.3); c.keyframe_insert('location', frame=IMP + 2)
            c.location = (0.62, hit.y + 1.0, 0.2); c.keyframe_insert('location', frame=N)
        else:
            # cold open: fast FPV, impact, violent but controlled crash zoom into the capsule
            c.location = (0.2, END_Y + 12.0, 0.2); c.keyframe_insert('location', frame=1)
            c.location = (0.26, hit.y + 1.7, 0.2); c.keyframe_insert('location', frame=IMP + 1)
            c.data.lens = 22; c.data.keyframe_insert('lens', frame=IMP + 2)
            c.data.lens = 70; c.data.keyframe_insert('lens', frame=IMP + 9)
            c.location = (0.18, hit.y + 0.95, 0.12); c.keyframe_insert('location', frame=IMP + 9)
            c.location = (0.18, hit.y + 0.92, 0.12); c.keyframe_insert('location', frame=N)
        track_to(c, cap); c.data.dof.focus_object = cap
    # fill/rim lights
    for loc, col, en in (((2.5, END_Y - 2, 2.5), (0.75, 0.85, 1.0), 400), ((-3, END_Y + 4, -1.5), (0.7, 0.8, 1.0), 250)):
        l = bpy.data.lights.new('fill', 'AREA'); l.energy = en; l.color = col; l.size = 2
        lo = bpy.data.objects.new('fill', l); lo.location = loc; lo.visible_camera = False; lo.visible_transmission = False; sc.collection.objects.link(lo); track_to(lo, cap)

# =====================================================================================
elif SHOT == 'S03D':
    # the capsule is born from the success screen, rises, accelerates and becomes a pinpoint
    N = 48; sc.frame_start, sc.frame_end = 1, N
    tube.hide_render = True
    for r in RIBS: r.hide_render = True
    scr = bpy.data.materials.new('screen'); scr.use_nodes = True; nt = scr.node_tree
    img = bpy.data.images.load(os.path.join(ROOT, 'gen', 'frames', 'success_screen.png'))
    tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img; em = nt.nodes.new('ShaderNodeEmission'); em.inputs['Strength'].default_value = 2.2
    nt.links.new(tx.outputs[0], em.inputs[0]); nt.links.new(em.outputs[0], nt.nodes['Material Output'].inputs[0])
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0)); s = bpy.context.object; s.scale = (0.7, 1.52, 1); s.data.materials.append(scr)
    body_m = bpy.data.materials.new('body'); body_m.use_nodes = True
    body_m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (0.012, 0.012, 0.014, 1)
    body_m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value = 0.25
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, -0.03)); b = bpy.context.object; b.scale = (0.76, 1.58, 0.05); b.data.materials.append(body_m)
    bev = b.modifiers.new('bev', 'BEVEL'); bev.width = 0.06; bev.segments = 6
    cap, core_e, caplight, trail = make_capsule()
    cap.rotation_euler = (math.pi / 2, 0, 0)
    cap.scale = (0.01, 0.01, 0.01); cap.location = (0, -0.35, 0.02); cap.keyframe_insert('scale', frame=1); cap.keyframe_insert('location', frame=1)
    cap.scale = (1, 1.75, 1); cap.keyframe_insert('scale', frame=12)
    cap.location = (0, -0.35, 0.55); cap.keyframe_insert('location', frame=14)
    cap.location = (0, -0.1, 9.0); cap.keyframe_insert('location', frame=N)
    c = cam('cam', 28); sc.camera = c
    c.location = (0.9, -1.9, 1.4); c.keyframe_insert('location', frame=1)
    c.location = (0.5, -1.4, 2.4); c.keyframe_insert('location', frame=N)
    track_to(c, cap); c.data.dof.focus_object = cap
    warm = bpy.data.lights.new('lamp', 'AREA'); warm.energy = 60; warm.color = (1.0, 0.72, 0.45); warm.size = 3
    wl = bpy.data.objects.new('lamp', warm); wl.location = (2.5, 1.5, 2.5); sc.collection.objects.link(wl); track_to(wl, s)
    bg.inputs['Color'].default_value = hexc('120D0C')

# =====================================================================================
elif SHOT == 'S06':
    # One-take, 13.6s (408f). Thread enters, tests 4 junctions (rings), snags at the barrier (server), repairs (stitch + knot),
    # a pulse re-tests the whole path, and the light turns warm. Timings mirror GFX_06_journey (overlay starts 0.2s in).
    N = 408; sc.frame_start, sc.frame_end = 1, N
    cap, core_e, caplight, trail = make_capsule(); trail.hide_render = True
    BAR = END_Y - 6.0
    barrier, bglass, bdisp, btex = make_barrier(BAR); bdisp.strength = 0.05; btex.noise_scale = 0.33; bglass.inputs['IOR'].default_value = 1.06
    cap.location = (0, BAR + 0.42, 0); core_e.inputs['Strength'].default_value = 1.8
    # junction nodes: product, cart, submit, server(barrier), dashboard (beyond)
    JY = [END_Y + 60, END_Y + 40, END_Y + 20, BAR + 0.1, BAR - 14]
    node_m = []
    for i, y in enumerate(JY):
        m, e = mat_emit(f'node{i}', IVORY, 0.6); node_m.append(e)
        bpy.ops.mesh.primitive_torus_add(major_radius=0.55 if i != 3 else 0.9, minor_radius=0.025, major_segments=96, minor_segments=12,
                                         location=(0, y, 0), rotation=(math.pi / 2, 0, 0))
        bpy.context.object.data.materials.append(m)
    # thread path: a gentle helix along -Y passing through every node center
    pts = []
    y = JY[0] + 14
    while y > JY[-1] - 2:
        a = (y * 0.35)
        rr = 0.35 * min(1, min(abs(y - j) for j in JY) / 3.0)   # pinch to the centre at each node
        pts.append(Vector((math.cos(a) * rr, y, math.sin(a) * rr))); y -= 0.25
    def make_curve(name, offs, bevel, mat):
        cu = bpy.data.curves.new(name, 'CURVE'); cu.dimensions = '3D'; cu.bevel_depth = bevel; cu.bevel_resolution = 3; cu.use_fill_caps = True
        sp = cu.splines.new('POLY'); sp.points.add(len(pts) - 1)
        for k, p in enumerate(pts):
            j = math.sin(k * 0.37 + offs * 3.1) * 0.012 * (1 if offs else 0)
            sp.points[k].co = (p.x + offs * 0.6 + j, p.y, p.z + offs * 0.4 - j, 1)
        ob = bpy.data.objects.new(name, cu); sc.collection.objects.link(ob); cu.materials.append(mat); return ob, cu
    core_m, core_emit = mat_emit('thread_core', PEACH, 9.0)
    halo_m, halo_emit, halo_mix = mat_mix_emit_transp('thread_halo', hexc('8F2A31'), 5.0, 0.35)
    fib_m, fib_emit = mat_emit('thread_fib', PEACH, 5.0)
    threads = [make_curve('core', 0, 0.0055, core_m)]
    for k in range(7):
        threads.append(make_curve(f'fib{k}', (k - 3) * 0.022, 0.0016, fib_m))
    pulse_m, pulse_e = mat_emit('pulse', hexc('FFF1E4'), 60.0)
    pulse, pcu = make_curve('pulse', 0, 0.011, pulse_m)
    total = len(pts)
    def s_at(y):  # 0..1 along path for a given y
        return max(0.0, min(1.0, (pts[0].y - y) / (pts[0].y - pts[-1].y)))
    # head timeline (frames) — overlay t + 0.2s
    K = [(1, s_at(JY[0] + 14)), (48, s_at(JY[0])), (108, s_at(JY[1])), (174, s_at(JY[2])), (258, s_at(JY[3]))]
    for ob, cu in threads:
        cu.bevel_factor_mapping_end = 'SPLINE'
        for f, v in K:
            cu.bevel_factor_end = v; cu.keyframe_insert('bevel_factor_end', frame=f)
        cu.bevel_factor_end = s_at(JY[3]); cu.keyframe_insert('bevel_factor_end', frame=330)   # held at the snag until repair
        cu.bevel_factor_end = 1.0; cu.keyframe_insert('bevel_factor_end', frame=375)
    # pulse re-test: a bright short segment races along the whole path 330→375
    pcu.bevel_factor_mapping_start = pcu.bevel_factor_mapping_end = 'SPLINE'
    for f, a_ in ((1, 0.0), (330, 0.0), (375, 0.97)):
        pcu.bevel_factor_start = a_; pcu.keyframe_insert('bevel_factor_start', frame=f)
        pcu.bevel_factor_end = min(1.0, a_ + (0.03 if f >= 330 else 0.0)); pcu.keyframe_insert('bevel_factor_end', frame=f)
    pulse.hide_render = True; pulse.keyframe_insert('hide_render', frame=329); pulse.hide_render = False; pulse.keyframe_insert('hide_render', frame=330)
    pulse.hide_render = True; pulse.keyframe_insert('hide_render', frame=378)
    # snag tremor
    for ob, cu in threads:
        ob.location = (0, 0, 0); ob.keyframe_insert('location', frame=258)
        fc = fcurve(ob, 'location', 0); n = fc.modifiers.new('NOISE'); n.scale = 1.5; n.strength = 0.0
        n.use_restricted_range = True; n.frame_start = 262; n.frame_end = 300; n.blend_in = 4; n.blend_out = 6; n.strength = 0.02
    # junctions light up as the head passes; server goes red-ish dim, then warm after repair
    for i, e in enumerate(node_m):
        fpass = [48, 108, 174, 258, 372][i]
        e.inputs['Strength'].default_value = 0.6; e.inputs['Strength'].keyframe_insert('default_value', frame=fpass - 2)
        e.inputs['Color'].default_value = IVORY; e.inputs['Color'].keyframe_insert('default_value', frame=fpass - 2)
        if i == 3:
            e.inputs['Color'].default_value = hexc('C23A3F'); e.inputs['Color'].keyframe_insert('default_value', frame=fpass)
            e.inputs['Strength'].default_value = 6; e.inputs['Strength'].keyframe_insert('default_value', frame=fpass)
            e.inputs['Color'].default_value = PEACH; e.inputs['Color'].keyframe_insert('default_value', frame=306)
        else:
            e.inputs['Color'].default_value = PEACH; e.inputs['Color'].keyframe_insert('default_value', frame=fpass)
            e.inputs['Strength'].default_value = 8; e.inputs['Strength'].keyframe_insert('default_value', frame=fpass)
    # repair: barrier ripple flattens and turns to warm light; capsule brightens and moves on to the dashboard
    bdisp.keyframe_insert('strength', frame=300); bdisp.strength = 0.0; bdisp.keyframe_insert('strength', frame=330)
    bglass.inputs['IOR'].keyframe_insert('default_value', frame=300); bglass.inputs['IOR'].default_value = 1.0; bglass.inputs['IOR'].keyframe_insert('default_value', frame=326)
    core_e.inputs['Strength'].keyframe_insert('default_value', frame=306); core_e.inputs['Strength'].default_value = 9; core_e.inputs['Strength'].keyframe_insert('default_value', frame=330)
    cap.keyframe_insert('location', frame=330); cap.location = (0, JY[4] + 0.6, 0); cap.keyframe_insert('location', frame=380)
    # stitch knot at the server node
    bpy.ops.curve.primitive_bezier_circle_add(radius=0.16, location=(0, JY[3] + 0.02, 0), rotation=(math.pi / 2, 0, 0))
    knot = bpy.context.object; knot.data.bevel_depth = 0.01; knot.data.materials.append(core_m)
    knot.data.bevel_factor_end = 0.0; knot.data.keyframe_insert('bevel_factor_end', frame=300)
    knot.data.bevel_factor_end = 1.0; knot.data.keyframe_insert('bevel_factor_end', frame=318)
    # world warms up from graphite to deep burgundy-brown during the repair
    bg.inputs['Color'].default_value = GRAPH; bg.inputs['Color'].keyframe_insert('default_value', frame=300)
    bg.inputs['Color'].default_value = hexc('2A0E10'); bg.inputs['Color'].keyframe_insert('default_value', frame=380)
    rib_emit.inputs['Color'].keyframe_insert('default_value', frame=300); rib_emit.inputs['Color'].default_value = PEACH
    rib_emit.inputs['Color'].keyframe_insert('default_value', frame=380)
    # camera: one continuous move riding just behind/beside the thread head, orbit at the knot, whip along the pulse
    c = cam('cam', 22); sc.camera = c
    tgt = bpy.data.objects.new('tgt', None); sc.collection.objects.link(tgt)
    def head_y(f):
        for (f0, v0), (f1, v1) in zip(K, K[1:]):
            if f0 <= f <= f1: return pts[0].y - (v0 + (v1 - v0) * (f - f0) / (f1 - f0)) * (pts[0].y - pts[-1].y)
        return JY[3]
    for f in range(1, N + 1, 6):
        if f <= 258: hy = head_y(f); cl = (0.75, hy + 2.6, 0.45); tl = (0, hy - 0.6, 0)
        elif f <= 330:
            a = (f - 258) / 72 * math.pi * 0.9; hy = JY[3]
            cl = (math.cos(a) * 1.4, hy + 0.9 + math.sin(a) * 0.4, math.sin(a) * 1.0 + 0.2); tl = (0, hy, 0)
        else:
            u = min(1, (f - 330) / 45); hy = JY[3] + (JY[4] - JY[3]) * u
            cl = (0.6, hy + 2.0, 0.35); tl = (0, hy - 1.0, 0)
        c.location = cl; c.keyframe_insert('location', frame=f); tgt.location = tl; tgt.keyframe_insert('location', frame=f)
    track_to(c, tgt); c.data.dof.use_dof = False
    for loc, en in (((2, JY[3] + 3, 2), 300), ((-2, JY[1], -1), 200)):
        l = bpy.data.lights.new('fill', 'AREA'); l.energy = en; l.color = (0.85, 0.88, 1.0); l.size = 3
        lo = bpy.data.objects.new('fill', l); lo.location = loc; lo.visible_camera = False; lo.visible_transmission = False; sc.collection.objects.link(lo); track_to(lo, cap)

# ---------- compositor: soft bloom + grain-free (grain added in conform) ----------
sc.use_nodes = True
tree = sc.node_tree if hasattr(sc, 'node_tree') and sc.node_tree else None
try:
    nt = sc.compositing_node_group if hasattr(sc, 'compositing_node_group') else None
except Exception:
    nt = None

sc.render.image_settings.file_format = 'PNG'
sc.render.filepath = out_path(SHOT)
if '--still' in ARGS:
    sc.frame_set(int(opt('--still', 1))); sc.render.filepath = os.path.join(ROOT, 'cgi', f'still_{SHOT}.png')
    bpy.ops.render.render(write_still=True)
else:
    fr = opt('--frames', None)
    if fr: a, b = fr.split(':'); sc.frame_start, sc.frame_end = int(a), int(b)
    sc.frame_step = int(opt('--step', 1))
    bpy.ops.render.render(animation=True)
print('DONE', SHOT)
