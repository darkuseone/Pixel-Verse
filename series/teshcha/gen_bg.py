"""xAI backgrounds for «Тёща на недельку» (16:9 1280x720, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/teshcha/gen_bg.py [names...]
Heroes, props (armchair, bags, camp bed), notices, labels, light and particles are drawn in code; backgrounds have no people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, cosy retro 90s sitcom look, modern indie pixel-art adventure game style, crisp visible '
         'pixels, rich environmental detail, warm saturated colours, small Soviet panel-block apartment, wide 16:9 scene, front view, '
         'eye level. No characters, no people, no animals, no text, no letters, no numbers, no symbols; any signs, labels, calendars, '
         'posters and papers are completely blank. ')
BG = {
    'landing': 'A stairwell landing of a Soviet nine-storey panel block in the evening. On the right third: a padded brown leatherette '
               'apartment front door with brass studs swung wide open, through it a warm yellow-lit narrow apartment hallway with a coat '
               'rack, a mirror and a patterned runner rug. On the left third: an old elevator with closed sliding grey metal doors in a '
               'painted frame and a call button. Walls painted two-tone: lower half mustard-ochre gloss paint, upper half dirty whitewash '
               'with peeling patches; a small blank cork notice board with blank papers pinned; a bare light bulb in a wire cage on the '
               'ceiling; at the lower left concrete stairs going down with a green-painted metal railing and a wooden handrail; a dusty '
               'radiator; grey speckled terrazzo floor; a worn rubber doormat in front of the open door. The middle of the floor is clear '
               'empty space.',
    'room': 'A cramped living room of a small Soviet two-room apartment in the evening, warm lamp light. On the back wall a big '
            'red-and-burgundy oriental carpet hanging on the wall; on the left a tall lacquered brown wall unit with glass doors full of '
            'crystal glassware and porcelain sets; on the far right a window with white tulle curtains, dark blue evening sky and lights of '
            'panel blocks outside, a radiator under it with houseplants on the sill; a floor lamp with a fringed orange shade; a small old '
            'TV on a wooden stand at the right edge; a glossy freshly washed parquet floor with reflections; a doorway on the far left to a '
            'dark hallway; a wall clock and family photos in frames. The centre and centre-right of the room in front of the carpet is '
            'empty floor space with nothing standing there.',
    'balcony': 'A narrow glazed Soviet apartment balcony at night in winter. Old white-painted wooden window frames along the back with '
               'frosted cracked glass, snow blowing in through gaps, outside a snowy night city of panel blocks with warm lit windows and '
               'falling snow. The balcony is packed with junk along the walls: glass preserving jars on wooden shelves at the right, old '
               'wooden skis and a sled leaning on the wall, a bicycle wheel, cardboard boxes, an old car tyre, a metal basin; on the far '
               'left a glazed balcony door leading into a warm yellow-lit room. Cold blue moonlight and the warm light from the door. '
               'The floor in the middle is clear empty space.',
}


def main(names):
    for n in names or BG:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        xai.generate(STYLE + BG[n], [str(out)], aspect='16:9')
        print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1:])
