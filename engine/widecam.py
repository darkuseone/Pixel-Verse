"""Vertical-authored camera -> 16:9 camera (PV_WIDE=1). Shots in epNN.py are written for 360x640 screens:
view_at(world, wx, wy, Z, sx, sy)  puts subject (wx,wy) at logical screen (sx,sy); View(world, X0, Y0, Z) has world top-left X0,Y0.
In wide mode the subject is centred horizontally and the zoom is reduced so the composition keeps its meaning."""
import stage as ST
from stage import WIDE

VW, VH = 360, 640          # authoring canvas
SUBJ_Y = 196               # where subjects sit on the 360-high wide canvas


def kz(Z, tune=1.0):
    """zoom factor vertical->wide: close-ups keep more zoom, wide shots fit more world"""
    return max(0.50, min(0.70, 0.56 + 0.10 * (Z - 1.0))) * tune


def conv_zoom(world, Z, tune=1.0):
    Zw = Z * kz(Z, tune)
    zmin = max(ST.W / world.shape[1], ST.H / world.shape[0])
    return max(Zw, zmin)


def view_at(world, wx, wy, Z, sx=180, sy=400, hlog=None, wlog=None, tune=1.0, sy_w=None):
    if not WIDE: return ST.view_at(world, wx, wy, Z, sx, sy, **({'hlog': hlog} if hlog else {}))
    half = hlog is not None
    Zw = conv_zoom(world, Z, tune)
    if half:                                             # side-by-side half: 320 x 360
        return ST.View(world, wx - 160 / Zw, wy - (sy_w or SUBJ_Y) / Zw, Zw, hlog=ST.H, wlog=320)
    return ST.View(world, wx - ST.W / 2 / Zw, wy - (sy_w or SUBJ_Y) / Zw, Zw)


def View(world, X0, Y0, Z, oy=0, hlog=None, tune=1.0):
    """authored with world top-left for a vertical window -> same world centre in wide"""
    if not WIDE: return ST.View(world, X0, Y0, Z, oy, **({'hlog': hlog} if hlog else {}))
    cx, cy = X0 + VW / 2 / Z, Y0 + VH / 2 / Z
    Zw = conv_zoom(world, Z, tune)
    return ST.View(world, cx - ST.W / 2 / Zw, cy - ST.H / 2 / Zw, Zw)


def halves(imgs, col=(30, 18, 12)):
    """two full frames rendered with half views (subject at x=160 logical) -> side-by-side split 1920x1080"""
    import numpy as np
    out = np.concatenate([imgs[0][:, :960], imgs[1][:, :960]], 1)
    out[:, 954:966] = col
    return out
