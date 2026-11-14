"""xAI backgrounds for «Замело» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/zamelo/gen_bg.py [names...]
Heroes, the seagull, every sign text, snowfall, light and particles are drawn in code on top;
backgrounds have no people, no animals, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, crisp visible pixels, rich but '
         'uncluttered detail, cosy funny wintry Russian Far East mood, palette of warm sunrise orange, peach and pink light against '
         'blue-violet snow shadows and bright white snow, like a modern indie pixel adventure game, wide 16:9 scene, strong sense of depth '
         'with clear foreground, middle ground and far background. No characters, no people, no animals, no birds, no cars, no vehicles, '
         'no text, no letters, no numbers, no logos; every sign, poster and plate is completely blank. ')
BG = {
    'yard': 'Wide eye-level view from standing on top of a gigantic snowdrift that has buried a Soviet-era town in the Russian Far East: '
            'rows of grey-beige nine-storey prefab panel apartment blocks buried in snow up to the windows of their top floor, so only '
            'the top-floor windows, a few glassed-in balconies and the flat roofs with antennas stick out above a smooth white snow plain. '
            'The snow plain is the ground across the whole lower third, with trodden footpaths, the glass heads of old street lamps '
            'sticking out of the snow at knee height, the roof of a buried bus stop, the bare tips of birch trees. Far behind: a big '
            'snow-capped volcano cone with a thin plume of smoke, the tops of harbour cranes sticking out of the snow, low snowy hills. '
            'Clear frosty morning, low warm orange-pink sun, long blue shadows, sparkling snow, pale turquoise sky.',
    'facade': 'Eye-level close view of the top floor of a Soviet nine-storey prefab panel apartment block buried in snow right up to the '
              'bottom of the top-floor windows: a flat white snow surface is the ground across the lower third. In the centre a wide old '
              'wooden double window stands WIDE OPEN, showing a dim cosy Soviet kitchen inside (net curtains, a warm lamp, a shelf). '
              'Beige-grey concrete wall panels with dark joints, a neighbour\'s glassed-in balcony on the left, a closed window on the '
              'right, a row of icicles hanging from the roof edge at the top, a strip of blue sky and the top of another buried block '
              'far behind. Soft warm morning sunlight, blue-violet snow shadows.',
    'kitchen': 'Interior of a small cosy Soviet-era apartment kitchen, eye-level side view: on the left an old white gas stove with a '
               'kettle and a steaming pot, an old rounded fridge, a small table with an oilcloth tablecloth and two stools, a patterned '
               'carpet hanging on the wall, a cupboard with crockery; on the right a large window - outside the window the snow is level '
               'with the windowsill, a bright white snow surface, blue sky and the tops of other buried apartment blocks. Bright cold '
               'daylight from the window and a warm orange lamp, linoleum floor across the lower third.',
    'door': 'Eye-level view at the bottom of a deep narrow pit dug down through snow: in the centre the old metal entrance door of a '
            'Soviet apartment block with a small concrete canopy above it, an intercom panel beside it, the door covered with white '
            'frost and icicles; tall smooth snow walls on the left and right with shovel marks, going up out of frame; cold blue-white '
            'light falling from high above, a packed snow floor and one concrete step in front of the door across the lower third.',
    'landing': 'Interior of the top-floor stairwell landing of a Soviet apartment block, eye-level view: in the centre an old padded '
               'brown leatherette apartment front door with a small doormat in front of it; on the right a steel ladder going up to an '
               'open roof hatch with bright daylight and a few snowflakes falling through it; walls painted green below and white above, '
               'a radiator, an electricity meter box, on the left a window completely blocked by packed snow glowing blue, a tiled floor '
               'across the lower third.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
