"""Shot builders for the feature cut: close-ups and two-shots on top of kit.scene(); each returns fn(ctx, t, u, dur)."""
from kit import *

ANCH = dict(yard=dict(dale=(430.0, 592.0, 16.0), brenda=(965.0, 592.0, 16.0), earl=POND['yard']),
            clubhouse=dict(dale=(330.0, 600.0, 16.0), brenda=(760.0, 600.0, 16.0), earl=POND['clubhouse']),
            interior=dict(dale=(430.0, 592.0, 16.0), brenda=(965.0, 592.0, 16.0), earl=POND['yard']),
            storm=dict(dale=(430.0, 592.0, 16.0), brenda=(965.0, 592.0, 16.0), earl=POND['yard']),
            board=dict(dale=(430.0, 600.0, 16.0), brenda=(770.0, 600.0, 16.0), earl=POND['yard']),
            beach=dict(dale=(430.0, 600.0, 16.0), brenda=(820.0, 600.0, 16.0), earl=POND['yard']))


def cu(who, world, Z=1.25, dz=0.06, anchor=None, dx=0.0, dy=0.0, lift=19.5, before=None, after=None, extra=(), vig=0.25, shake=0.0, post=None, front=None, **kw):
    """close-up of one hero (head + shoulders) at his/her anchor; extra = other hero specs kept in frame (drawn too)"""
    ax, ay, au = anchor or ANCH[world][who]
    flip = who == 'brenda'
    def fn(ctx, t, u, dur):
        sp = dict(who=who, x=ax, y=ay, u=au, flip=flip, **kw)
        cx = ax + (-1.5 if flip else 1.5) * au + dx
        cy = ay - lift * au + dy
        return scene(ctx, t, u, dur, world, [sp] + list(extra), (cx, cy, Z, cx, cy, Z + dz), before=before, after=after, vig=vig, shake=shake, post=post, sy=190, front=front)
    return fn


def two(world, cast, cam, before=None, after=None, vig=0.25, shake=0.0, post=None, sy=190, front=None):
    """wide / medium shot with several heroes; cast = list of specs (or callable(ctx,t,u,dur)->list); cam = (cx,cy,Z[,cx1,cy1,Z1])"""
    def fn(ctx, t, u, dur):
        c = cast(ctx, t, u, dur) if callable(cast) else cast
        return scene(ctx, t, u, dur, world, c, cam, before=before, after=after, vig=vig, shake=shake, post=post, sy=sy, front=front)
    return fn


def earl(world='yard', lid=0.5, Z=2.3, **kw):
    def fn(ctx, t, u, dur):
        return earl_cu(ctx, t, u, dur, world, lid=lid, Z=Z, **kw)
    return fn


def with_pip(base, world='yard', corner='br', w=700, lid=0.5, Z=2.3, label='EARL (grandfathered in)', **ekw):
    """scene `base` (mouths muted for Earl's line by the caller) + Earl reaction cam"""
    def fn(ctx, t, u, dur):
        big = base(ctx, t, u, dur)
        pip(big, earl_cu(ctx, t, u, dur, world, lid=lid, Z=Z, zoom=0.03, **ekw), corner, w, 1.0, label)
        return big
    return fn


def insert_dim(world, draw, Z=1.0, cx=640, cy=360, dimk=0.55):
    """dimmed world background with a 1080p overlay drawn by draw(big, t, u, dur)"""
    def fn(ctx, t, u, dur):
        ST.set_px(1)
        v = view_at(world_(world), cx, cy, Z, 320, 180)
        big = v.bg(); dim(big, dimk); draw(big, t, u, dur)
        return big
    return fn


def world_(name): return world(name)


def title_card(lines, sub=None, size=100, bg='yard', dimk=0.6, pan=0.0):
    """full-frame neon title over a dimmed, slowly panning location"""
    ti = O.neon_title(lines, size, width=W_)
    def fn(ctx, t, u, dur):
        ST.set_px(1)
        v = view_at(world(bg), 640 + pan * u, 360, 1.05, 320, 180)
        big = v.bg(); dim(big, dimk)
        k = sm(u / 0.25)
        O.overlay(big, ti, 0, int(H_ / 2 - ti.shape[0] / 2 - 30 - (1 - k) * 60), k)
        if sub: ptext(big, sub, W_ // 2, int(H_ / 2 + ti.shape[0] / 2 + 30), 34, (0, 214, 232), (20, 6, 40))
        return big
    return fn


def cuts(seq):
    """seq = [(t_start, fn), ...]: switch shots inside one beat (u restarts at each cut) — keeps a new angle every ~2 s"""
    seq = sorted(seq, key=lambda q: q[0])
    def fn(ctx, t, u, dur):
        k = 0
        for i, (a, _) in enumerate(seq):
            if u >= a: k = i
        a, f = seq[k]
        end = seq[k + 1][0] if k + 1 < len(seq) else dur
        return f(ctx, t, u - a, end - a)
    return fn


def portrait_insert(draw, bg='yard', ph=980, cx=640, cy=360, Z=1.0, ctx_arg=False):
    """draw(big1080x1920, t, u) paints a portrait UI; shown on a device in front of the dimmed location"""
    def fn(ctx, t, u, dur):
        ST.set_px(1)
        v = view_at(world(bg), cx, cy, Z, 320, 180)
        bgf = v.bg()
        pt = np.zeros((1920, 1080, 3), np.uint8)
        (draw(pt, t, u, dur, ctx) if ctx_arg else draw(pt, t, u, dur))
        return device(pt, bgf, ph)
    return fn


def kev_hook(x, y, u, flip=False, wob=0.0, shades=True, tilt=0.0):
    def f(C, v, t, uu):
        UP.flamingo(C, v.cam(x, y, u, flip), t, True, shades, wob, tilt)
    return f
