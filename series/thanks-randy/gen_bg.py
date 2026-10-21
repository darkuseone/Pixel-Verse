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
    'airport': 'Interior of a small American desert airport security checkpoint, eye-level side view. In the middle a long grey X-ray '
               'baggage scanner machine with a black rubber conveyor belt running from left to right through a boxy tunnel with rubber '
               'flaps, stacks of empty grey plastic bins at its left end, a steel roller table at its right end. On the right a tall '
               'cylindrical full-body scanner booth with clear curved glass walls. Background: big windows with a sunny Arizona desert, '
               'saguaro cactuses, red mesas and a parked airplane tail, blue sky; blank hanging signs, retractable belt queue posts, a '
               'blank monitor on a stand. Clean shiny grey floor across the lower third, empty. Bright cool airport light with warm '
               'desert sun from the windows.',
    'airport_b': 'Close view of an airport security X-ray conveyor belt and its scanner tunnel with rubber flaps, seen from the side at '
                 'table height, grey plastic bins on the belt rollers, a blank operator monitor on an arm, a steel table, a small locked '
                 'box for confiscated items, behind it big windows with a sunny Arizona desert, saguaro cactuses and red mesas, blue sky. '
                 'Bright cool airport light, shiny grey floor, empty, no people.',
    'kitchen': 'Interior of a cozy cluttered American suburban kitchen at 3 AM, eye-level side view. Left: a white fridge covered with '
               'blank paper notes and magnets and kids drawings of hand turkeys; middle: a kitchen counter with a deep steel sink under a '
               'dark window with blue moonlight, a dish rack, a roll of paper towels, a toaster, a coffee maker; right: a wooden back door '
               'with a small window and a coat hook, a wall clock, an autumn wreath. Warm yellow under-cabinet light over the counter, cold '
               'blue moonlight from the window, a hanging lamp. Linoleum floor across the lower third, empty, a small kitchen table with '
               'chairs at the far right. Blank calendar, blank whiteboard on the fridge.',
    'callcenter': 'Interior of a busy small-town turkey hotline call center at night, eye-level view: rows of beige office cubicles with '
                  'desks, old computer monitors with blank screens, desk phones, headsets on hooks, coffee mugs, stacks of paper, '
                  'potted plants; on the back wall a big blank digital counter board and blank framed posters; fluorescent ceiling '
                  'lights, one flickering; a big window with a dark night sky and snow. Carpeted floor across the lower third, empty, '
                  'no people.',
    'yard': 'An American suburban house front yard in Ohio on a cold November morning, eye-level side view. Left: a two-car garage '
            'attached to a beige house with its big garage door wide open (dark empty inside with shelves and a lawnmower), a concrete '
            'driveway in front of it; middle: a front lawn covered with fallen yellow and orange maple leaves, a curbside mailbox on a '
            'post, a bare maple tree; right: the front porch with steps, a front window, pumpkins on the steps, corn stalks tied to the '
            'porch post. A neighbor house far right, grey overcast sky. Flat open driveway and lawn across the lower third, empty, '
            'no people, no cars.',
    'living': 'Interior of a cozy American suburban living room and dining area on Thanksgiving evening, eye-level side view. Left: a '
              'big flat TV on a low wooden TV stand (black blank screen), a game console, a potted plant; middle: a long dining table '
              'with a white tablecloth, plates, glasses, candles, autumn leaves centerpiece, mashed potatoes, green bean casserole, '
              'cranberry sauce, rolls, an EMPTY big platter in the center; right: a brown leather recliner, a small separate low '
              'folding kids table with a paper tablecloth and a tiny chair; on the walls: a blank wooden decor sign, framed family photos, '
              'a window with dark evening blue sky and warm lamp light. Warm cozy yellow lamp light, hardwood floor across the lower '
              'third, empty, no people.',
    'bbout': 'Outside a big American electronics superstore at 4:59 AM on Black Friday, eye-level side view: a wide store front with '
             'big glass sliding doors in the middle (lights on inside, a pyramid of big TV boxes visible through the glass), a blank '
             'store sign above, blank banners in the windows, a long line of empty folding camping chairs and small camping tents along '
             'the sidewalk, a shopping cart corral, frost on the glass, a dark blue dawn sky with the first pink light, parking lot lamps '
             'glowing, cold breath mist. Flat sidewalk across the lower third, empty, no people.',
    'bbin': 'Interior of a big American electronics superstore on Black Friday morning, eye-level view: a huge pyramid of flat-screen TV '
            'boxes in the center, walls of glowing TV screens showing colorful blank screens, aisles with laptops and speakers, '
            'hanging blank yellow and blue sale banners, a row of two self-checkout kiosks with a bagging shelf on the right side, '
            'bright white store lights, a shiny grey floor with scattered fallen shoes and a lost shopping cart, empty, no people.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
