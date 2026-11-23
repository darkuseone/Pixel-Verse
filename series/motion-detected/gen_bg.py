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
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        outs = [OUT / f'{n}.png', OUT / f'{n}_b.png']
        if outs[0].exists(): print('skip', n); continue
        xai.generate(STYLE + BG[n], [str(o) for o in outs])
