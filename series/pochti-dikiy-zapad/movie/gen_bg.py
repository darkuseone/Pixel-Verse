"""xAI backgrounds for the feature cut (16:9, grok-imagine-image-2.0 medium 1k). Skips existing files.
  python3 series/pochti-dikiy-zapad/movie/gen_bg.py [names...]"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, indie game look, warm cinematic lighting, rich environmental detail, '
         'wide 16:9 scene, wild west setting. No characters, no people, no animals, no text, no letters, no numbers; '
         'any signs or boards are completely blank. ')
BG = {
    'ranch_dawn': 'Ranch yard at sunrise, pink and orange sky, a small wooden ranch house and barn on the left, hitching post and wooden fence, '
                  'one big saguaro cactus in the centre-left, dusty ground, soft long shadows, mesas on the horizon.',
    'desert_road': 'Bright sunny desert dirt road running left to right across the frame, red rock mesas in the distance, blue sky with a few '
                   'white pixel clouds, sparse cacti and dry bushes, tumbleweeds, open flat ground in the lower half for characters to ride on.',
    'cactus_field': 'Open sunny desert flat with many saguaro and prickly-pear cacti scattered, a wooden post on the left, dry grass tufts, '
                    'red mesas far away, hazy warm sky, wide empty ground in the lower half.',
    'ad_studio': 'Cheesy vintage TV commercial studio set, red velvet curtains, spotlight cone on a checkered floor, small wooden desk '
                 'with an old candlestick telephone, big empty easel board on the right, retro 1950s advertising mood.',
    'barn_board': 'Dim old wooden barn interior at night, hanging oil lantern casting warm light, hay bales, a huge blank cork board '
                  'fixed on the back wall taking the centre of the frame, a small table with a candle and papers in front, dust motes.',
    'town_gate': 'Entrance of a small dusty western town, wooden arch over the road with a big blank wooden sign board, saloon and '
                 'houses along the main street in the background, cacti beside the road, late morning sun, long empty road in front.',
    'training_field': 'Cowboy training ground in early morning, hay bales, wooden obstacle poles, a wooden fence, target cacti in a row, '
                      'a big rock, dusty ground, low golden sun, mesas on the horizon.',
    'sunset_road': 'Dramatic desert sunset, huge orange and purple sky, silhouetted mesas and saguaro cacti, long dirt road leading '
                   'to the horizon, glowing sun low on the right, peaceful ending mood, lots of empty space in the centre.',
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
