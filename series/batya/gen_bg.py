"""xAI backgrounds for «Батя сам» (16:9 1280x720, grok-imagine-image-2.0, ~$0.04–0.06 each). Skips existing files.
  python3 series/batya/gen_bg.py [names...]
Heroes, blankets, the nightstand pharmacy, pots, smoke, signs, labels, light and particles are drawn in code; backgrounds have no
people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, cosy retro 90s sitcom look, modern indie pixel-art adventure game style, crisp visible '
         'pixels, rich environmental detail, warm saturated colours, small Soviet panel-block apartment in late November, wide 16:9 scene, '
         'front view, eye level. No characters, no people, no animals, no text, no letters, no numbers, no symbols; any signs, labels, '
         'calendars, certificates, posters and papers are completely blank. ')
BG = {
    'bedroom': 'The parents\' bedroom in the evening, warm yellow lamp light and a cold dark blue window. In the centre-left a wide double '
               'bed with a tall glossy polished dark-wood headboard against the back wall, a smooth plain beige bedspread and two white '
               'pillows, the top of the bed is clear and flat. On the back wall above the bed a huge red-and-burgundy oriental carpet '
               'hanging on the wall. To the right of the bed a small polished wooden nightstand with an empty top and a table lamp with a '
               'pleated orange shade. On the far left a tall lacquered brown wall unit with glass doors, crystal glassware and porcelain '
               'behind the glass. On the right a window with white tulle and heavy curtains, dark blue November evening sky, snowflakes and '
               'lit windows of panel blocks outside, a radiator under the window. On the far right edge a half-open white-painted door to a '
               'dark hallway. Parquet floor with a small rug. Blank framed certificate and a blank wall calendar on the walls.',
    'kitchen': 'A tiny Soviet panel-block kitchen in the evening, warm ceiling lamp light, dark blue window. In the centre-left an old white '
               'four-burner gas stove with an oven, the stove top is clear and empty, a light-blue tiled wall behind it with a rooster tile '
               'strip, a small extractor hood. On the far left an old white rounded fridge with many fridge magnets. On the back wall a '
               'window with tulle and pots of seedlings on the sill, wooden wall cupboards with glass jars of buckwheat and salt. On the right '
               'a small kitchen table with a checked oilcloth tablecloth, a stool, a radio on a shelf, a blank wall calendar. Worn linoleum '
               'floor. The floor in the middle is clear empty space.',
    'yard': 'A courtyard of Soviet nine-storey panel blocks on a frosty winter morning at dawn, minus twenty degrees: deep fresh snow, '
            'a row of old snow-covered Soviet cars parked along the building in the middle ground; in the centre an old boxy red Lada '
            'hatchback with its hood closed, the snow brushed off it, standing on a cleared patch of snow; on the right the entrance '
            'porch (podyezd) of the building with a metal door, a small canopy and a bench covered with snow; on the left a lamp post '
            'with a warm light and a bare tree with frost; on the building wall next to the door a round blank wall plate; frosty haze, '
            'pink-blue sky, lit windows. The snowy ground in the front is clear empty space.',
    'balcony': 'A narrow glazed Soviet panel-block balcony (loggia) at night, cluttered: on the left old wooden window frames with single '
               'glass, dark blue night outside with snow and lit windows of panel blocks across the yard. In the centre against the back '
               'brick wall an old white rounded Soviet chest freezer with a closed lid and a chrome handle, frost on it, a small blank '
               'metal plate on its front. To the right of the freezer an old oil-filled electric radiator heater glowing warm orange, and '
               'wooden boxes of green seedlings on a shelf under a pink-purple grow lamp. Clutter: three-litre glass jars on shelves, old '
               'skis, a bicycle wheel, a sledge, a cardboard box, an old stool, a bare light bulb hanging from a wire. Worn painted wooden '
               'floor. On the far right edge a white balcony door with glass to the dark apartment. The floor in front of the freezer is '
               'clear empty space.',
    'hall': 'A dark narrow Soviet apartment hallway at night, all lamps off, cold blue moonlight from the kitchen door. On the left wall at '
            'eye level an old grey electricity meter box with a round glass window and a spinning disc, a blank paper notice under it. A '
            'coat rack with winter coats and fur hats, a shoe shelf with boots, a mirror, an old wall telephone, wallpaper with a faded '
            'pattern. On the right a doorway to a dark room. Worn parquet floor with a long runner rug. The floor in the middle is clear '
            'empty space.',
    'room': 'The living room of a small Soviet panel-block apartment in the evening, warm ceiling lamp light, cold dark blue window. '
            'In the centre against a plain wallpapered wall a wide clear empty space of bare wall and floor (where new furniture will '
            'stand), with torn brown cardboard, styrofoam pieces and bubble wrap scattered on the floor. On the left an old sofa with a '
            'crocheted blanket and a small tube TV on a stand. On the right a window with tulle, a radiator, and a door to the hallway. A '
            'patterned rug on the parquet floor, a ceiling lamp with a glass shade, a wall clock. The floor in the middle is clear.',
    'garage': 'Inside an old Soviet brick garage (garage cooperative) on a late November afternoon, a warm work lamp light: a long '
              'wooden workbench along the back wall covered with tools, a vice, jars of screws, wood shavings and sawdust everywhere on '
              'the concrete floor, planks of wood leaning on the wall, old tyres, a shelf with paint cans, a calendar and a blank poster '
              'on the wall, an old radio, a hanging bulb, the half-open metal garage door on the right showing grey snowy daylight. '
              'The floor in front of the workbench is clear empty space.',
}


def main(names):
    for n in names or BG:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        xai.generate(STYLE + BG[n], [str(out)], aspect='16:9')
        print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1:])
