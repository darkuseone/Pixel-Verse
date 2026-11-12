"""xAI backgrounds for «STILL 1986» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/still-1986/gen_bg.py [names...]        python3 series/still-1986/gen_bg.py night   (edit of ocean.png, same layout)
Heroes, the car, the tow truck, Fran (the neon flamingo), every sign text, light and particles are drawn in code on top;
backgrounds have no people, no cars and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, crisp visible pixels, rich but '
         'uncluttered detail, 1980s Miami retro synthwave mood, hot pink, coral, peach, turquoise and violet palette, like a modern indie '
         'pixel adventure game, wide 16:9 scene, strong sense of depth with clear foreground, middle ground and far background. '
         'No characters, no people, no animals, no cars, no vehicles, no text, no letters, no numbers, no logos; every sign, neon sign, '
         'banner, awning and window is completely blank. ')
BG = {
    'ocean': 'Eye-level side view across a wide empty beach-front boulevard in Miami Beach at sunset, looking at a row of pastel art deco '
             'hotels: left a mint green hotel with rounded corners and a porthole window, middle a pink hotel with a tall vertical blank '
             'neon sign fin and horizontal eyebrow ledges, right a lavender hotel with a blank neon marquee and a sidewalk cafe with '
             'empty bistro tables under a striped awning. Glowing turquoise and pink neon tube outlines along the cornices, all signs '
             'blank. Tall palm trees in front of the hotels. Behind and above: a huge dramatic sunset sky, big orange-pink sun low behind '
             'the buildings, purple and peach clouds. Foreground: an old single-head parking meter on a pole at the curb on the left, '
             'a light grey sidewalk, a white curb, and an empty dark asphalt street with faded white parking lines across the whole '
             'lower third. Warm sunset backlight, pink rim light on edges.',
    'side': 'Eye-level side view of a quiet side street one block off a Miami Beach boulevard at dusk, blue hour: left an art deco '
            'parking garage with a curved concrete facade and blank neon strips, middle a chain-link fence lot with a blank metal sign '
            'board, a tall palm tree, a fire hydrant, right a small pastel yellow motel with a blank neon arrow sign and an ice machine. '
            'Deep violet and magenta sky with the last orange glow on the horizon, the first stars, warm street lamps turning on. '
            'Foreground: sidewalk with a low curb and an empty asphalt street across the whole lower third, puddles reflecting neon.',
    'club': 'Eye-level side view of the entrance of a retro 1980s Miami Beach nightclub at night: a pastel art deco facade with glowing '
            'pink and turquoise neon tube outlines, a big blank marquee sign above double doors with chrome handles, on the right a small '
            'ticket booth with a glass window, a round speaker grille and a counter slot, a blank screen inside the booth; red velvet rope '
            'on chrome posts in front, a short red carpet, palm trees in pots, a wet sidewalk reflecting neon across the lower third, '
            'purple night sky. Empty, no people.',
    'disco': 'Interior of a retro 1980s neon nightclub dance floor at night, eye-level wide view: a glowing checkered light-up dance floor '
             'in pink, turquoise and yellow squares across the lower third, a mirror ball hanging from the ceiling, purple haze, neon tube '
             'lines on dark walls, a DJ booth with blank screens at the back, a bar with stools at the side, light beams from the ceiling. '
             'Empty, no people.',
    'marina': 'Eye-level side view of a Miami marina at sunset: a long wooden dock with bollards and coiled ropes across the lower third, '
              'a small blank rental shack with a striped awning and a big blank chalkboard sign on the left, white sailboats and yachts '
              'in the water behind, palm trees, the Miami skyline far away across the bay, a huge orange-pink sunset sky reflected in '
              'calm water. Empty, no people, no small boats on the dock side.',
    'bay': 'Wide open Biscayne Bay water at sunset seen from water level: calm rippling water across the lower half with long golden '
           'and pink sun reflections, the Miami skyline with pastel towers and a long causeway bridge far away, a few distant sailboats, '
           'a huge glowing sunset sky with purple clouds. Empty, no people, no boats in the foreground.',
    'mall': 'Eye-level side view of the outside of a big electronics store in an outdoor Miami shopping mall at midnight: a wide glass '
            'storefront with closed sliding doors and a metal security gate half down, glowing screens and boxes visible inside, a big '
            'blank neon sign above, blank posters in the windows, queue barrier posts with belts along the sidewalk, palm trees in '
            'planters, mall lamps glowing, a dark purple night sky. Empty sidewalk across the lower third, no people.',
    'studio': 'Interior of a small cluttered retro studio apartment at night, eye-level side view: left an old chunky CRT television on '
              'a low wooden stand with a game console and tangled cables, a beanbag chair and a pink couch in the middle, blank framed '
              '80s posters on the walls, a lava lamp, a rotary-style phone, VHS tapes; right a big window with blinds open showing the '
              'night street outside with neon signs glowing pink and turquoise across the street; a ceiling fan, warm lamp light. '
              'Wooden floor across the lower third, empty, no people.',
}

NIGHT = ('Exactly the same scene, same buildings, same composition, same camera, but at night: black-violet night sky with stars, '
         'all the neon tube outlines and the blank neon signs glowing bright hot pink and turquoise, warm lit windows, street lamps on, '
         'neon reflections on the wet asphalt, palm trees as dark silhouettes against the glow. Still no people, no cars, no text.')

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        if n == 'night':
            o = OUT / 'ocean_night.png'
            if o.exists(): print('skip night'); continue
            xai.generate(STYLE + NIGHT, [str(o)], ref_png=str(OUT / 'ocean.png'))
            continue
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
