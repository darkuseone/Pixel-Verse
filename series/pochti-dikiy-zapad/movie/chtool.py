"""Chapter tool (16:9): python3 chtool.py sheet <chapter_dir>/<module> [-r] t1 t2 ...   (-r: use render() with overlays)
                     python3 chtool.py frame <chapter_dir>/<module> t [-r]
                     python3 chtool.py seg <chapter_dir>/<module> t_in a b out.mp4   (frames a..b-1 at t=t_in+i/30)"""
import os, sys, pathlib, importlib, subprocess
os.environ['PV_WIDE'] = '1'
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image


def load(spec):
    d, m = spec.split('/')
    cdir = HERE / ('blocks' if d == 'blocks' else 'chapters/' + d)
    sys.path.insert(0, str(cdir)); sys.path.insert(0, str(HERE))
    return importlib.import_module(m)


def main():
    a = sys.argv[1:]
    cmd, spec = a[0], a[1]
    rest = a[2:]
    raw = '-r' not in rest
    rest = [x for x in rest if x != '-r']
    M = load(spec)
    fn = getattr(M, 'render_scene') if raw and hasattr(M, 'render_scene') else M.render
    out_dir = HERE / 'build'; out_dir.mkdir(exist_ok=True)
    if cmd == 'sheet':
        ts = list(map(float, rest)); cols = 3; rows = (len(ts) + cols - 1) // cols
        sheet = Image.new('RGB', (480 * cols, 270 * rows))
        for k, t in enumerate(ts):
            sheet.paste(Image.fromarray(fn(t)).resize((480, 270), Image.LANCZOS), ((k % cols) * 480, (k // cols) * 270))
        p = out_dir / f'sheet_{spec.replace("/", "_")}.png'; sheet.save(p); print(p)
    elif cmd == 'frame':
        p = out_dir / f'frame_{spec.replace("/", "_")}.png'; Image.fromarray(fn(float(rest[0]))).save(p); print(p)
    elif cmd == 'seg':
        t_in, a0, a1, out = float(rest[0]), int(rest[1]), int(rest[2]), rest[3]
        crf = os.environ.get('PV_CRF', '20')
        proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1920x1080', '-r', '30', '-i', '-',
                                 '-c:v', 'libx264', '-preset', 'medium', '-crf', crf, '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
        for i in range(a0, a1): proc.stdin.write(fn(t_in + i / 30.0).tobytes())
        proc.stdin.close(); proc.wait(); print('done', out)


if __name__ == '__main__': main()
