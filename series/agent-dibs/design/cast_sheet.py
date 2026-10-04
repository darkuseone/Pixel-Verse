"""Agent Dibs — cast model sheet (design skill output, see philosophy.md).  python3 cast_sheet.py  ->  cast_sheet.png
Lineup at one scale with a height ruler, palette swatches, silhouette strip, Dibs expression strip, busts of Deb and the window ladies."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
from props import dibspix as DX, dibscast as DC

W, H = 2400, 1640
INK, GRID, GRID2 = (13, 17, 34), (19, 25, 48), (26, 34, 64)
ICE, MUTED, RED, SKY = (236, 244, 255), (118, 140, 186), (226, 40, 60), (104, 186, 240)
FD = P.ENGINE / 'fonts'


def font(name, size):
    return ImageFont.truetype(str(FD / name), size)


def sprite(fn, **P_):
    sp = DX.Spr(); fn(sp, **P_)
    return sp


def put(big, sp, ox, oy, s, flip=False, sil=None):
    if sil is not None:
        sp = sp.__class__(); sp.col, sp.m = sil
    DX.blit(big, sp, ox, oy, s, None, flip)


def silhouette(sp, col):
    c = np.zeros_like(sp.col); c[:] = col
    return c, sp.m.copy()


def head_box(big, sp, cx, cy, s, below=24.0):
    """head-and-shoulders crop: everything lower than `below` sprite px under the head centre is cut, so cells never overlap"""
    hx, hy = sp.anchors['head']
    sp.clip_below(hy - below)
    DX.blit(big, sp, cx - hx * s, cy + hy * s, s, None, False)


def main():
    big = np.zeros((H, W, 3), np.uint8); big[:] = INK
    big[:, ::40] = GRID; big[::40, :] = GRID
    big[:, ::200] = GRID2; big[::200, :] = GRID2
    img = Image.fromarray(big); d = ImageDraw.Draw(img)
    # header
    d.text((70, 52), 'AGENT DIBS', font=font('BigShoulders-Bold.ttf', 132), fill=ICE)
    d.text((76, 200), 'CAST  ·  MODEL SHEET  ·  SEASON 1', font=font('JetBrainsMono-Regular.ttf', 22), fill=MUTED)
    d.text((76, 232), 'LAKE-EFFECT FOLK  —  1 SPRITE PX = 1 VISIBLE SQUARE  ·  4 TONES + ORDERED DITHER  ·  NAVY OUTLINE', font=font('JetBrainsMono-Regular.ttf', 16), fill=(86, 104, 146))
    for y in (284, 296): d.rectangle([70, y, W - 70, y + 4], fill=SKY)
    big = np.array(img)

    lineup = [('DIBS', 'special agent, 22 yrs probation', DC.dibs, dict(expr='smug', pose='hips', shades=False), [DC.D_SKIN, DC.D_JACKET, DC.D_FUR]),
              ('TERRY', 'tough guy, community theatre', DC.terry, dict(expr='nervous'), [DC.T_SKIN, DC.PUFF]),
              ('GARY', 'his guard, earnest', DC.gary, dict(expr='grin'), [DC.G_SKIN, DC.PUFF]),
              ('BRAD', 'Naperville dad, rival', DC.brad, dict(expr='grin', ting=1.0), [DC.B_SKIN, DC.B_VEST, DC.B_KHAKI]),
              ('BOMB TECH', 'respects the chair', DC.tech, dict(expr='nervous'), [DC.T_SUIT]),
              ('MARTY', 'informant (rat)', DC.marty, dict(expr='deadpan'), [DC.R_FUR, DC.R_PINK, DC.R_CAP])]
    base, s = 1000, 5.0
    xs = [300 + i * 345 for i in range(len(lineup))]
    # height ruler
    img = Image.fromarray(big); d = ImageDraw.Draw(img)
    fm = font('JetBrainsMono-Regular.ttf', 14)
    for k in range(0, 131, 10):
        y = base - k * s
        d.line([(120, y), (138 if k % 50 else 150, y)], fill=MUTED, width=2)
        if k % 20 == 0: d.text((80, y - 9), f'{k:3d}', font=fm, fill=(86, 104, 146))
    d.line([(138, base), (138, base - 130 * s)], fill=(60, 74, 110), width=2)
    d.line([(150, base), (W - 70, base)], fill=(70, 86, 126), width=2)
    big = np.array(img)
    sprites = []
    for (name, role, fn, P_, pals), x in zip(lineup, xs):
        sp = sprite(fn, t=0.6, **P_)
        sprites.append(sp)
        put(big, sp, x, base, s)
    img = Image.fromarray(big); d = ImageDraw.Draw(img)
    fn_name, fn_role = font('BigShoulders-Bold.ttf', 44), font('JetBrainsMono-Regular.ttf', 15)
    for (name, role, fn, P_, pals), x in zip(lineup, xs):
        w = d.textlength(name, font=fn_name); d.text((x - w / 2, base + 18), name, font=fn_name, fill=ICE)
        w = d.textlength(role, font=fn_role); d.text((x - w / 2, base + 72), role, font=fn_role, fill=MUTED)
        sw = 20; tot = len(pals) * (4 * sw + 10) - 10; x0 = x - tot / 2
        for pi, pal in enumerate(pals):
            for ci, c in enumerate(pal):
                xx = x0 + pi * (4 * sw + 10) + ci * sw
                d.rectangle([xx, base + 100, xx + sw - 2, base + 118], fill=tuple(c))
    big = np.array(img)
    # silhouette strip (top right): readable as pure shapes
    for i, sp in enumerate(sprites):
        put(big, sp, 1300 + i * 165, 262, 1.55, sil=silhouette(sp, MUTED))
    img = Image.fromarray(big); d = ImageDraw.Draw(img)
    d.text((1300 - 40, 60), 'SILHOUETTE TEST', font=font('JetBrainsMono-Regular.ttf', 15), fill=(86, 104, 146))
    # lower band: Dibs expressions + busts
    y0 = 1190
    d.rectangle([70, y0 - 30, W - 70, y0 - 27], fill=(40, 52, 90))
    d.text((70, y0 - 16), 'DIBS · EXPRESSIONS', font=font('JetBrainsMono-Regular.ttf', 15), fill=(86, 104, 146))
    d.text((1480, y0 - 16), 'DEB · MRS. WOZNIAK · ROSE · DOT', font=font('JetBrainsMono-Regular.ttf', 15), fill=(86, 104, 146))
    big = np.array(img)
    exprs = [('normal', {}), ('shout', dict(mouth_=0.9)), ('smug', dict(shades=True)), ('shock', dict(mouth_=0.6)), ('angry', {}), ('deadpan', dict(soot=0.75, shades=True))]
    for i, (e, kw) in enumerate(exprs):
        cx, cy = 180 + i * 222, y0 + 210
        sp = sprite(DC.dibs, t=0.6, expr=e, **kw)
        head_box(big, sp, cx, cy, 4.6)
    low = dict(L=(-6.0, 34.0), R=(9.0, 34.0))
    busts = [(DC.deb, dict(expr='smile', hands=low, props={})), (DC.lady, dict(who='mrs_w', hands=low)),
             (DC.lady, dict(who='rose', expr='smug', hands=low)), (DC.lady, dict(who='dot', expr='squint', hands=low))]
    for i, (fn, kw) in enumerate(busts):
        cx, cy = 1560 + i * 215, y0 + 210
        sp = sprite(fn, t=0.6, **kw)
        head_box(big, sp, cx, cy, 4.6, below=22.0)
    img = Image.fromarray(big); d = ImageDraw.Draw(img)
    for i, (e, kw) in enumerate(exprs):
        cx = 180 + i * 222
        w = d.textlength(e.upper(), font=fn_role); d.text((cx - w / 2, y0 + 345), e.upper(), font=fn_role, fill=MUTED)
    d.text((W - 70 - d.textlength('PIXEL VERSE ^^', font=fn_role), H - 40), 'PIXEL VERSE ^^', font=fn_role, fill=(70, 86, 126))
    out = pathlib.Path(__file__).with_name('cast_sheet.png')
    img.save(out); print(out)


if __name__ == '__main__':
    main()
