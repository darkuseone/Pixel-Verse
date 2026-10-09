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
    'deli': 'Front view of the deli counter inside a Florida supermarket: a long glass deli display case with trays of sliced meats, '
            'cheeses and salads in the middle, a meat slicer and a digital scale standing on top of the counter, behind it a wall with a big '
            'completely blank menu board, shelves with bread rolls and wrapped sandwiches, bright fluorescent lights, a polished floor in the '
            'lower third in front of the counter, clean and empty.',
    'hospital': 'Front view of a hospital billing and cashier window: a counter with a thick glass partition and a small speaking hole, a '
                'blank sign above it, a water cooler, a potted plant, pale green walls with a handrail, fluorescent ceiling lights, a linoleum '
                'floor in the lower third, a little rope barrier with stanchions, clean, sterile and slightly depressing.',
    'vet': 'Front view of the waiting room of a small Florida veterinary clinic: a row of plastic waiting chairs along the wall in the middle, '
           'a reception counter on the right, a big blank poster on the wall, a dog water bowl, a pet scale on the floor, a cat tree, a window '
           'with palm trees outside, cheerful pastel teal and yellow walls with painted paw prints, tiled floor in the lower third, empty.',
    'swamp': 'Side view of the Florida Everglades at noon: wide flat sawgrass marsh, a channel of dark still water across the lower third with '
             'lily pads, mangrove and cypress trees with Spanish moss, a small wooden dock on the left edge, distant herons, big cumulus '
             'clouds in a hot cyan sky, heat haze.',
    'booth': 'Front view of a small weathered wooden roadside kiosk booth in the Florida Everglades with a big open service window and a '
             'counter shelf in the middle, a completely blank sign board above the window, a cooler, wooden dock posts, sawgrass and palm '
             'trees around, a gravel parking area in the lower third, hot noon sun.',
    'jail_ext': 'Front view of the outside of a small county jail at night: a tall chain-link fence with a closed gate across the middle of '
                'the frame, behind it a beige concrete jail building with small barred windows and a completely blank sign, a tall light pole '
                'with a bright searchlight beam, palm trees, a dark blue night sky with stars, an empty parking lot in the lower third, warm '
                'yellow sodium lights.',
    'booking': 'Front view of the booking desk of a small county jail: a long high wooden counter in the middle with a computer monitor, a '
               'fingerprint pad and a small service bell, behind it a pale green wall with a bulletin board with blank papers and a round '
               'wall clock, a camera on a tripod on the right, fluorescent lights, a linoleum floor in the lower third, empty.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists():
            print('skip', p); continue
        xai.generate(STYLE + BG[n], [str(p)], '16:9')
