"""New SFX (-> library/sfx/) and two 15 s music loops (-> series/.../music/) for the feature cut. Skips existing files.
  python3 series/pochti-dikiy-zapad/movie/gen_audio.py [sfx|music]"""
import sys, pathlib, os
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'engine'))
import tts

SFX = [  # name, seconds, prompt
    ('vhs_rewind', 2.5, 'VHS tape rewind, whirring scrubbing tape noise, retro video cassette fast reverse'),
    ('film_click', 0.6, 'old film projector single click clack, short'),
    ('ad_jingle', 3.0, 'cheesy 1950s TV commercial jingle sting, cheerful bells and xylophone, short'),
    ('pencil_scribble', 1.5, 'pencil scribbling quickly on paper, scratchy'),
    ('pushpin_pop', 0.5, 'pushpin pressed into a cork board, short pop click'),
    ('slowmo_whoosh', 2.5, 'slow motion deep whoosh swoosh with a low rumble, cinematic'),
    ('counter_blip', 0.5, 'short retro 8-bit coin blip, cheerful'),
    ('title_stinger', 2.5, 'epic cinematic movie title sting, brass hit with big reverb, western'),
    ('glass_slide', 1.2, 'shot glass sliding along a wooden bar counter then a small clink'),
    ('needle_prick', 0.5, 'small sharp prick pop, cartoon needle poke, short'),
    ('record_scratch', 0.8, 'vinyl record scratch stop, comedic freeze frame'),
]
MUSIC = [  # name, seconds, prompt
    ('board_tension_15s', 15.0, 'Tense playful western investigation loop, plucked upright bass, pizzicato strings, ticking rhythm, '
                                'light spy-thriller mood, comedic, instrumental, seamless loop'),
    ('credits_swing_15s', 15.0, 'Upbeat triumphant western chiptune end-credits loop, twangy guitar and 8-bit synth, jaunty and warm, '
                                'instrumental, seamless loop'),
]

if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('all', 'sfx'):
        for n, sec, prompt in SFX:
            out = ROOT / 'library' / 'sfx' / f'{n}.mp3'
            if out.exists(): continue
            tts._post(f'{tts.API}/sound-generation', {'text': prompt, 'duration_seconds': sec}, out)
    if what in ('all', 'music'):
        for n, sec, prompt in MUSIC:
            out = ROOT / 'series' / 'pochti-dikiy-zapad' / 'music' / f'{n}.mp3'
            if out.exists(): continue
            tts._post(f'{tts.API}/music?output_format=mp3_44100_128', {'prompt': prompt, 'music_length_ms': int(sec * 1000),
                                                                     'model_id': 'music_v2_5', 'force_instrumental': True}, out)
