"""«VINCE VELOUR'S GUIDE TO 1986» — 16:9 extended version: timeline built from a list of beats.
  ('v', key, shot, kw)      a new movie line (voice/movie_t/<key>.mp3) over shot `shot`
  ('vr', ep, key, shot, kw) a reused line from an episode take (voice/<ep>_t/<key>.mp3)
  ('clip', ep, a, b, kw)    a piece of an episode (final.mp4 a..b s) on the studio screen; kw audio=False mutes it (new VO over it)
  ('beat', dur, shot, kw)   a visual/SFX beat without dialogue
Every beat becomes a SHOT (t0, t1, name, kw); clips also add their audio to SFX."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'episodes'))
import common as CM

FPS = 30
SLUG = 'still-1986'
LUFS = -14.0
GAP = 0.12

B = [
    # ---------------- COLD OPEN
    ('beat', 1.0, 'play', {}),
    ('v', 'h1', 'host_wide', dict(push=True)),
    ('v', 'fh1', 'fran_cu', {}),
    ('v', 'h2', 'host_cu', dict(expr='smooth', arms=True)),
    ('beat', 1.6, 'audience', {}),
    ('v', 'fh2', 'fran_cu', {}),
    ('v', 'h3', 'host_cu', dict(expr='cool', point=True)),
    ('beat', 4.2, 'title', {}),
    # ---------------- LESSON 1: PARKING
    ('v', 'l1', 'host_wide', dict(board='LESSON 1: PARKING')),
    ('clip', 'ep01', 3.98, 10.75, {}),
    ('v', 'l2', 'host_cu', dict(expr='scheming')),
    ('clip', 'ep01', 14.42, 25.55, {}),
    ('v', 'l3', 'host_cu', dict(expr='ecstatic')),
    ('clip', 'ep01', 25.58, 38.75, {}),
    ('v', 'l4', 'host_cu', dict(expr='proudsad')),
    ('v', 'fl1', 'fran_cu', {}),
    ('beat', 0.8, 'reveal_tow', {}),
    ('v', 'rl1', 'reveal_tow', {}),
    # ---------------- AD 1: REY'S TOWING
    ('beat', 0.7, 'adcard', dict(text='COMMERCIAL BREAK')),
    ('v', 'rc1', 'ad_rey', dict(stage=0)),
    ('v', 'rc2', 'ad_rey', dict(stage=1)),
    ('v', 'xc1', 'ad_rey', dict(stage=2)),
    # ---------------- LESSON 2: MONEY
    ('v', 'm1', 'host_wide', dict(board='LESSON 2: MONEY')),
    ('clip', 'ep02', 3.27, 20.30, {}),
    ('clip', 'ep02', 22.51, 32.40, {}),
    ('v', 'm2', 'host_cu', dict(expr='smooth')),
    ('clip', 'ep03', 3.95, 10.40, {}),
    ('clip', 'ep03', 15.60, 19.00, {}),
    ('clip', 'ep03', 22.09, 34.00, {}),
    ('v', 'm3', 'host_cu', dict(expr='proudsad')),
    ('v', 'fm1', 'fran_cu', {}),
    # ---------------- AD 2: ROOF-E PREMIUM
    ('beat', 0.7, 'adcard', dict(text='COMMERCIAL BREAK')),
    ('v', 'xr1', 'ad_roof', dict(stage=0)),
    ('v', 'xr2', 'ad_roof', dict(stage=1)),
    ('v', 'xr3', 'ad_roof', dict(stage=2)),
    # ---------------- LESSON 4: STYLE
    ('v', 's1', 'host_wide', dict(board='LESSON 4: STYLE')),
    ('clip', 'ep05', 2.40, 14.85, {}),
    ('clip', 'ep05', 19.10, 27.10, {}),
    ('v', 's2', 'host_cu', dict(expr='proudsad')),
    # ---------------- CALL-IN
    ('v', 'c1', 'host_wide', dict(board='LIVE CALL-IN', phone=True)),
    ('v', 'tc1', 'caller', dict(who='tiffany', src=('ep02', 3.30, 4.80))),
    ('v', 'c2', 'host_cu', dict(expr='nervous', phone=True)),
    ('v', 'gc1', 'caller', dict(who='gary', src=('ep04', 3.70, 6.00))),
    ('v', 'c3', 'host_cu', dict(expr='nervous', phone=True, cough=True)),
    ('v', 'c4', 'host_cu', dict(expr='outraged', phone=True)),
    ('v', 'dc1', 'caller', dict(who='diaz', src=('ep03', 30.40, 33.00))),
    ('v', 'c5', 'host_cu', dict(expr='defeated', phone=True, tears=True)),
    ('v', 'fc1', 'fran_cu', dict(phone=True)),
    ('beat', 1.6, 'fax', {}),
    # ---------------- LESSON 5: CAREER
    ('v', 'k1', 'host_cu', dict(expr='scheming', board='LESSON 5: CAREER')),
    ('clip', 'ep04', 8.86, 27.30, {}),
    ('v', 'k2', 'host_cu', dict(expr='smooth')),
    # ---------------- LESSON 3: PATIENCE
    ('v', 'd1', 'host_wide', dict(board='LESSON 3: PATIENCE (LATE)')),
    ('clip', 'ep06', 3.00, 17.10, {}),
    ('clip', 'ep06', 19.55, 25.40, {}),
    ('v', 'd2', 'host_cu', dict(expr='tired')),
    # ---------------- FINALE: THE TAPE
    ('v', 'f1', 'host_cu', dict(expr='smooth', freeze_at=3.6)),
    ('v', 'xf1', 'bluescreen', dict(line=0)),
    ('v', 'f2', 'host_cu', dict(expr='outraged', kick=True)),
    ('v', 'xf2', 'bluescreen', dict(line=1)),
    ('vr', 'ep01', 'v4', 'host_cu', dict(expr='outraged', kick=True, zoom=1.25)),
    ('v', 'ff1', 'fran_cu', {}),
    ('v', 'f4', 'host_cu', dict(expr='proudsad', shades_off=True, zoom=1.1)),
    ('beat', 1.6, 'rewind', {}),
    ('beat', 3.2, 'endcard', {}),
]

CM.EP = 'movie'
VOICE, SHOTS, CLIPS, SFX_CLIPS = [], [], [], []
t = 0.0
for b in B:
    kind = b[0]
    if kind in ('v', 'vr'):
        if kind == 'v':
            key, shot, kw = b[1], b[2], b[3]; ep = 'movie'
        else:
            ep, key, shot, kw = b[1], b[2], b[3], b[4]
        d = CM.dur(ep, key)
        vid = key if ep == 'movie' else f'{key}_{ep}'
        VOICE.append((vid, f'{ep}_t', key, round(t, 2), 0.0, round(d, 2), _who := None, ''))
        SHOTS.append([round(t, 2), round(t + d + GAP, 2), shot, dict(kw, line=vid)])
        t += d + GAP
    elif kind == 'clip':
        ep, a, bb, kw = b[1], b[2], b[3], b[4]
        d = bb - a
        SHOTS.append([round(t, 2), round(t + d, 2), 'screen', dict(kw, ep=ep, a=a)])
        if kw.get('audio', True): SFX_CLIPS.append((f'series/{SLUG}/episodes/{ep}/final.mp4', round(t, 2), 1.0, a, bb))
        t += d
    elif kind == 'beat':
        d, shot, kw = b[1], b[2], b[3]
        SHOTS.append([round(t, 2), round(t + d, 2), shot, kw])
        t += d
DUR = round(t, 2)

# speaker + text for captions, from the lines files
import json, pathlib as _p
_L = {('movie', k): v for k, v in json.load(open(_p.Path(__file__).resolve().parents[1] / 'voice' / 'movie' / 'lines.json')).items()}
_L.update({('ep01', k): v for k, v in json.load(open(_p.Path(__file__).resolve().parents[1] / 'voice' / 'ep01' / 'lines.json')).items()})
import re
VOICE = [(vid, vep, key, t0, a, b_, _L[(vep[:-2], key)][0], re.sub(r'\[[^\]]*\]\s*', '', _L[(vep[:-2], key)][1]).strip())
         for (vid, vep, key, t0, a, b_, _w, _x) in VOICE]
CUTS = [s[0] for s in SHOTS] + [DUR]
NAMES = [f'{i:02d}_{s[2]}' for i, s in enumerate(SHOTS)]
TWIST = next(s[0] for s in SHOTS if s[2] == 'bluescreen')
CH = [(0.0, 'Lesson 1: Parking'), (next(s[0] for s in SHOTS if s[3].get('board') == 'LIVE CALL-IN'), 'Live Call-In'),
      (next(s[0] for s in SHOTS if s[3].get('freeze_at')), 'The Tape')]

X = 'series/still-1986/sfx/'
L = 'library/cc0/sfx/'
SFX = list(SFX_CLIPS)
prev = None
for s in SHOTS:
    t0, t1, name, kw = s
    if name == 'play': SFX.append((X + 'vhs_insert.mp3', t0, 0.8))
    if name == 'title': SFX += [(X + 'sax_fantasy.mp3', t0 + 0.2, 0.6), (L + 'whoosh_1.mp3', t0, 0.5)]
    if name == 'audience': SFX += [(X + 'crickets_studio.mp3', t0 + 0.15, 0.9), (X + 'lonely_clap.mp3', t0 + 0.7, 0.8)]
    if name == 'reveal_tow' and kw.get('line') is None: SFX += [(X + 'tow_winch.mp3', t0, 0.6), (L + 'vinyl_scratch.mp3', t0 - 0.4, 0.45)]
    if name == 'adcard': SFX += [(L + 'whoosh_3.mp3', t0, 0.5), (X + 'crt_on.mp3', t0, 0.35)]
    if name == 'ad_rey' and kw.get('stage') == 1: SFX.append((X + 'tow_winch.mp3', t0 + 0.2, 0.5))
    if name == 'ad_rey' and kw.get('stage') == 2: SFX.append((X + 'register.mp3', t0 + 0.4, 0.45))
    if name == 'ad_roof' and kw.get('stage') == 0: SFX.append((X + 'rain_loop.mp3', t0, 0.55, 0.0, t1 - t0))
    if name == 'ad_roof' and kw.get('stage') == 1: SFX += [(X + 'roof_motor.mp3', t0, 0.6), (X + 'car_chime.mp3', t0 + 1.2, 0.4)]
    if name == 'ad_roof' and kw.get('stage') == 2: SFX.append((X + 'sax_fantasy.mp3', t0 + 0.1, 0.45))
    if name == 'caller': SFX += [(X + 'ringtone.mp3', t0 - 0.9, 0.35), (L + 'phone_key_click.mp3', t0, 0.5)]
    if name == 'fran_cu': SFX.append((X + 'neon_on.mp3', t0, 0.25))
    if name == 'fax': SFX += [(X + 'fax_print.mp3', t0, 0.7), (X + 'register.mp3', t0 + 0.5, 0.5)]
    if name == 'bluescreen' and kw.get('line') == 'xf1': SFX += [(L + 'vinyl_scratch.mp3', t0 - 0.6, 0.6), (X + 'car_chime.mp3', t0 + 0.1, 0.7)]
    if name == 'bluescreen' and kw.get('line') == 'xf2': SFX.append((X + 'register.mp3', t0 + 0.3, 0.55))
    if name == 'rewind': SFX += [(L + 'whoosh_1.mp3', t0, 0.6), (L + 'whoosh_3.mp3', t0 + 0.6, 0.5)]
    if name == 'endcard': SFX.append((X + 'app_ding.mp3', t0 + 0.1, 0.5))
    if name == 'screen' and prev != 'screen': SFX += [(X + 'crt_on.mp3', t0, 0.3), (L + 'whoosh_1.mp3', t0 - 0.1, 0.25)]
    if name != 'screen' and prev == 'screen': SFX.append((L + 'whoosh_3.mp3', t0 - 0.1, 0.25))
    if kw.get('board'): SFX.append((L + 'chair_creak.mp3', t0 + 0.4, 0.3))
    if kw.get('arms') or kw.get('point') or kw.get('shades_off'): SFX.append((L + 'cloth_rustle.mp3', t0 + 0.2, 0.35))
    if kw.get('kick'): SFX.append((L + 'boing_cartoon.mp3', t0 + 0.3, 0.25))
    prev = name


def _host_spans():
    out, cur = [], None
    for t0, t1, name, kw in SHOTS:
        host = name != 'screen'
        if host and cur is None: cur = t0
        if not host and cur is not None: out.append((cur, t0)); cur = None
    if cur is not None: out.append((cur, DUR))
    return out


BEDS = [(CM.MUSIC, 15.0, a, b, 0.12, True, CM.MUSIC_DIP) for a, b in _host_spans() if b - a > 1.0]
VGAIN, VFX = CM.VGAIN, CM.VFX
