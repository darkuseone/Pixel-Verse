"""xAI backgrounds for «Agent Dibs» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/agent-dibs/gen_bg.py [names...]
Heroes, signs, light, snow and particles are drawn in code on top; the backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, modern indie pixel-art adventure game look, crisp visible pixels, rich environmental detail, '
         'cinematic night lighting, wide 16:9 scene. No characters, no people, no animals, no text, no letters, no numbers; '
         'any signs, boards and papers are completely blank. ')
BG = {
    'dibs_row': 'Deep-winter night on a Chicago residential side street at street level: brick two-flat apartment buildings with wooden porches '
                'and lit windows with closed curtains on the left and right, cars buried in snow along both curbs, the plowed street running to the '
                'back, elevated train tracks glowing far at the end of the street, orange sodium streetlamps, falling snow, steam rising from a '
                'manhole. In the empty foreground, centre, a freshly shoveled empty parking spot between two tall piles of snow at the curb. '
                'Along the curbs a few parking savers: an old plastic lawn chair, an orange traffic cone, an ironing board, a plastic kiddie pool. '
                'Deep navy sky, warm orange light pools on the snow, wide empty street in the lower third.',
    'lair_lobby': 'Interior of a villain skyscraper lobby at night: glossy black-and-white checkered marble floor, a long security desk on the left, '
                  'floor-to-ceiling windows on the right showing a glowing Chicago-style skyline at night, a mezzanine balcony with a railing high '
                  'above, large potted palms, a gold elevator door at the back, teal and magenta neon accent strips, a big blank plaque wall. '
                  'Empty lobby with wide open marble floor in the centre.',
    'avenue_under_L': 'Side view of a wide Chicago avenue at night running left to right under an elevated train structure: steel girders, columns '
                      'and tracks across the top of the frame with warm sparks, snow-dusted wet asphalt road in the lower half full of large deep '
                      'potholes and cracks, orange sodium streetlights, closed storefronts with shuttered doors along the back, a traffic light '
                      'on a pole, falling snow, deep blue sky. The road is empty and wide.',
    'sals_stand': 'Corner Italian beef and hot dog stand at night on a snowy city street, side view: a small brick shack with a large service '
                  'window glowing warm yellow and an empty blank neon sign frame above it, string lights, a steel counter ledge, steam from a roof '
                  'vent, snow piled on the sidewalk, a green dumpster and a metal trash can on the right, a few picnic tables dusted with snow, '
                  'cold blue night with falling snow, wide empty sidewalk and street in front where a crowd could stand.',
    'skyline_river': 'A Chicago-style skyline at night seen across a dark river: tall glass skyscrapers, one with an X-braced facade and two '
                     'antennas, a pair of round corn-cob shaped towers, a bridge over the river with glowing reflections, snowy riverwalk with '
                     'lamps, windy sky with streaks of clouds and a pale moon, neon accents in cyan and orange, large calm sky area above.',
    'field_office': 'Cramped 1990s government field office interior seen head-on: wood-paneled wall, a big corkboard with index cards and red '
                    'string, a crockpot with rising steam on a filing cabinet, an old fax machine, a wooden desk in the lower foreground with a '
                    'beige landline phone with a curly cord and a coffee mug, a flickering fluorescent ceiling light, a calendar, Christmas lights '
                    'around a window with snow falling outside. Warm cozy but shabby. Empty office, the area behind the desk in the centre is open.',
    'bean_plaza': 'Night city park plaza dominated by a giant polished stainless-steel bean-shaped sculpture reflecting the glowing skyline and '
                  'sky, a wide stone plaza floor with snow flurries, skyscrapers behind, strings of lights, a wide empty open area in the '
                  'foreground, cinematic blue and orange light.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    total = 0.0
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists():
            continue
        total += xai.generate(STYLE + BG[n], [str(p)], aspect='16:9')
    print('total $%.3f' % total)
