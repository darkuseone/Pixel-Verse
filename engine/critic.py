"""Critic pass (owner rule 10.10.2026): after an episode is rendered, a critic looks at it for visual artefacts BEFORE it goes to the owner.
This script prepares the material; the review itself is done by a vision sub-agent (Claude Agent tool) with CHECKLIST below,
its report is saved as episodes/epNN/critic.md, every finding is fixed and the episode re-rendered until the critic finds nothing.

  python3 engine/critic.py series/<slug>/episodes/epNN [video.mp4]
    -> build/<slug>-epNN/critic/  f_<t>.png (full 1080x1920: the middle of every shot + every ~1.5 s), sheet_XX.png (3x2 contact
       sheets at half size), cover.png + cover_grid.png (TikTok / Reels profile-grid preview), list.txt (what to look at)
"""
import sys, os, subprocess, pathlib, importlib.util
from PIL import Image

CHECKLIST = """\
CRITIC CHECKLIST (look at every full-size frame, not only the sheets):
1. Character sprites in close-ups: no «pixel mush» (blocky blobs instead of eyes / mouth / hands); facial features readable:
   eyes with whites + pupils, mouth with teeth / tongue, brows; accessories sit where they belong (glasses ON the eyes, hats on heads).
2. Every inscription (signs, plates, stickers, labels on props, chyrons, cards, captions): readable, spelled right, fully INSIDE its plate,
   not crooked relative to its plate, not cut by the frame edge when it is the subject of the shot, no letters bleeding off a sign.
3. Physically possible frame: feet / wheels / chair legs on the ground (contact shadow), scale of sprites matches props and background,
   nothing floating, nothing stuck halfway into a wall; who is speaking is clear.
4. Artefacts: hard seams, half-screen colour splits, stray pixels / specks, torn or doubled sprites, sprites clipped by a mask, flicker
   between neighbouring frames, AI-background glitches (zigzags, melted shapes, garbage text), hard edges of an effect, black bars.
5. Subtitles and stickers never cover faces or the key prop; the episode plate (top-left) does not cover anything important.
6. Ambience: the location reads at once (local signs, stickers, props, particles); background not empty or static.
7. Cover: plate at the top of the 3:4 profile-grid zone (y 240..1680), title right under it, faces inside the zone, nothing important
   below y 1520 (date / views overlay); cover_grid.png must read well at thumbnail size.
Report: numbered findings «time / file — what is wrong — where in the frame (x, y) — how bad (BLOCKER / FIX / NIT)», then
«VERDICT: CLEAN» or «VERDICT: FIX». BLOCKER and FIX must be fixed before delivery."""


def main():
    ep = pathlib.Path(sys.argv[1]).resolve()
    slug = ep.parents[1].name
    name = ep.name
    root = ep.parents[3]
    out = root / 'build' / f'{slug}-{name}' / 'critic'
    out.mkdir(parents=True, exist_ok=True)
    for f in out.glob('*.png'): f.unlink()
    video = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ep / 'final.mp4'
    spec = importlib.util.spec_from_file_location('tl', ep / 'timeline.py'); tl = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(ep)); spec.loader.exec_module(tl)
    cuts = list(tl.CUTS)
    ts = {round((a + b) / 2, 2) for a, b in zip(cuts[:-1], cuts[1:])}
    t = 0.25
    while t < tl.DUR - 0.1: ts.add(round(t, 2)); t += 1.5
    ts = sorted(x for x in ts if x < tl.DUR - 0.05)
    files = []
    for x in ts:
        f = out / f'f_{x:05.2f}.png'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{x:.3f}', '-i', str(video), '-frames:v', '1', str(f)], check=True)
        files.append(f)
    for i in range(0, len(files), 6):
        grp = files[i:i + 6]
        c = Image.new('RGB', (540 * 3, 960 * 2), (20, 20, 20))
        for k, f in enumerate(grp):
            c.paste(Image.open(f).resize((540, 960), Image.LANCZOS), ((k % 3) * 540, (k // 3) * 960))
        c.save(out / f'sheet_{i // 6:02d}.png')
    for nm in ('cover.png', 'cover_grid.png'):
        if (ep / nm).exists(): Image.open(ep / nm).save(out / nm)
    (out / 'list.txt').write_text('\n'.join(str(f) for f in sorted(out.glob('*.png'))) + '\n\n' + CHECKLIST + '\n')
    print(out)
    print(len(files), 'frames,', (len(files) + 5) // 6, 'sheets')


if __name__ == '__main__':
    main()
