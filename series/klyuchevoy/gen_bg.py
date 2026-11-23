"""xAI backgrounds for «Ключевой сотрудник» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/klyuchevoy/gen_bg.py [names...]       python3 series/klyuchevoy/gen_bg.py night   (edit of office.png, same layout)
Heroes, the ficus, every sign / poster text, the wall clock, light and particles are drawn in code on top; no people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, crisp visible pixels, rich but '
         'uncluttered detail, warm nostalgic post-soviet office mood, beige, mustard, olive green, brown and pale yellow palette with '
         'cool greenish fluorescent light, like a modern indie pixel adventure game, wide 16:9 scene, strong sense of depth with clear '
         'foreground, middle ground and far background. No characters, no people, no animals, no plants, no text, no letters, no '
         'numbers, no logos; every poster, sign, notice board, screen and frame is completely blank. ')
BG = {
    'office': 'Eye-level wide view of a shabby open-space office of a small Russian trading company at 6 pm in late November: '
              'on the left a closed tall dark wooden office door with a blank brass name plate (the boss office), a blank round wall '
              'clock above it; in the middle two rows of beige office desks with low grey partitions, old chunky beige computer '
              'monitors with blank glowing screens, office chairs, paper stacks, a desk lamp, cables; on the back wall a blank honor '
              'board with empty photo frames and a blank poster; on the right a big window with half-open dusty horizontal blinds, '
              'blue-violet winter dusk outside with falling snow and lit windows of panel buildings far away, a wide empty white '
              'windowsill, a radiator under it, a water cooler with a big blue bottle next to the window, an old grey laser printer on '
              'a small table. Fluorescent ceiling tubes glowing, worn brown linoleum floor across the lower third.',
    'kassa': 'Eye-level straight-on view of a narrow corridor wall in the same shabby post-soviet office: in the center a small cashier '
             'window cut in the wall at chest height, with a thick glass pane, a semicircular opening at the bottom and a narrow wooden '
             'counter shelf in front of it; behind the glass a cramped accounting room with shelves of thick binders, an old adding '
             'machine, a desk lamp and a kettle; on the wall left of the window a big blank paper chart grid pinned to the wall (a '
             'schedule table with empty cells), on the right a blank notice board with pinned blank papers and a fire extinguisher; '
             'beige painted walls with an olive green lower half, fluorescent ceiling tubes, worn brown linoleum floor across the lower '
             'quarter, a wooden bench along the wall.',
}

NIGHT = ('Exactly the same office, same furniture, same composition, same camera, but late at night: all ceiling lights off, the room is '
         'dark blue, only one warm desk lamp glowing in the middle, monitor screens dim blue, black night outside the window with snow and '
         'a few lit windows far away, cold moonlight through the blinds. Still no people, no plants, no text.')
MORNING = ('Exactly the same office, same furniture, same composition, same camera, but at 8 am on a grey winter morning: pale bluish '
           'daylight from the window, ceiling fluorescent tubes on, snowy morning outside. Still no people, no plants, no text.')

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        if n in ('night', 'morning'):
            o = OUT / f'office_{n}.png'
            if o.exists(): print('skip', n); continue
            xai.generate(STYLE + (NIGHT if n == 'night' else MORNING), [str(o)], ref_png=str(OUT / 'office.png'))
            continue
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
