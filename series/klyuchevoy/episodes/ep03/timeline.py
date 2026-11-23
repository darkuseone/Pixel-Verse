"""S01E03 «КОРПОРАТИВ» (standard «голливудский уровень», reference E01 v2.1 / E02 v2). Timing from the tightened takes voice/ep03_t."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import kscommon as KC
SLUG = 'klyuchevoy'
FPS = 30
LUFS = -14.0
ORDER = ['s1', 'e1', 'f1', 'f2', 'l1', 'e2', 's2', 'e3', 's3', 'l2', 'f3']
VOICE, T0, END = KC.timing('ep03', ORDER, gaps=dict(f2=0.7, s2=0.9, f3=0.3), texts=KC.texts('ep03'))
DUR = round(END + 0.55, 2)
#       hook   aside  fik1   garland lyuda  toast  door   smug   plead  nelz   dance
CUTS = [0.0, T0['e1'], T0['f1'], T0['f2'] - 0.5, T0['l1'], T0['e2'], T0['s2'] - 0.8, T0['e3'], T0['s3'], T0['l2'], T0['f3'] - 0.2, DUR]
NAMES = ['hook', 'aside', 'fik1', 'garland', 'lyuda', 'toast', 'door', 'smug', 'plead', 'nelz', 'dance']
TWIST = T0['s2']
L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'phone_vibrate.mp3', 0.05, 0.8),
    (L + 'coat_rustle.mp3', T0['e1'], 0.45),
    (L + 'light_switch_click.mp3', T0['f2'] - 0.55, 1.0),
    (L + 'whoosh_1.mp3', T0['f2'] - 0.5, 0.35),
    (L + 'bottle_clink.mp3', T0['l1'] + 0.3, 0.6),
    (L + 'party_horn.mp3', T0['e2'] + 0.2, 0.55),
    (L + 'bottle_clink.mp3', T0['e2'] + 1.3, 0.8),
    (L + 'door_knock.mp3', T0['s2'] - 0.85, 1.0),
    (L + 'door_unlock_open.mp3', T0['e3'] - 0.2, 0.7),
    (L + 'steps_wood_floor.mp3', T0['s3'] - 0.3, 0.5),
    (L + 'party_horn.mp3', T0['f3'] - 0.15, 0.5),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 86.4, 0.0, T0['f2'] - 0.55, 0.75, True, VOICE_DIP),
    (CM + 'freepd_baltic_levity.mp3', 48.0, T0['f2'] - 0.4, TWIST - 0.9, 0.85, True, VOICE_DIP),
    (CM + 'freepd_managing_mischief.mp3', 164.0, T0['e3'], DUR, 0.80, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9, 'lyuda': 2.1}
