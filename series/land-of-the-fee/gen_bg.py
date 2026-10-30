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
    'leasing': 'Interior of a glossy American apartment complex leasing office, eye-level wide view. Left: a white modern desk with a laptop, '
               'a bowl of candy and a small potted succulent, two chairs in front of it. Back wall: big blank framed posters, a glass door to the '
               'outside, a wall-mounted blank screen, a shelf with blank binders and a coffee machine. Right: a big window showing a sunny '
               'apartment complex courtyard. Light grey walls with a navy accent wall, pendant lamps, a beige carpet across the lower third, '
               'empty, no people. Bright warm daylight.',
    'courtyard': 'A small sad apartment complex courtyard on a sunny afternoon, eye-level wide view. Middle: a tiny round inflatable kiddie pool '
                 'on dry patchy grass. Left: a wooden fence with a blank sign board, a lonely plastic lounge chair. Right: a concrete pad with an '
                 'old exercise mat, a vending machine with blank labels against the wall. Background: three-story beige apartment buildings with '
                 'small balconies, air conditioner units, a dumpster, power lines and a blue sky. Patchy grass and concrete across the lower third, '
                 'empty, no people, no animals.',
    'roof': 'The flat tar rooftop of a three-story American apartment building on a sunny afternoon, eye-level wide view. Middle: a big '
            'galvanized steel HVAC unit with a round vent cap on top, a satellite dish, pipes and a small roof access door hut on the left. '
            'Background: a suburban skyline with other flat roofs, a water tower, power lines, palm-less trees, a blue sky with puffy clouds. '
            'Grey gravel roof surface across the lower third, empty, a low brick parapet at the front edge, no people, no birds.',
    'er': 'Interior of a small American hospital emergency room bay, eye-level wide view. Middle: a hospital bed with white sheets and a raised '
          'back, a metal IV pole on the right of it, a vital signs monitor on a wall arm with a blank screen, a pastel blue privacy curtain '
          'half drawn on a ceiling rail on the left. Back wall: pale green tiles, a blank whiteboard, a hand sanitizer dispenser, a glove box '
          'holder, a small window with blinds. Right: a rolling cart with a blank box printer on top and supply drawers. Speckled vinyl floor '
          'across the lower third, empty, no people. Cold fluorescent ceiling light.',
    'tower': 'A tall modern glass office skyscraper seen from across a city street on a sunny day, eye-level looking slightly up. The tower '
             'fills the middle and right with a huge mirror-like blue glass facade reflecting clouds and the sky. Left: a smaller brick '
             'building, a street lamp, a blank billboard on a pole. Blue sky with puffy clouds at the top. A sidewalk and street across the '
             'lower part, empty, no people, no cars, no birds.',
    'billing': 'Interior of a cramped hospital back office, eye-level wide view. Left half: a doctor desk with a beige computer, a desk lamp, '
               'blank framed diplomas on the wall, a skeleton model, a coat hook. Right half, right next to it: an insurance call center '
               'cubicle desk with a headset hook, a phone, a stack of paper forms, a blank motivational poster on a grey cubicle wall. One '
               'single rolling office chair between the two desks. Fluorescent light, a water cooler, grey carpet across the lower third, '
               'empty, no people.',
    'street': 'A modest American suburban street on a sunny morning, eye-level side view. Background: a small beige ranch house with a '
              'garage, a mailbox on a post, a lawn with a few dandelions, a basketball hoop over the garage, power lines, a blue sky. The '
              'concrete driveway in the middle foreground is EMPTY. A sidewalk and the street asphalt across the lower third, empty, no cars, '
              'no people, no animals.',
    'highway': 'A wide American interstate highway seen from the side and slightly above on a sunny day: a long traffic jam of many cars and '
               'trucks bumper to bumper on all lanes in the lower half, a concrete median barrier, blank green overhead highway signs on a '
               'gantry, light poles, distant hills, billboards with blank faces, a big open blue sky with clouds in the upper half. No people, '
               'no text, no birds.',
    'shoulder': 'The grassy shoulder of an American interstate highway on a sunny day, eye-level side view: dry grass and a gravel shoulder '
                'across the lower third (empty), a metal guardrail, behind it the highway with a traffic jam of cars, a blank green highway '
                'sign on a post, power lines, a blue sky. No people, no text.',
    'stadium': 'Outside a big American concert stadium at sunset, eye-level wide view: a tall curved concrete stadium wall with arched gates '
               'and closed metal turnstiles, huge blank banners hanging on the wall, stadium light towers glowing, an orange and purple '
               'sunset sky. In front: an empty parking lot with painted lines, a concrete curb and a sidewalk across the lower third, a few '
               'traffic cones, a trash can. No people, no text.',
    'stage': 'Inside a big rock concert arena at night, view from the crowd floor toward the stage: a wide black stage with stacks of '
             'speakers on both sides, a drum riser, microphone stands, colorful stage lights and light beams cutting through haze, a huge '
             'blank video screen above the stage, trusses with lamps. The crowd floor in the lower third is EMPTY dark floor. No people, '
             'no text, no logos.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    usd = 0.0
    for n in names:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        usd += xai.generate(STYLE + BG[n], [str(out)])
    print('total $%.2f' % usd)
