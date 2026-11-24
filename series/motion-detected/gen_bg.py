"""xAI backgrounds for «MOTION DETECTED» (US, 16:9, ~$0.06 each). Skips existing files.  python3 series/motion-detected/gen_bg.py [names...]
Heroes, the doorbell Doris, every sign / text, the porch light glow, leaves and particles are drawn in code on top; no people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, crisp visible pixels, rich but '
         'uncluttered detail, cozy American suburbia mood, saturated colors: warm cream siding, brick red, forest green, pumpkin orange, '
         'and a vivid purple-pink sunset sky, like a modern indie pixel adventure game, wide 16:9 scene, strong sense of depth with clear '
         'foreground, middle ground and far background. No characters, no people, no animals, no text, no letters, no numbers, no logos, '
         'no house numbers; every sign, mailbox side and doormat is completely blank. ')
BG = {
    'porch': 'Eye-level wide view of the covered front porch of a two-story cream-sided suburban American house at dusk in late November. '
             'On the left third a closed glossy dark green front door with a brass handle and a tall narrow vertical glass sidelight '
             'window right next to it, a plain blank rectangular doormat in front of it, a warm glowing porch lamp on the wall, an autumn '
             'wreath of orange leaves on the door, two white porch columns, a white wooden railing, a wooden plank porch floor across the '
             'lower third, two carved pumpkins and a potted plant by the steps. On the right two thirds: three wide steps down to a front '
             'lawn with fallen orange leaves, a concrete path, a blank black mailbox on a post at the curb, the street, and across the street '
             'two neighbor houses, one already covered with colorful Christmas string lights, bare trees, a purple and orange dusk sky.',
    'hall': 'Eye-level wide view from inside the entry hall of an American suburban house in daylight, looking straight at the inside of '
            'the closed front door: on the left third a white front door with a brass knob and a tall narrow frosted glass sidelight window '
            'next to it glowing with daylight, a plain blank doormat inside, coat hooks with jackets and a baseball cap, a small wooden '
            'console table with a bowl for keys; in front of the door, in the middle, a single empty wooden kitchen chair standing alone and '
            'facing the door; on the right a carpeted staircase going up with white banisters, a family photo wall with blank frames, a '
            'beige wall, a small window with blinds, hardwood floor with a striped runner rug across the lower third.',
    'breakroom': 'Eye-level wide view of a small American corporate office break room during the holiday party in early December: on the '
                 'left a long white table with a red plastic tablecloth and a pile of colorfully wrapped gift boxes of different sizes, paper '
                 'plates, a bowl of red punch, cookies; in the middle back a small sad fake Christmas tree with tinsel and a few ornaments, a '
                 'string of paper snowflakes along the wall, a blank whiteboard on the wall, a fridge covered with blank notes, a coffee '
                 'machine and a microwave on a counter; on the right a grey cubicle partition wall, a window with blinds showing a snowy '
                 'parking lot at dusk, a water cooler, a blank framed poster; fluorescent ceiling lights, grey-blue carpet across the lower third.',
    'postoffice': 'Eye-level view of the inside of a small American post office in December: in the middle a long service counter with a '
                  'scale, a card reader, rolls of tape and a few small parcels, a blank sign above it; behind the counter shelves with stacks '
                  'of flat-rate boxes and mail bins; on the left a wall of small brass PO boxes; on the right a retractable belt queue barrier '
                  'with chrome posts, a blank poster on the wall, a sad strand of tinsel along the counter, a window with snow outside; '
                  'fluorescent lights, beige linoleum floor across the lower third.',
    'momporch': 'Eye-level view of the small front porch of a cozy one-story ranch house of an old lady in the countryside at 2 am in '
                'winter: on the left a white front door with a blank doormat and a small dark rectangle doorbell spot, in the middle a big '
                'front picture window glowing blue-white from a TV inside, lace curtains half open, an armchair silhouette shape inside, a '
                'porch light glowing, a garden gnome by the steps, a wreath with a red bow on the door, a potted frozen plant, snow on the '
                'railing and the steps, a dark starry sky, bare trees, a parked old sedan covered in snow on the right.',
    'living': 'Eye-level wide view of the messy living room of an American suburban family house in the afternoon: on the left a tall white '
              'closed closet door with a round brass knob, in the middle a beige couch with throw pillows, a coffee table, a big TV on a '
              'stand, a decorated Christmas tree in the corner with a few gifts, a window with daylight and snow outside, framed blank '
              'pictures on the wall, on the right the front door with a small window and a coat rack; hardwood floor with a big rug across '
              'the lower third. Cozy warm colors.',
}

EDITS = {
    'porch_night': ('porch', 'Exactly the same porch, house, street and composition, same camera, but late at night: deep dark blue night sky '
                    'with stars, the warm porch lamp glowing, the house across the street completely covered in bright colorful Christmas '
                    'lights with a big glowing inflatable snowman on its lawn, warm orange street lamps along the street, frost on the lawn. '
                    'The porch, railing and columns of the near house have NO lights. Still no people, no text.'),
    'porch_dawn': ('porch', 'Exactly the same porch, house, street and composition, same camera, but at 6 am at sunrise in early December: '
                   'a pale pink and gold dawn sky, frost on the lawn and the railing, the porch lamp still on, the neighbor house across the '
                   'street with dim Christmas lights, a light morning mist on the street. Still no people, no text.'),
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        if n in EDITS:
            src, pr = EDITS[n]
            o = OUT / f'{n}.png'
            if o.exists(): print('skip', n); continue
            xai.generate(STYLE + pr, [str(o)], ref_png=str(OUT / f'{src}.png'))
            continue
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
