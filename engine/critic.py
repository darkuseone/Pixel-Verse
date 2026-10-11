"""Critic pass (owner rule 10.10.2026), economical version (11.10.2026): the machine does the measurable checks, the eye only the rest.

  python3 engine/critic.py series/<slug>/episodes/epNN
    1. runs engine/autocheck.py (renders the middle of every shot from code with a render log: signs cut by the edge, text over faces,
       plate over signs, cut heads, timing 30–38 s / twist 50–60 % / <= 18 s, loudness, cover files) -> episodes/epNN/autocheck.md
    2. builds 2 compact sheets of 12 shots each (270x480 per shot, findings boxed) -> build/<slug>-epNN/review/mini_N.png
    3. prints the vision checklist below.
  The vision pass looks ONLY at the mini sheets (+ a full-size crop of anything suspicious) — ~4–6k image tokens per episode instead of
  ~100k for 40 full frames. Who looks: me (main loop), or a sub-agent with model='sonnet' when a second pair of eyes is needed
  (re-check only the shots that changed). Report -> episodes/epNN/critic.md, verdict CLEAN / FIX; BLOCKER/FIX are fixed with
  `python3 epNN.py shots <i|name> ...` (only those shots are re-rendered), then `mix.py`.
"""
import sys, subprocess, pathlib
from PIL import Image, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parents[1]

CHECKLIST = """\
VISION CHECKLIST (mini sheets; zoom into a full-size frame only where something looks off):
1. Close-ups: no «pixel mush»; eyes / mouth / brows readable; accessories where they belong (glasses ON the eyes, hat on the head).
2. Physically possible: feet / wheels on the ground, contact shadow, sprite scale matches props and background; nothing floating,
   nothing held without a hand; it is clear who speaks.
3. Artefacts the machine can't see: hard seams / half-screen colour splits, stray specks, torn / doubled sprites, odd clipping,
   AI-background glitches (zigzags, melted shapes, garbage text), an effect with a hard edge.
4. Signs read and are spelled right; the location reads at once (local signs, stickers, props, particles).
5. Cover: plate on top of the 3:4 zone, title under it, faces inside, nothing important below y 1520 (see cover_grid.png).
Machine findings (autocheck.md) are already measured — just confirm or accept each FIX (intended POV / split-screen = accept)."""


def mini_sheets(review_dir, out_prefix='mini'):
    fs = sorted(review_dir.glob('f_*.png'))
    outs = []
    for j in range(0, len(fs), 12):
        c = Image.new('RGB', (270 * 6, 480 * 2), (16, 16, 16))
        for i, f in enumerate(fs[j:j + 12]):
            im = Image.open(f).convert('RGB').resize((270, 480), Image.LANCZOS)
            d = ImageDraw.Draw(im)
            d.rectangle([0, 456, 270, 480], fill=(0, 0, 0)); d.text((6, 462), f.stem[2:] + 's', fill=(255, 255, 255))
            c.paste(im, ((i % 6) * 270, (i // 6) * 480))
        p = review_dir / f'{out_prefix}_{j // 12}.png'
        c.save(p); outs.append(p)
    return outs


def main():
    ep = pathlib.Path(sys.argv[1]).resolve()
    extra = sys.argv[2:]
    r = subprocess.run([sys.executable, str(ROOT / 'engine' / 'autocheck.py'), str(ep)] + extra, capture_output=True, text=True)
    if r.returncode: sys.exit(r.stderr[-2000:])
    review = ROOT / 'build' / f'{ep.parents[1].name}-{ep.name}' / 'review'
    sheets = mini_sheets(review)
    print((ep / 'autocheck.md').read_text())
    print('mini sheets:', *sheets, sep='\n  ')
    print('cover:', ep / 'cover.png', ep / 'cover_grid.png')
    print(CHECKLIST)


if __name__ == '__main__':
    main()
