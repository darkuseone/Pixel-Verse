"""Shared building blocks of «Ключевой сотрудник» episodes made to the reference E01 v2.1 / E02 v2 (standard «голливудский уровень»):
voice timing from the tightened takes, faces, the no-blur shot, real-scale floor actors, close-ups, the ficus close-up as a real camera
move onto the windowsill, inserts (calculator, phone chat, calendar, printer sheet), on-screen tallies.
Usage in epNN.py:  import kscommon as KC;  E = KC.Ep('ep03', ORDER, gaps={...}, endcard_promise='ЗАВТРА: …')"""
import sys, pathlib, subprocess, math
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from stage import OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import kscast as C
from props import kskit as K
from props import mimic as M
from props.kskit import at, aout

SLUG = 'klyuchevoy'
WHO = dict(s='shef', e='edik', f='fikus', l='lyuda')
WS_SILL = 2.9
SILL = (1040.0, 372.0)
TAB = (C.XTRA, C.EXPR)


def dur(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(path)],
                         capture_output=True, text=True).stdout
    return max(0.3, float(out) - 0.05)


def timing(vep, order, gap=0.06, gaps=None, texts=None):
    """VOICE list + start times: lines one after another (gap s), gaps={key: extra pause before the line} for visual beats"""
    gaps = gaps or {}
    vdir = ROOT / 'series' / SLUG / 'voice' / f'{vep}_t'
    t = 0.0; V = []; T0 = {}
    for i, k in enumerate(order):
        if i: t += gap + gaps.get(k, 0.0)
        d = dur(vdir / f'{k}.mp3')
        T0[k] = round(t, 2)
        V.append((k, f'{vep}_t', k, T0[k], 0.0, round(d, 2), WHO[k[0]], (texts or {}).get(k, '')))
        t += d
    return V, T0, round(t, 2)


def texts(vep):
    import json
    L = json.load(open(ROOT / 'series' / SLUG / 'voice' / vep / 'lines.json'))
    out = {}
    for k, (who, txt) in L.items():
        s = txt
        while s.startswith('['): s = s[s.index(']') + 1:].strip()
        out[k] = s.replace('́', '')
    return out


class Faces:
    def __init__(s, epi, tracks):
        s.epi = epi
        s.F = {who: M.Face(tr, TAB, seed=sd) for who, (tr, sd) in tracks.items()}

    def kw(s, who, t, base=(0.7, 0.0), **kw):
        m = M.mouth(s.epi.talk, who, t)
        F = s.F[who]
        return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def shot(name, cx, cy, Z, **kw):
    kw.setdefault('dof_k', 0.0)                          # no background blur unless it means something (owner 22.11.2026)
    kw.setdefault('clock', '16:40')
    return K.shot(name, cx, cy, Z, **kw)


def floor_actor(fn, wx, wy, Z, **kw):
    return K.A(fn, wx, wy, K.ws_at(wy) * 3 * Z, **kw)


def fik_cu(FC, t, u, name='office', Z0=2.3, **kw):
    """the ficus close-up = the camera moves in on the windowsill: the pot stands ON the sill at its real size"""
    Z = Z0 + 0.06 * u
    fk = K.A(C.fikus, SILL[0], SILL[1], WS_SILL * 3 * Z, **FC.kw('fikus', t, (0.0, 0.0), **kw))
    return shot(name, SILL[0] + 6.0, 290.0, Z, acts=[fk], par=(-2 + 3 * u, 0), t=t)


def cu(FC, who, fn, t, u, name='office', cx=520.0, cy=360.0, y=860, s=32.0, base=(0.0, 0.0), flip=False, post=None, **kw):
    Z = 1.3
    v = K.V(name, cx, cy, Z)
    a = at(fn, v, 540, y, s, pin='head', near=0.99, flip=flip, **FC.kw(who, t, base, **kw))
    big = shot(name, cx, cy, Z, acts=[a], par=(-6 + 10 * u, 0), t=t)
    if post: post(big, a, v)
    return big


def tally(big, text, fg=(255, 232, 110), y=380, size=64):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2, y, 1.0)


def darken(big, k=0.5):
    big[:] = (big * k).astype(np.uint8)
    return big


# ---------------------------------------------------------------- inserts
def desk_bg():
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    yy = np.linspace(0, 1, OUT_H)[:, None, None]
    big[:] = (np.array((150, 118, 84)) * (1 - yy) + np.array((110, 84, 58)) * yy).astype(np.uint8)
    return big


def phone_insert(t, msgs, title='ОБЩИЙ ЧАТ • 47', deleted=False, banner=None):
    """Эдик's phone, the «ЧАТСАП» group chat; msgs = [(author, text, mine)]"""
    big = desk_bg()
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([170, 220, 910, 1760], 70, fill=(30, 30, 36), outline=(10, 10, 12), width=12)
    d.rectangle([210, 330, 870, 1640], fill=(236, 230, 214))
    d.rectangle([210, 330, 870, 430], fill=(52, 120, 90))
    d.text((240, 360), 'ЧАТСАП', font=O.pfont(26), fill=(255, 255, 255))
    d.text((240, 396), title, font=O.pfont(22), fill=(220, 240, 230))
    y = 470
    for who, txt, mine in msgs:
        f = O.pfont(30)
        w = int(f.getlength(txt)) + 60
        x0 = 840 - w if mine else 240
        col = (210, 246, 190) if mine else (255, 255, 255)
        if deleted and mine:
            txt = 'Сообщение удалено'; col = (220, 220, 220); w = int(f.getlength(txt)) + 60; x0 = 840 - w
        d.rounded_rectangle([x0, y, x0 + w, y + 110], 22, fill=col)
        d.text((x0 + 26, y + 12), who, font=O.pfont(18), fill=(52, 120, 90))
        d.text((x0 + 26, y + 50), txt, font=f, fill=(140, 140, 140) if (deleted and mine) else (30, 30, 34))
        if mine and not deleted: d.text((x0 + w - 70, y + 84), '✓✓'.replace('✓', 'v'), font=O.pfont(16), fill=(60, 140, 230))
        y += 140
    if banner:
        d.rounded_rectangle([230, 1500, 850, 1610], 20, fill=(40, 40, 46))
        f = O.pfont(28); d.text(((1080 - f.getlength(banner)) / 2, 1540), banner, font=f, fill=(255, 255, 255))
    return np.array(im)


def calendar_insert(t, month='ФЕВРАЛЬ 2027', days=28, first=0, mark=None, vanish=None, stamp=None):
    """a wall calendar page; vanish=(day, k 0..1) — the day cell dissolves in pixels"""
    big = desk_bg()
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([110, 260, 970, 1660], fill=(250, 248, 240), outline=(60, 50, 40), width=10)
    d.rectangle([110, 260, 970, 420], fill=(190, 40, 40))
    f = O.pfont(56); d.text(((1080 - f.getlength(month)) / 2, 310), month, font=f, fill=(255, 255, 255))
    cw, ch = 118, 170
    for i, wd in enumerate(['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']):
        d.text((140 + i * cw + 30, 440), wd, font=O.pfont(26), fill=(190, 40, 40) if i > 4 else (60, 60, 70))
    for k in range(days + (1 if mark else 0)):
        day = k + 1
        c = (first + k) % 7; r = (first + k) // 7
        x0, y0 = 140 + c * cw, 500 + r * ch
        d.rectangle([x0, y0, x0 + cw - 8, y0 + ch - 10], outline=(180, 170, 150), width=3)
        if day <= days:
            d.text((x0 + 18, y0 + 16), str(day), font=O.pfont(40), fill=(190, 40, 40) if c > 4 else (40, 40, 44))
        elif mark:
            d.text((x0 + 18, y0 + 16), str(day), font=O.pfont(40), fill=(200, 200, 200))
    a = np.array(im)
    if vanish and mark:
        k_ = vanish
        c = (first + days) % 7; r = (first + days) // 7
        x0, y0 = 140 + c * cw, 500 + r * ch
        reg = a[y0:y0 + ch - 10, x0:x0 + cw - 8]
        rng = np.random.default_rng(3)
        m = rng.random(reg.shape[:2]) < k_
        reg[m] = (250, 248, 240)
        if k_ < 0.5:
            reg[(rng.random(reg.shape[:2]) < 0.15)] = (255, 90, 80)
    if stamp:
        img = O.sticker(stamp, fg=(230, 50, 50), size=70)
        O.overlay(a, img, (OUT_W - img.shape[1]) // 2, 1250, 1.0)
    return a


def ep(ep_id, voice, dur_, promise, promo='ru'):
    return Episode(ep_id, voice, dur_, 30, colors=K.COL, slug=SLUG, endcard=dict(style='ks', lang='ru', promise=promise), promo=promo)
