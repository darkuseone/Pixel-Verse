"""Episode scaffolding shared by all episodes: voice envelopes (lip flap), karaoke captions, encode + CLI.
Usage in epNN.py:
    EPI = Episode('ep06', VOICE, DUR, FPS)
    talk = EPI.talk
    ...
    if __name__ == '__main__': EPI.main(render, __file__)"""
import os, subprocess, sys
import numpy as np
from PIL import Image
import paths as P
import scene as S
import overlays as O
from stage import OUT_W, OUT_H

COL = dict(billy=(255, 222, 96), molniya=(255, 255, 255), sam=(214, 170, 255))
CRF = os.environ.get('PV_CRF', '20')              # chat upload limit is 30 MiB: if final.mp4 > 29 MiB re-render with PV_CRF=23
COVER_SEC = 0.1  # длительность вшитой обложки в начале ролика (правило владельца, 01.10.2026)


class Episode:
    def __init__(s, ep, voice, dur, fps=30, colors=COL, slug=P.PDZ, cap_words=3, endcard=None):
        """endcard=dict(style='fm'|'default'|..., lang='us'|'ru', sec=1.0, cy=None): «SUBSCRIBE!/ПОДПИШИСЬ!» in the last second (engine/endcard.py)"""
        s.ep, s.voice, s.dur, s.fps, s.slug = ep, voice, dur, fps, slug
        s.endcard = endcard
        s.bk = ep if slug == P.PDZ else f'{slug}-{ep}'      # build/ subfolder
        s.env = {}
        for vid, vep, key, t0, a, b, who, txt in voice:
            if (vep, key) not in s.env: s.env[(vep, key)] = S.load_env(P.voice_wav(vep, key, slug))
        items = []
        for vid, vep, key, t0, a, b, who, txt in voice:
            txt = txt.replace('\u0301', '')                 # stress marks are for the TTS only, never in subtitles (owner, 12.10.2026)
            ch = O.chunk_words(O.word_times(s.env[(vep, key)], t0, a, b, txt.split()), cap_words)
            for i, c in enumerate(ch):
                s0 = c[0][1]; e0 = ch[i + 1][0][1] if i + 1 < len(ch) else max(c[-1][2] + 0.35, t0 + (b - a))
                items.append((s0, e0, [w[0] for w in c], colors[who]))
        items.sort(key=lambda it: it[0])
        items = [(a, min(b, items[i + 1][0]) if i + 1 < len(items) and items[i + 1][0] > a else b, w, c)       # a caption never overlaps the next one
                 for i, (a, b, w, c) in enumerate(items)]
        s.captions = O.Captions(items)

    def talk(s, who, t):
        v = 0.0
        for vid, vep, key, t0, a, b, spk, txt in s.voice:
            if spk == who and t0 <= t < t0 + (b - a):
                e = s.env[(vep, key)]; i = int((a + t - t0) * 100)
                if 0 <= i < len(e): v = max(v, float(e[i]))
        return v

    def cover_frame(s):
        p = P.episode(s.ep, s.slug) / 'cover.png'
        return np.array(Image.open(p).convert('RGB').resize((OUT_W, OUT_H))) if p.exists() else None

    def encode(s, render, a0, a1, out):
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OUT_W}x{OUT_H}',
                                 '-r', str(s.fps), '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', CRF,
                                 '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        cov = s.cover_frame()
        cover_n = max(1, round(COVER_SEC * s.fps))  # обложка вшита в первые 0,1 с (3 кадра при 30 fps)
        for i in range(a0, a1):
            fr = cov if (i < cover_n and cov is not None) else render(i / s.fps)
            proc.stdin.write(fr.tobytes())
        proc.stdin.close(); proc.wait()

    def _cuts(s):
        m = sys.modules.get('__main__')
        c = getattr(m, 'CUTS', None)
        return list(c) if c else None

    def _shot_id(s, x):
        if x.isdigit(): return int(x)
        names = list(getattr(sys.modules.get('__main__'), 'NAMES', []))
        return names.index(x)

    def _shot_frames(s, i, n):
        c = s._cuts()
        f0 = int(round(c[i] * s.fps)); f1 = n if i == len(c) - 2 else int(round(c[i + 1] * s.fps))
        return f0, min(f1, n)

    def _render_even(s, render, script, a, n):
        k = int(a[2]) if len(a) > 2 else 4
        cuts = [round(n * i / k) for i in range(k + 1)]
        procs = [subprocess.Popen([sys.executable, script, 'seg', str(cuts[i]), str(cuts[i + 1])]) for i in range(k)]
        for p_ in procs: p_.wait()
        lst = P.build(s.bk, 'segs.txt')
        with open(lst, 'w') as f:
            for i in range(k): f.write(f"file '{P.build(s.bk, f'seg_{cuts[i]:04d}.mp4')}'\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                        P.build(s.bk, 'noaudio.mp4')], check=True)
        print('ok', P.build(s.bk, 'noaudio.mp4'))

    def main(s, render, script):
        import stage
        render0 = render
        def render(t):                               # animated decals / ambience read the frame time
            stage.T_NOW[0] = t
            fr = render0(t)
            ec = s.endcard
            if ec:                                   # end card «SUBSCRIBE!» (rule 12.10.2026), drawn on top of everything
                import endcard as EC
                t0 = s.dur - ec.get('sec', 1.0)
                if t >= t0: EC.draw(fr, EC.card(ec.get('style', 'default'), ec.get('lang', 'us')), t, t0, ec.get('cy') or int(OUT_H * 0.19))
            return fr
        n = int(round(s.dur * s.fps)); a = sys.argv
        if a[1] == 'test':
            ts = list(map(float, a[2:]))
            c = Image.new('RGB', (270 * len(ts), 480))
            for k, tt in enumerate(ts):
                c.paste(Image.fromarray(render(tt)).resize((270, 480), Image.LANCZOS), (k * 270, 0))
            c.save(P.build(s.bk, 'sheet.png')); print(P.build(s.bk, 'sheet.png'))
        elif a[1] == 'frames':                       # full-size control frames (critic, close-up check at 1080x1920)
            for tt in map(float, a[2:]):
                f = P.build(s.bk, f'f_{tt:05.2f}.png'); Image.fromarray(render(tt)).save(f); print(f)
        elif a[1] == 'frame':
            Image.fromarray(render(float(a[2]))).save(P.build(s.bk, 'frame.png')); print(P.build(s.bk, 'frame.png'))
        elif a[1] == 'seg':
            a0, a1 = int(a[2]), min(int(a[3]), n)
            s.encode(render, a0, a1, P.build(s.bk, f'seg_{a0:04d}.mp4')); print('done', a0, a1)
        elif a[1] == 'segs':                         # worker: render the listed shots, one segment per shot
            for i in map(int, a[2].split(',')):
                f0, f1 = s._shot_frames(i, n)
                s.encode(render, f0, f1, P.build(s.bk, f'shot_{i:02d}.mp4')); print('shot', i, f0, f1, flush=True)
        elif a[1] in ('all', 'shots'):
            # per-shot segments (rule 11.10.2026): after the critic only the fixed shots are re-rendered —
            #   python epNN.py shots 3 7 twist     (indexes or NAMES), then concat of all shot segments
            cuts = s._cuts()
            if cuts is None or a[1] == 'all' and os.environ.get('PV_SEGMODE') == 'even':
                return s._render_even(render, script, a, n)
            ids = list(range(len(cuts) - 1)) if a[1] == 'all' else [s._shot_id(x) for x in a[2:]]
            k = int(os.environ.get('PV_PROCS', '4'))
            lens = sorted(ids, key=lambda i: -(cuts[i + 1] - cuts[i]))
            jobs = [[] for _ in range(min(k, len(ids)))]
            load = [0.0] * len(jobs)
            for i in lens:                                          # greedy balance by shot length
                j = load.index(min(load)); jobs[j].append(i); load[j] += cuts[i + 1] - cuts[i]
            procs = [subprocess.Popen([sys.executable, script, 'segs', ','.join(map(str, jb))]) for jb in jobs if jb]
            for p_ in procs: p_.wait()
            if any(p_.returncode for p_ in procs): sys.exit('a shot worker failed')
            missing = [i for i in range(len(cuts) - 1) if not os.path.exists(P.build(s.bk, f'shot_{i:02d}.mp4'))]
            if missing: sys.exit(f'shot segments missing: {missing} (run: all)')
            lst = P.build(s.bk, 'shots.txt')
            with open(lst, 'w') as f:
                for i in range(len(cuts) - 1): f.write(f"file '{P.build(s.bk, f'shot_{i:02d}.mp4')}'\n")
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy',
                            P.build(s.bk, 'noaudio.mp4')], check=True)
            print('ok', P.build(s.bk, 'noaudio.mp4'), f'({len(ids)} shot(s) rendered)')
