"""xAI backgrounds for «Кощей из панельки» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/koshchei/gen_bg.py [names...]
Heroes, signs, notices, the coffin, the hut on chicken legs, light and particles are drawn in code on top; backgrounds have no people,
no animals and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, rich but uncluttered detail, '
         'like a modern indie pixel adventure game; a shabby post-Soviet apartment-block world in late October; warm yellow light of bare '
         'incandescent bulbs, deep warm black shadows like black lacquer, accents of gold and cinnabar red, a faint eerie green moonlight; '
         'cozy, nostalgic and a little spooky; wide 16:9 scene. No characters, no people, no animals, no text, no letters, no numbers; '
         'any signs, posters, papers, screens and labels are completely blank. ')
BG = {
    'office': 'Front view of the waiting hall of a shabby Russian social security office: along the back wall three service windows, each a '
              'counter with a glass partition and a small arched opening at counter height, behind the glass a dim clerk space with shelves '
              'of paper folders; a row of joined metal waiting chairs on the left, a big potted rubber plant, an empty water cooler, a blank '
              'electronic queue display above the windows, a blank notice board, worn linoleum floor with an empty open space in the '
              'middle foreground, fluorescent tubes on the ceiling, one of them flickering.',
    'desk': 'Close view of a clerk workplace behind a service window, seen from the customer side through the glass: a desk with a big '
            'stack of thick paper folders, an old computer monitor, a rubber stamp and an ink pad, a cup of tea and a plate of ring biscuits, '
            'a desk lamp, behind it a wall with a blank tear-off calendar, a blank framed certificate, a grey electrical panel box with a small '
            'red light, a window with a dark night sky; the lower foreground is the counter edge and the glass frame.',
    'flat': 'Interior of an old Soviet Khrushchev-era apartment living room, front view: a big red patterned carpet hanging on the left wall, '
            'a tall polished wooden sideboard with glass doors full of crystal glasses and vases on the left, a cast-iron radiator under a '
            'window with lace curtains in the middle, an old tube TV with a rabbit-ears antenna on a small table on the right, a worn sofa, '
            'a tear-off calendar on the wall, a ceiling lamp with a fringed shade, cobwebs in the corners, wooden parquet floor with an empty '
            'open space in the middle foreground, a dark night window with a faint green moon.',
    'stairs': 'Interior of a shabby Soviet apartment-block stairwell landing at night, front view: two padded apartment doors (one left, one '
              'right), between them on the wall a grey metal electrical panel box with a small door, a bare light bulb hanging on a wire, '
              'a flight of concrete stairs with a metal railing going up on the right, a row of dented blue metal mailboxes, a garbage chute '
              'hatch, walls painted green on the bottom and white on top, peeling paint, a dusty window; empty floor space in the middle '
              'foreground.',
    'yard': 'An old Soviet panel apartment block courtyard in late October at dusk, side view: the building entrance with a heavy metal door '
            'and a small concrete canopy on the left, a wooden bench beside it, a big above-ground heating pipe wrapped in torn insulation '
            'running horizontally across the middle of the yard at knee height with a little steam, a rusty swing set and a sandbox on the '
            'right, bare birch trees with a few yellow leaves, puddles and fallen leaves on the cracked asphalt, rows of lit windows in the '
            'background buildings, purple sky with a green-tinted moon; open empty asphalt across the lower third.',
    'facade': 'Looking up at the facade of a five-storey Soviet panel apartment block at night from the courtyard: rows of windows, some lit '
              'warm yellow, glazed and open balconies with laundry lines, a satellite dish, potted plants, two balconies one above the other '
              'in the centre of the image, a purple night sky with a big moon; strong upward perspective.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    total = 0.0
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists(): continue
        total += xai.generate(STYLE + BG[n], [str(p)], aspect='16:9')
    print('total $%.3f' % total)
