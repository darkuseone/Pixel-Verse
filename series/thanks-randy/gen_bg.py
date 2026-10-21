"""xAI backgrounds for «Thanks, Randy» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/thanks-randy/gen_bg.py [names...]
Heroes, the self-checkout kiosk, signs, price tags, light and particles are drawn in code on top; backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, crisp visible pixels, rich but '
         'uncluttered detail, cozy funny American sitcom look, like a modern indie pixel adventure game, wide 16:9 scene. '
         'No characters, no people, no animals, no text, no letters, no numbers, no logos; every sign, banner, label, screen and price tag '
         'is completely blank. ')
BG = {
    'store': 'Interior of a big American suburban supermarket the week before Thanksgiving, eye-level view across the self-checkout area. '
             'Background: long aisles with colorful shelves, bright white fluorescent ceiling light panels, a row of three distant '
             'self-checkout kiosks with blank dark screens and small light poles. Middle left: a long open chest freezer full of frozen '
             'turkeys in red nets, cold blue light and frost mist rising from it. Middle right: a big pyramid of orange pumpkins and gourds '
             'on a wooden pallet, corn stalk bundles, hay bales, paper autumn leaf garlands hanging from the ceiling, blank hanging sale '
             'banners. Clean shiny grey tiled floor across the whole lower third, empty, with reflections. Warm yellow store light from '
             'above mixed with cold blue freezer light from the left.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
