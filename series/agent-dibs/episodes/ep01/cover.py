"""S01E01 cover (v2 cast).  python3 cover.py ref | ai | make
The environment (street, chair, bomb) goes through xAI edit for extra detail; the hero is pasted afterwards from the sprite engine,
so the cover shows exactly the Dibs of the episode (no AI-redrawn faces)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import fx
import xai
import covergen_dibs as CG
from stage import Chars, Light, view_at
from props import chi_props as PR, chikit as K
from props import dibspix as DX, dibscast as DC

EP, SLUG = 'ep01', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['CALLED', 'DIBS!']
SIZES = [96, 132]
PROMPT = ("Redraw this image as a highly detailed, vivid HD pixel art scene from a modern indie pixel-art adventure game (crisp visible pixels, "
          "rich environment detail, cold deep-blue Chicago winter night, warm orange sodium streetlamp glow, falling snow). Keep the same vertical "
          "composition and the same objects: on the right a green-and-white aluminium folding lawn chair standing in the snow with a blank cardboard "
          "sign taped to its seat, and under the chair a big round black cartoon bomb with a short burning fuse throwing bright orange sparks. "
          "Snowy Chicago side street with brick two-flat buildings, cars buried in snow, orange street lamps, an elevated train bridge far away. "
          "NO people, NO characters, NO animals. Keep the left half of the lower image as empty snowy street. Keep the top third calm and simple "
          "(dark night sky with a few snowflakes) for a title. No text, no letters, no numbers, no watermark.")
HERO = dict(head=(190, 640), s=4.0)                     # on the 540x960 cover canvas


def ref():
    world = K.world('dibs_row')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    wcx, wcy, sx, sy = 640.0, 420.0, 180, 372
    v = view_at(world, wcx, wcy, Z, sx, sy)
    big = v.bg()
    CG.calm_night(big)
    cu = 15.0 * 0.62 * 1.0
    ax, ay = wcx + 90.0, wcy + 236.0
    C2 = Chars()
    PR.dibs_chair(C2, v.cam(ax, ay, cu), t=0.3)
    C2.comp(big, K.light_street(v))
    C3 = Chars()
    bx, by, bu = ax - 22.0, ay + 18.0, cu * 1.3
    sp = PR.bomb(C3, v.cam(bx, by, bu), 0.3, 1.0)
    C3.comp(big, K.light_street(v))
    ox, oy = v.opt(bx + sp[0] * bu, by - sp[1] * bu)
    fx.glow(big, ox, oy, 300 * Z, (255, 150, 50), 0.85)
    Image.fromarray(big).save(REF); print(REF)


def hero(F):
    """paste Dibs (sprite engine) shouting and pointing at the chair, lit like the street at night"""
    sp = DX.Spr()
    DC.dibs(sp, 'point', t=0.3, mouth_=0.95, expr='shout', flap=0.4, hands={'R': (46.0, 60.0)})
    hx, hy = sp.anchors['head']
    (cx, cy), s = HERO['head'], HERO['s']
    lt = Light(amb=(0.98, 0.98, 1.06), rim=(1, -0.4, (255, 206, 150), 0.5), grad=(1.04, 0.92))
    DX.blit(F, sp, cx - hx * s, cy + hy * s, s, lt, False, shadow=0.0)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': xai.generate(PROMPT, [RAW], aspect='9:16', ref_png=REF)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e01.png'], 1, TITLE, SIZES, pre=hero)
        print('ok')
