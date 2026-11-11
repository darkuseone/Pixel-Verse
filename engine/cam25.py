"""Камера 2.5D (правило владельца 11.11.2026): грамматика камеры из разбора вирусных 3D/2.5D-шортсов
(darkuseone/claude-animated-shorts, MIT): проезды с плавностью smootherstep, каждый план медленно «вползает» (наезд
~0,15 % за кадр), лёгкое «дыхание» параллакса на статичных планах, удар — «кик» (смещение меняет знак каждый кадр и
затухает за 7 кадров) вместо долгой тряски; жёсткая склейка — только при смене места/информации.

    from cam25 import Cam, kick
    CAM = Cam([(0.0, 520, 330, 1.35, 0, 0), (2.4, 600, 330, 1.6, 8, 0)], creep=0.0015, breathe=3.0)
    cx, cy, Z, par = CAM.at(t)                       # для depth25.shot25(world, light, cx, cy, Z, depth, par=par, ...)
    big = depth25.shot25(..., kick=kick(t, [(3.10, 1.0)]))"""
import math

FPS = 30


def glide(u):
    """smootherstep 0..1: плавный старт и остановка (проезды 0,6–1,3 с)"""
    u = 0.0 if u < 0 else 1.0 if u > 1 else u
    return u * u * u * (u * (u * 6 - 15) + 10)


class Cam:
    """keys: [(t, cx, cy, Z, par_x, par_y), ...] — точка мира в точке экрана (sx, sy) шота, зум, параллакс (px мира).
    Между ключами — glide; creep — наезд за кадр от первого ключа (0 = выключен); breathe — амплитуда «дыхания»
    параллакса в px мира (живой статичный план, период ~5 с)."""
    def __init__(s, keys, creep=0.0015, breathe=0.0, seed=0):
        s.k = sorted(keys, key=lambda k: k[0]); s.creep = creep; s.breathe = breathe; s.ph = seed * 1.7

    def at(s, t):
        K = s.k
        if t <= K[0][0] or len(K) == 1: a, b, u = K[0], K[0], 0.0
        elif t >= K[-1][0]: a, b, u = K[-1], K[-1], 0.0
        else:
            i = max(j for j in range(len(K) - 1) if K[j][0] <= t)
            a, b = K[i], K[i + 1]; u = glide((t - a[0]) / max(1e-6, b[0] - a[0]))
        L = lambda j: a[j] + (b[j] - a[j]) * u
        Z = L(3) * (1 + s.creep * max(0.0, t - K[0][0]) * FPS) if s.creep else L(3)
        px, py = L(4), L(5)
        if s.breathe:
            px += s.breathe * math.sin(t * 1.25 + s.ph); py += s.breathe * 0.35 * math.sin(t * 0.9 + s.ph * 2)
        return L(1), L(2), Z, (px, py)


def kick(t, events, px=16.0):
    """удар камеры: events = [(время, сила), ...] -> (dx, dy) px кадра; знак меняется каждый кадр, затухание за 7 кадров"""
    dx = dy = 0.0
    for t0, g in events:
        n = int(math.floor((t - t0) * FPS + 1e-6))
        if 0 <= n < 7:
            k = g * (1 if n % 2 == 0 else -1) * (1 - n / 7) ** 1.5
            dx += k * px; dy += k * px * 0.45
    return dx, dy
