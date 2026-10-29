"""xAI backgrounds for «Land of the Fee» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.04-0.06 each). Skips existing files.
  python3 series/land-of-the-fee/gen_bg.py [names...]
Heroes, kiosks, the EMPLOYEES ONLY door, signs, bills, light and particles are drawn in code on top; backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, crisp visible pixels, rich but '
         'uncluttered detail, sunny satirical American sitcom look with a warm red-white-blue and mint-green palette, like a modern indie '
         'pixel adventure game, wide 16:9 scene. No characters, no people, no animals, no birds, no text, no letters, no numbers, no logos; '
         'every sign, banner, poster, label and screen is completely blank. ')
BG = {
    'apartment': 'Interior of a small cheap American studio apartment in the late afternoon, eye-level side view. Left: a tiny kitchenette '
                 'with an old white fridge completely covered with blank paper bills held by magnets, a microwave, a sink with dirty dishes. '
                 'Middle: a small round kitchen table with one chair and a coffee mug, behind it on a wall shelf a small internet router with '
                 'antennas. Right: a big sash window with a wide outside window ledge, through it a view of a suburban strip mall parking lot, '
                 'power lines and a pale blue sky. Far right: an unmade bed with blankets piled up like a messy round nest. Blank posters on '
                 'beige walls, a cheap ceiling lamp. Worn wooden floor across the whole lower third, empty. Warm sunlight from the window.',
    'mall': 'An American suburban strip mall on a sunny afternoon, wide eye-level view across a big mostly empty asphalt parking lot with '
            'painted white parking lines. A long row of small one-story shops with flat roofs and blank sign boards: a nail salon, a pizza '
            'place, a laundromat and in the middle a sleek cell phone and internet store with big glass windows glowing purple inside. '
            'Tall light poles, power lines with wires, a tall blank pylon sign by the road, shopping carts, a few trees, blue sky with puffy '
            'white clouds. Parking lot asphalt across the lower third, empty, no cars.',
    'store': 'Interior of a sleek minimalist American cell phone and internet provider retail store, eye-level wide view. White walls with '
             'purple and mint accent stripes, glossy white display tables with rows of blank phones and routers, big blank wall screens, a '
             'long white counter on the left with nobody behind it, bright cold LED ceiling light panels. The middle of the store is an open '
             'empty space. On the right part of the back wall a large plain empty white wall section. Polished white floor across the lower '
             'third, empty, reflections, clean and sterile, no people.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    usd = 0.0
    for n in names:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        usd += xai.generate(STYLE + BG[n], [str(out)])
    print('total $%.2f' % usd)
