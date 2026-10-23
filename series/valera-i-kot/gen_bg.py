"""xAI backgrounds for «Валера и кот» season 2 (16:9 1280x720, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/valera-i-kot/gen_bg.py [names...]
Heroes, notices, labels, light and particles are drawn in code on top; backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, modern indie pixel-art adventure game look, crisp visible pixels, rich environmental detail, '
         'shabby post-Soviet nine-storey panel apartment block, late autumn, wide 16:9 scene, front view, eye level. No characters, no people, '
         'no animals, no text, no letters, no numbers, no symbols; any signs, labels, calendars and papers are completely blank. ')
BG = {
    'bedroom': 'Small cramped Soviet bedroom in early grey morning: a sagging single bed with a patterned wool blanket and a big pillow in '
               'the lower middle, a big red-and-brown oriental carpet hanging on the wall above the bed, an old round mechanical alarm clock '
               'with two bells on a wooden bedside stool on the left, a lacquered wardrobe on the right with a mirror, a window with tulle '
               'curtains and frost on the glass, cracked white ceiling with a crack running across it and a simple ceiling lamp, '
               'worn parquet floor, cold blue morning light from the window.',
    'gena_flat': 'An apartment room in the middle of an endless DIY renovation: bare grey concrete walls with patches of plaster and a few '
                 'drilled holes, one wall half covered in torn old wallpaper, a stepladder in the middle left, bags of plaster mix and buckets '
                 'on the floor, a long wooden plank on two stools like a workbench, extension cords, a bare light bulb hanging on a wire, '
                 'dust in the air, an old radio on a crate, a window covered with plastic film, plastic sheet on the floor; the right half of '
                 'the back wall is an empty smooth plastered wall with nothing on it.',
    'landing': 'A narrow staircase landing in a Soviet panel apartment block: two old apartment doors side by side on the back wall, the left '
               'one padded with brown leatherette and brass studs, the right one a cheap steel door; a doorbell button and a blank number '
               'plate next to each door; green-painted lower walls and whitewashed upper walls with peeling paint, a dusty radiator, a '
               'window with a cracked pane on the far right, concrete steps going down at the lower right, a single bare bulb on the ceiling, '
               'plaster dust on the floor, a rubber doormat in front of each door.',
    'pantry': 'A tiny Soviet apartment storage pantry (кладовка) packed floor to ceiling with wooden shelves full of glass preserving jars: '
              'pickled cucumbers, tomatoes, red jam, compote with cherries, sauerkraut, all with metal lids, dozens and dozens of jars, '
              'many blank paper labels; a single bare bulb with a pull string, an old suitcase and a sledge on the top shelf, a wicker basket '
              'of potatoes on the floor, the open wooden pantry door frame around the view, warm dim yellow light; the floor in the middle '
              'is clear.',
}


def main(names):
    for n in names or BG:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        xai.generate(STYLE + BG[n], [str(out)], aspect='16:9')
        print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1:])
