"""xAI backgrounds for «Florida Man: Allegedly» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/florida-man/gen_bg.py [names...]
Heroes, the A/C unit, the recliner, signs, light and particles are drawn in code on top; backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, modern indie pixel-art adventure game look, crisp visible pixels, rich environmental detail, '
         'hot sunny Florida, blazing noon sun high overhead, saturated tropical colours: turquoise, coral, mango, sun-bleached sand, '
         'short hard shadows, heat haze, wide 16:9 scene. No characters, no people, no animals, no vehicles, no text, no letters, '
         'no numbers, no logos, no flags, no symbols; any signs, labels and billboards are completely blank. ')
BG = {
    'yard': 'Side view of the back yard of a small old mobile home in a Florida trailer park at noon: the trailer wall with pale teal '
            'aluminium siding and a small window on the left half, a little wooden porch with three steps and a wooden railing on the far '
            'left, a patch of empty sandy ground and dry grass in the middle and right of the lower third, a plastic lawn chair, a palm tree, '
            'a chain-link fence, behind it a canal with green water and across the canal a big completely blank white billboard on tall poles, '
            'a highway overpass far away, fluffy white cumulus clouds in a bright cyan sky.',
    'store': 'Front view of the entrance of a big Florida supermarket at noon: a long stucco storefront painted pale green and white, a wide '
             'glass automatic sliding door entrance in the middle with dark glass, a big completely blank sign band above the entrance, '
             'shopping cart corral, potted palm trees on both sides of the door, a sidewalk in front, the hot asphalt parking lot with white '
             'painted parking lines across the lower third, empty, heat shimmer, bright cyan sky with clouds.',
    'aisle': 'Front view of the frozen food aisle inside a supermarket: a long row of tall glass-door freezer cases along the back wall facing '
             'the viewer, the glass doors frosty with condensation, colourful frozen food boxes on the shelves inside (no readable text), '
             'chrome door handles, cold blue-white interior light, a blank hanging aisle sign, bright fluorescent ceiling lights, a shiny '
             'polished pale floor tiles across the lower third with long reflections, clean and empty.',
    'cell': 'Front view of the inside of a small county jail cell looking at its back wall: painted cinder block wall in pale institutional '
            'green, a plain steel bunk bed attached to the wall at the left with a thin grey mattress, a small high window with bars and a '
            'beam of hot sunlight, a square air-conditioning vent grille high on the right side of the wall, a concrete floor in the lower '
            'third, gritty and plain.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists():
            print('skip', p); continue
        xai.generate(STYLE + BG[n], [str(p)], '16:9')
