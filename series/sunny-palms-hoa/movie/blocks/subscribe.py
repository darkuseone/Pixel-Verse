"""Earl asks you to subscribe (cancelling requires Form 27-B)."""
from shots import *


def button(big, x, y, label='SUBSCRIBE', col=(230, 40, 60), k=1.0, struck=False):
    f = O.pfont(34); bb = f.getbbox(label); w = bb[2] - bb[0] + 80
    box = np.zeros((90, w, 4), np.uint8); box[..., :3] = col; box[..., 3] = 255
    box[:6, :, :3] = (255, 255, 255); 
    O.overlay(big, box, int(x - w / 2), int(y - 45), k)
    ptext(big, label, int(x), int(y), 34, (255, 255, 255), col)
    if struck: big[int(y - 4):int(y + 4), int(x - w / 2):int(x + w / 2)] = (20, 10, 30)


def s1(ctx, t, u, dur):
    big = earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3)
    k = sm((u - 0.2) / 0.3)
    button(big, 1480, 300 + int((1 - k) * 60), 'SUBSCRIBE', k=k)
    return big


def doc(big, u):
    x0, y0, w, h = 560, 200, 800, 720
    box = np.zeros((h, w, 4), np.uint8); box[..., :3] = (20, 12, 30); box[..., 3] = 255
    box[10:-10, 10:-10, :3] = (250, 246, 232)
    O.overlay(big, box, x0, y0 + int((1 - sm(u / 0.3)) * 200), 1.0)
    ptext(big, 'FORM 27-B', x0 + w // 2, y0 + 120, 46, (40, 30, 100), (250, 246, 232))
    ptext(big, 'CANCEL SUBSCRIPTION', x0 + w // 2, y0 + 220, 26, (60, 50, 90), (250, 246, 232))
    ptext(big, 'FILE 30 DAYS BEFORE', x0 + w // 2, y0 + 330, 30, (200, 40, 60), (250, 246, 232))
    ptext(big, 'SUBSCRIBING', x0 + w // 2, y0 + 390, 30, (200, 40, 60), (250, 246, 232))
    if u > 1.1: ptext(big, 'DENIED', x0 + w // 2, y0 + 560, 90, (230, 40, 60), (250, 246, 232))


def s2(ctx, t, u, dur):
    if u < 2.4:
        big = earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.4)
        button(big, 1480, 300, 'UNSUBSCRIBE', (120, 120, 130), 1.0, struck=(u > 1.2))
        return big
    ST.set_px(1)
    v = view_at(world('yard'), 640, 360, 1.0, 320, 180)
    big = v.bg(); dim(big, 0.5)
    doc(big, u - 2.4)
    return big


def s3(ctx, t, u, dur):
    big = earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.4, zoom=0.05)
    k = sm((u - 0.6) / 0.25)
    box = np.zeros((180, 900, 4), np.uint8); box[..., :3] = (245, 245, 250); box[..., 3] = 235
    box[:8, :, :3] = (255, 110, 190)
    O.overlay(big, box, 960 - 450, 180 + int((1 - k) * 40), k)
    ptext(big, 'Brenda W. (HOA PRESIDENT)', 960, 230 + int((1 - k) * 40), 22, (200, 40, 90), (245, 245, 250))
    ptext(big, 'This video is not approved.', 960, 300 + int((1 - k) * 40), 26, (40, 40, 60), (245, 245, 250))
    return big


BLOCK = Block('subscribe', [
    dict(v=('movie_t', 's1', 'earl', "If you like this video, SUBSCRIBE."), fn=s1, lead=0.1, sfx=[('library/sfx/ui_tap_chirp.mp3', 1.4, 0.6)], mosaic=[0.0]),
    dict(v=('movie_t', 's2', 'earl', "To unsubscribe, file Form twenty-seven B. Thirty days BEFORE subscribing."), fn=s2, sfx=[('library/sfx/paper_unroll.mp3', 2.4, 0.45, 0.0, 0.9), ('library/sfx/stamp.mp3', 3.7, 1.0), ('library/sfx/sad_trombone.mp3', 3.9, 0.3, 0.0, 1.4)]),
    dict(v=('movie_t', 's3', 'earl', "Comments are read by Brenda. Choose your words CAREFULLY."), fn=s3, sfx=[('library/sfx/app_notify_ping.mp3', 0.7, 0.6), ('library/sfx/pond_bloop.mp3', 0.0, 0.4)], pad=0.3),
], beds=[('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.3, False), ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.16, True)], hud=True, chapter='Subscribe (Terms Apply)')
