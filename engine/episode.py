"""Episode scaffolding shared by all episodes: voice envelopes (lip flap), karaoke captions, encode + CLI.
Usage in epNN.py:
    EPI = Episode('ep06', VOICE, DUR, FPS)
    talk = EPI.talk
    ...
    if __name__ == '__main__': EPI.main(render, __file__)"""
import subprocess, sys
import numpy as np
from PIL import Image
import paths as P
import scene as S
import overlays as O
from stage import OUT_W, OUT_H

COL = dict(billy=(255, 222, 96), molniya=(255, 255, 255), sam=(214, 170, 255))
CRF = '20'


class Episode:
    def __init__(s, ep, voice, dur, fps=30, colors=COL):
        s.ep, s.voice, s.dur, s.fps = ep, voice, dur, fps
        s.env = {}
        for vid, vep, key, t0, a, b, who, txt in voice:
            if (vep, key) not in s.env: s.env[(vep, key)] = S.load_env(P.voice_wav(vep, key))
        items = []
        for vid, vep, key, t0, a, b, who, txt in voice:
            ch = O.chunk_words(O.word_times(s.env[(vep, key)], t0, a, b, txt.split()))
            for i, c in enumerate(ch):
                s0 = c[0][1]; e0 = ch[i + 1][0][1] if i + 1 < len(ch) else max(c[-1][2] + 0.35, t0 + (b - a))
                items.append((s0, e0, [w[0] for w in c], colors[who]))
        s.captions = O.Captions(items)

    def talk(s, who, t):
        v = 0.0
        for vid, vep, key, t0, a, b, spk, txt in s.voice:
            if spk == who and t0 <= t < t0 + (b - a):
                e = s.env[(vep, key)]; i = int((a + t - t0) * 100)
                if 0 <= i < len(e): v = max(v, float(e[i]))
        return v

    def cover_frame(s):
        p = P.episode(s.ep) / 'cover.png'
        return np.array(Image.open(p).convert('RGB').resize((OUT_W, OUT_H))) if p.exists() else None

    def encode(s, render, a0, a1, out):
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OUT_W}x{OUT_H}',
                                 '-r', str(s.fps), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF,
                                 '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        cov = s.cover_frame()
        for i in range(a0, a1):
            fr = cov if (i < 6 and cov is not None) else render(i / s.fps)
            proc.stdin.write(fr.tobytes())
        proc.stdin.close(); proc.wait()

    def main(s, render, script):
        n = int(round(s.dur * s.fps)); a = sys.argv
        if a[1] == 'test':
            ts = list(map(float, a[2:]))
            c = Image.new('RGB', (270 * len(ts), 480))
            for k, tt in enumerate(ts):
                c.paste(Image.fromarray(render(tt)).resize((270, 480), Image.LANCZOS), (k * 270, 0))
            c.save(P.build(s.ep, 'sheet.png')); print(P.build(s.ep, 'sheet.png'))
        elif a[1] == 'frame':
            Image.fromarray(render(float(a[2]))).save(P.build(s.ep, 'frame.png')); print(P.build(s.ep, 'frame.png'))
        elif a[1] == 'seg':
            a0, a1 = int(a[2]), min(int(a[3]), n)
            s.encode(render, a0, a1, P.build(s.ep, f'seg_{a0:04d}.mp4')); print('done', a0, a1)
        elif a[1] == 'all':
            k = int(a[2]) if len(a) > 2 else 4
            cuts = [round(n * i / k) for i in range(k + 1)]
            procs = [subprocess.Popen([sys.executable, script, 'seg', str(cuts[i]), str(cuts[i + 1])]) for i in range(k)]
            for p_ in procs: p_.wait()
            lst = P.build(s.ep, 'segs.txt')
            with open(lst, 'w') as f:
                for i in range(k): f.write(f"file '{P.build(s.ep, f'seg_{cuts[i]:04d}.mp4')}'\n")
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                            P.build(s.ep, 'noaudio.mp4')], check=True)
            print('ok', P.build(s.ep, 'noaudio.mp4'))
