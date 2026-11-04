"""xAI backgrounds for «Aura Dad» (16:9 1280x720, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/aura-dad/gen_bg.py [names...]
Heroes, MIRRA's face, phone screens, signs, light and particles are drawn in code; backgrounds have no people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, bright cheerful American suburban sitcom look, modern indie pixel-art adventure game '
         'style, crisp visible pixels, rich environmental detail, saturated warm desert colours with lavender and aqua accents, Arizona '
         'suburb, wide 16:9 scene, front view, eye level. No characters, no people, no animals, no text, no letters, no numbers, no '
         'symbols; any signs, labels, calendars, posters, screens and papers are completely blank. ')
BG = {
    'kitchen': 'A sunny open-plan kitchen of a beige stucco suburban house in Phoenix, Arizona, morning. Back wall: white shaker cabinets, '
               'a stainless steel double-door fridge on the left, a big window in the centre with a view of a desert backyard with a tall '
               'saguaro cactus, gravel, a pool fence and bright blue sky; a coffee maker and a fruit bowl on the counter; a blank framed '
               'wooden sign on the wall; a wall clock; pendant lamps. In the foreground right a light wood breakfast table with two chairs '
               'and a coffee mug; terracotta tile floor. The middle of the floor is clear empty space.',
    'bathroom': 'A suburban master bathroom in Arizona, bright morning light. In the exact centre of the back wall above a white double '
                'vanity sink with a quartz top: one large oval mirror with a thin brushed metal frame, the mirror glass is plain soft '
                'grey-blue with a gentle diagonal shine and reflects nothing. Around it: lavender painted walls, white subway tiles, two wall '
                'sconces, a small window with frosted glass on the right, a towel ring with a fluffy aqua towel, a succulent in a pot, '
                'toothbrush cup, soap dispenser, a bath mat on light grey tile floor. The space in front of the sink is clear.',
    'sephoria': 'Inside a trendy beauty cosmetics store in a big suburban shopping mall, bright and glossy. Left half: tall glowing white '
                'shelves packed with hundreds of colourful skincare bottles, jars and tubes in pastel pink, lavender, mint and gold, little '
                'tester stands, round mirrors on poles. Back wall: a wide glass shopfront and open entrance showing a mall corridor with a '
                'fountain, palm plants and other shop fronts. Right third: a long white checkout counter with a card terminal, a small '
                'display of mini products and paper shopping bags behind it. Black and white striped accent band along the top of the walls, '
                'pink neon ring lights on the ceiling, glossy white floor tiles with reflections. The floor in the middle is clear empty space.',
    'backyard': 'A sunny suburban backyard in Phoenix, Arizona, late afternoon golden light. Centre and right: a kidney-shaped turquoise '
                'swimming pool with a white coping edge and a small diving board, a pool float shaped like a flamingo, ripples. Left: a '
                'stainless steel barbecue grill on a stone patio with a striped umbrella, a cooler and patio chairs. Background: a tan '
                'stucco block wall, the back of the neighbour house with a red tile roof and a small security camera under the eave, '
                'palm trees, a tall saguaro cactus, desert mountains far away, blue sky with a few clouds. Gravel and desert plants, '
                'string lights over the patio. The patio floor in front of the grill and the pool edge is clear empty space.',
}


def main(names):
    for n in names or BG:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        xai.generate(STYLE + BG[n], [str(out)], aspect='16:9')
        print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1:])
