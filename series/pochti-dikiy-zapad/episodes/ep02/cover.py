import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import numpy as np, math
from PIL import Image
import ep02 as E          # sets 216 grid first
import cover as C         # switches engine grid to 540x960 (K=5)
import scene as S
import hd

def render():
    hd.SUN = (99, 96)
    F = hd.background_hd(E.CAMX, 3.0)
    cam = E.ACam(0, 0, 0, 0, 5.0)
    E.draw_town(F, cam)
    L = S.Layer(cam); E.draw_vulture(L, 12, 101, 0, perched=True, facing=1)
    E.draw_vulture(L, 70, 58, 1.0); E.draw_vulture(L, 88, 70, 2.2, facing=-1)
    S.outline(L, (30, 24, 26)); S.comp(F, L)
    E.draw_signpost(F, cam)
    E.draw_poster(F, cam, board=True)
    L = S.Layer(cam); E.draw_skull(L, 7.5, 157.5); S.outline(L, (110, 84, 60)); S.comp(F, L)
    # Molniya "hidden" behind the thin post
    t = 22.0
    E.draw_molniya(F, cam, t)
    E.draw_poster(F, cam, post_front=True, board=False)
    E.draw_motes(F, cam, 3.0)
    # foreground: costume (eyes bulging) with Sam sitting on it, big
    fg = E.ACam(E.CACT[0], E.CACT[1], 372, 742, 11.5)
    E.draw_costume(F, fg, t, squash=1.0, eyes='bulge')
    E.draw_sam(F, fg, (E.SAM_X_SIT, E.CACT[1] - 8.4 * 0.95), True, 'sit', 1.0, 0.0, True)
    L = S.Layer(fg)  # sweat drops + little shock lines by the face window
    for (dx, dy) in ((-6.2, -1.5), (6.3, -2.2), (-5.4, 1.2)):
        S.ell(L, (E.CACT[0] + dx, E.CACT[1] + dy), 0.45, 0.7, (170, 220, 255))
    S.comp(F, L)
    for i, yy in enumerate(range(0, 110, 22)):
        F[yy:yy + 22] = (F[yy:yy + 22].astype(np.float32) * (0.62 + 0.07 * i)).astype(np.uint8)
    C.plank(F, 'ПОЧТИ ДИКИЙ ЗАПАД • 2/6', 134, 16)
    C.pixel_text(F, ['Я — КАКТУС.'], 210, 64, max_w=512, gap=10)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    img.save(P.episode('ep02') / 'cover.png')

if __name__ == '__main__':
    render()
    Image.open(P.episode('ep02') / 'cover.png').resize((540, 960)).save(P.build('ep02', 'cover_prev.png'))
